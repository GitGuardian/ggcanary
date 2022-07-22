from typing import Dict, List

from ..types import ReportEntry
from .format_utils import create_email_body, create_email_subject
from .webhook_notifier import IWebhookNotifier


class SendGridNotifier(IWebhookNotifier):
    NAME = "SENDGRID"
    """
    Template parameters (all mandatories):

    - SENDGRID_API_KEY: SendGrid API key
    - SOURCE_EMAIL_ADDRESS: The email address used for the From field
    - DEST_EMAIL_ADDRESSES: ',' separated lists of recipient email addresses
    """

    def __init__(self):
        super(SendGridNotifier, self).__init__()
        self.api_key = self.param("API_KEY")
        self.source_email_address = self.param("SOURCE_EMAIL_ADDRESS")
        self.dest_email_addresses = self.param("DEST_EMAIL_ADDRESSES").split(",")

    @property
    def url(self) -> str:
        return "https://api.sendgrid.com/v3/mail/send"

    @property
    def extra_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    def format_payload(self, report_entries: List[ReportEntry]) -> Dict:
        subject = create_email_subject(report_entries)
        content = create_email_body(report_entries)

        return {
            "personalizations": [
                {
                    "to": [{"email": x} for x in self.dest_email_addresses],
                }
            ],
            "from": {"email": self.source_email_address},
            "subject": subject,
            "content": [
                {
                    "type": "text/plain",
                    "value": content,
                }
            ],
        }
