from typing import List

from ..types import ReportEntry
from .format_utils import format_report_entry
from .webhook_notifier import IWebhookNotifier


class SlackNotifier(IWebhookNotifier):
    NAME = "SLACK"

    def __init__(self):
        self.webhook = self.param("WEBHOOK")

    @property
    def url(self):
        return self.webhook

    def format_payload(self, report_entries: List[ReportEntry]):
        text = "\n\n".join(format_report_entry(entry) for entry in report_entries)
        return {"text": text, "type": "mrkdwn"}
