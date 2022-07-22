import abc
import os
from typing import List

from ..types import ReportEntry


class INotifier(abc.ABC):
    NAME = "ABSTRACT"

    @abc.abstractmethod
    def send_notification(self, events: List[ReportEntry]):
        pass

    @classmethod
    def param(cls, param_name):
        return cls.params()[param_name]

    @classmethod
    def params(cls):
        prefix = cls.NAME + "_"
        uppercased_env = {key.upper(): value for key, value in os.environ.items()}
        return {
            key[len(prefix) :]: value
            for key, value in uppercased_env.items()
            if key.startswith(prefix)
        }

    @classmethod
    def is_enabled(cls) -> bool:
        enabled_notifiers = os.environ.get("ENABLED_NOTIFIERS", "").upper().split(",")
        return cls.NAME in enabled_notifiers
