from typing import List, Type

from .abstract_notifier import INotifier
from .sendgrid_notifier import SendGridNotifier
from .ses_notifier import SESNotifier
from .slack_notifier import SlackNotifier


NOTIFIER_CLASSES: List[Type[INotifier]] = [SESNotifier, SlackNotifier, SendGridNotifier]

__all__ = (NOTIFIER_CLASSES,)
