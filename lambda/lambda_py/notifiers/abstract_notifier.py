import abc
from typing import List

from ..types import ReportEntry


class INotifier(abc.ABC):
    kind: str

    @abc.abstractmethod
    def send_notification(self, events: List[ReportEntry]):
        pass
