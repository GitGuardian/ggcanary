import abc
import json
from typing import Dict, List
from urllib import request

from ..types import ReportEntry
from .abstract_notifier import INotifier


class IWebhookNotifier(INotifier, abc.ABC):
    def __init__(self):
        self.template_parameters = self.params()

    @abc.abstractmethod
    def format_payload(self, report_entries: List[ReportEntry]) -> Dict:
        pass

    @property
    def extra_headers(self) -> Dict[str, str]:
        return {}

    @property
    @abc.abstractmethod
    def url(self) -> str:
        pass

    def generate_headers(self, data_encoded) -> Dict[str, str]:
        return {
            "Content-Type": "application/json; charset=utf-8",
            "Content-length": str(len(data_encoded)),
            **self.extra_headers,
        }

    def send_notification(self, report_entries: List[ReportEntry]):
        req = request.Request(self.url)
        data = self.format_payload(report_entries)
        data_encoded = json.dumps(data).encode("utf-8")
        for header_key, header_value in self.generate_headers(data_encoded).items():
            req.add_header(header_key, header_value)
        request.urlopen(req, data_encoded)
