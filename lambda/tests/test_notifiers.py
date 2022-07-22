import os
from unittest import mock

from lambda_py.notifiers import NOTIFIER_CLASSES, SendGridNotifier, SlackNotifier
from lambda_py.notifiers.abstract_notifier import INotifier


def test_notifiers_name_uppercase():
    """
    GIVEN a notifier class
    WHEN it is one of the exported notifier, or the abstract notifier
    THEN it's NAME attribute is uppercase
    """
    for notifier_class in NOTIFIER_CLASSES:
        assert notifier_class.NAME == notifier_class.NAME.upper()

    assert INotifier.NAME == INotifier.NAME.upper()


@mock.patch.dict(
    os.environ,
    {
        "SENDGRID_API_KEY": "DUMMY_API_KEY",
        "SENDGRID_SOURCE_EMAIL_ADDRESS": "canary@ggcanary.com",
        "SENDGRID_DEST_EMAIL_ADDRESSES": "security@ggcanary.com",
    },
)
def test_sendgrid_notifier():
    sendgrid_notifier = SendGridNotifier()
    assert sendgrid_notifier.extra_headers == {"Authorization": "Bearer DUMMY_API_KEY"}


@mock.patch.dict(
    os.environ,
    {
        "SLACK_WEBHOOK": "https://hooks.slack.com/services/MY_WEBHOOK",
    },
)
def test_slack_notifier_url():
    slack_notifier = SlackNotifier()
    assert slack_notifier.url == "https://hooks.slack.com/services/MY_WEBHOOK"
