import gzip
import json
import os
from collections import defaultdict
from typing import Dict, List

import boto3

from .notifiers import NOTIFIER_CLASSES
from .types import LogRecord, ReportEntry


USERNAME_TO_TRACK = os.environ["GGCANARY_USER_PREFIX"]
LAMBDA_PARAMETERS_PATH = "./builds/ggcanary_lambda_parameters.json"


def fetch_log_records(bucket: str, key: str) -> List[Dict]:
    """Return the list of log records from the given ``bucket`` and ``key``."""
    response = boto3.client("s3").get_object(Bucket=bucket, Key=key)
    json_data = gzip.decompress(response["Body"].read())
    data = json.loads(json_data)
    return data.get("Records", [])


def get_user_tags(username: str) -> Dict[str, str]:
    """Return the tags associated with a user"""
    # Note: in case there are many tags, the response will be paginated
    # See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_user_tags
    response = boto3.client("iam").list_user_tags(UserName=username)
    return {item["Key"]: item["Value"] for item in response["Tags"]}


def get_report_entries(records: List[Dict]) -> List[ReportEntry]:
    """Return the records associated with a ggcanary user as a mapping
    between username and relevant records."""
    records_by_username = defaultdict(list)
    for raw_record in records:
        record = LogRecord.from_raw_record(raw_record)
        if record is not None and record.username.startswith(USERNAME_TO_TRACK):
            records_by_username[record.username].append(record)

    return [
        ReportEntry(username=username, tags=get_user_tags(username), records=records)
        for username, records in records_by_username.items()
    ]


def load_notifiers():
    with open(LAMBDA_PARAMETERS_PATH) as json_file:
        notifier_configs = json.load(json_file)

    notifier_classes_by_kind = {
        notif_class.kind: notif_class for notif_class in NOTIFIER_CLASSES
    }
    # fmt: off
    notifiers = [
        notifier_classes_by_kind[notifier["kind"]](
            **notifier["parameters"]
        )
        for notifier in notifier_configs
    ]
    # fmt: on
    print(
        "Enabled notifiers:",
        [notifier.kind for notifier in notifiers],
    )
    return notifiers


def handler(event: Dict):
    notifiers = load_notifiers()

    src_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    src_key = event["Records"][0]["s3"]["object"]["key"]

    print(f"Fetching log file from {src_bucket}/{src_key}...")
    records = fetch_log_records(src_bucket, src_key)
    print(f"Fetched log file with {len(records)} entries")

    report_entries = get_report_entries(records)
    if len(report_entries) == 0:
        print("No ggcanary token was used.")
        return
    print(f"{len(report_entries)} ggcanary tokens were used; sending notification.")
    for notifier in notifiers:
        notifier.send_notification(report_entries)
