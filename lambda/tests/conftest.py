import os

import boto3
import moto
import pytest

from lambda_py.notifiers import SESNotifier


# constants for mock data
AWS_REGION = "us-west-2"
BUCKET_NAME = "cloudtrail_logs"
LOGFILE_NO_GGCANARY = "logs_no_ggcanary.json.gz"
LOGFILE_W_GGCANARY = "logs_w_ggcanary.json.gz"

# env variables for the lambda
os.environ["GGCANARY_USER_PREFIX"] = "ggcanary"

# avoid using real aws credentials
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = AWS_REGION

NOTIFIER_PARAMS = {
    "SES": {
        "DEST_EMAIL_ADDRESS": "test@test.com",
        "SOURCE_EMAIL_ADDRESS": "ggcanary@test.com",
    }
}


def make_trigger_event(bucket_name: str, key: str):
    return {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "eventTime": "2022-01-18T08:16:20.681Z",
                "eventName": "ObjectCreated:Put",
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "tf-s3-lambda-20220117151710690800000002",
                    "bucket": {
                        "name": bucket_name,
                    },
                    "object": {
                        "key": key,
                    },
                },
            }
        ]
    }


def setup_s3(s3):
    location = {"LocationConstraint": AWS_REGION}
    s3.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration=location)

    for log_file_name in [LOGFILE_NO_GGCANARY, LOGFILE_W_GGCANARY]:
        with open(f"tests/data/{log_file_name}", "rb") as f:
            s3.put_object(Body=f.read(), Bucket=BUCKET_NAME, Key=log_file_name)


def setup_iam(iam):
    iam.create_user(UserName="ggcanary-Alice")
    iam.create_user(UserName="ggcanary-Bob")


def setup_ses(ses):
    ses.verify_email_identity(
        EmailAddress=NOTIFIER_PARAMS["SES"]["SOURCE_EMAIL_ADDRESS"]
    )


@pytest.fixture(scope="session")
def mock_aws_data():
    with moto.mock_iam(), moto.mock_s3(), moto.mock_ses():
        iam = boto3.client("iam")
        setup_iam(iam)
        s3 = boto3.client("s3", region_name=AWS_REGION)
        setup_s3(s3)
        yield None


@pytest.fixture
def mock_ses_validation():
    ses = boto3.client("ses")
    setup_ses(ses)
    yield None


@pytest.fixture
def mock_ses_notifier_env_variables(monkeypatch):
    monkeypatch.setenv("ENABLED_NOTIFIERS", SESNotifier.NAME)
    for key, value in NOTIFIER_PARAMS["SES"].items():
        monkeypatch.setenv(f"SES_{key}", value)
