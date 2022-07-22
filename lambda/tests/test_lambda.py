from unittest.mock import patch

import pytest
from conftest import (
    BUCKET_NAME,
    LOGFILE_NO_GGCANARY,
    LOGFILE_W_GGCANARY,
    make_trigger_event,
)

from lambda_py import lambda_function
from lambda_py.notifiers.ses_notifier import SESNotifier


@pytest.mark.parametrize(
    "key,nb_records",
    (
        (LOGFILE_W_GGCANARY, 3),
        (LOGFILE_NO_GGCANARY, 3),
    ),
)
def test_fetch_logs(key, nb_records, mock_aws_data):
    records = lambda_function.fetch_log_records(bucket=BUCKET_NAME, key=key)
    assert len(records) == nb_records


def test_get_report_entries_ggcanary(mock_aws_data):
    records = lambda_function.fetch_log_records(
        bucket=BUCKET_NAME, key=LOGFILE_W_GGCANARY
    )
    report_entries = lambda_function.get_report_entries(records)
    assert len(report_entries) == 2


def test_get_report_entries_no_ggcanary(mock_aws_data):
    records = lambda_function.fetch_log_records(
        bucket=BUCKET_NAME, key=LOGFILE_NO_GGCANARY
    )
    report_entries = lambda_function.get_report_entries(records)
    assert len(report_entries) == 0


@pytest.mark.parametrize("log_file", (LOGFILE_W_GGCANARY, LOGFILE_NO_GGCANARY))
def test_lambda_handler(log_file, mock_aws_data):
    event = make_trigger_event(bucket_name=BUCKET_NAME, key=log_file)
    lambda_function.handler(event)


@patch.object(SESNotifier, "send_notification")
def test_lambda_handler_with_ses_notifier(
    mock_method,
    mock_aws_data,
    mock_ses_validation,
    mock_ses_notifier_env_variables,
):

    notifiers = lambda_function.load_notifiers()
    assert len(notifiers) == 1
    assert notifiers[0].__class__ == SESNotifier

    event = make_trigger_event(bucket_name=BUCKET_NAME, key=LOGFILE_W_GGCANARY)
    lambda_function.handler(event)
    mock_method.assert_called()
