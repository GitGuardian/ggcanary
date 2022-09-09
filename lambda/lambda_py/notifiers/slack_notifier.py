from typing import Any, Dict, List

from ..types import ReportEntry
from .format_utils import format_report_entry
from .webhook_notifier import IWebhookNotifier


class SlackNotifier(IWebhookNotifier):
    kind = "slack"

    def __init__(self, webhook, **kwargs):
        super().__init__()
        self.webhook = webhook

    @property
    def url(self):
        return self.webhook

    def format_payload(self, report_entries: List[ReportEntry]) -> Dict[str, Any]:
        text = "\n\n".join(format_report_entry(entry) for entry in report_entries)
        return {"text": text, "type": "mrkdwn"}
