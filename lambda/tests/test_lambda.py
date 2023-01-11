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
from lambda_py.notifiers.webhook_notifier import IWebhookNotifier


@pytest.mark.parametrize(
    "key,nb_records",
    (
        (LOGFILE_W_GGCANARY, 3),
        (LOGFILE_NO_GGCANARY, 3),
    ),
)
def test_fetch_logs(key, nb_records):
    records = lambda_function.fetch_log_records(bucket=BUCKET_NAME, key=key)
    assert len(records) == nb_records


def test_get_report_entries_ggcanary():
    records = lambda_function.fetch_log_records(
        bucket=BUCKET_NAME, key=LOGFILE_W_GGCANARY
    )
    report_entries = lambda_function.get_report_entries(records)
    assert len(report_entries) == 2


def test_get_report_entries_no_ggcanary():
    records = lambda_function.fetch_log_records(
        bucket=BUCKET_NAME, key=LOGFILE_NO_GGCANARY
    )
    report_entries = lambda_function.get_report_entries(records)
    assert len(report_entries) == 0


@patch.object(SESNotifier, "send_notification")
@patch.object(IWebhookNotifier, "send_notification")
def test_lambda_handler_called(
    mock_method_1,
    mock_method_2,
    mock_ses_validation,
):

    notifiers = lambda_function.load_notifiers()
    assert len(notifiers) == 3
    assert notifiers[0].__class__ == SESNotifier

    event = make_trigger_event(bucket_name=BUCKET_NAME, key=LOGFILE_W_GGCANARY)
    lambda_function.handler(event)
    mock_method_1.assert_called()
    mock_method_2.assert_called()


@patch.object(SESNotifier, "send_notification")
@patch.object(IWebhookNotifier, "send_notification")
def test_lambda_handler_not_called(
    mock_method_1,
    mock_method_2,
):

    notifiers = lambda_function.load_notifiers()
    assert len(notifiers) == 3
    assert notifiers[0].__class__ == SESNotifier

    event = make_trigger_event(bucket_name=BUCKET_NAME, key=LOGFILE_NO_GGCANARY)
    lambda_function.handler(event)
    mock_method_1.assert_not_called()
    mock_method_2.assert_not_called()
