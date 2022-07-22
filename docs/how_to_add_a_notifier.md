# How to add a new notifier

This document will present the steps required to add a new notifier.

## Context

The lambda function will be called each time a log file is exported by CloudTrail to it's bucket. The lambda function will parse each log record, and filter-in those relative to the usage of a GitGuardian Canary Token.
The log records are then aggregated by username (that is, of the AWS user associated with a GitGuardian Canary Token). This gives us a list of `ReportEntry`.
Whenever this list is not empty, the enabled notifiers are called with this list as input.

## Create a new notifier

### Add a dedicated python class

Each notifier needs to have a dedicated class, inheriting from the `lambda_py.notifiers.abstract_notifier.INotifier` class. The new class will need to specify two things:

1. A class attribute `NAME`, which will be used to detect whether the notifier was enabled in the terraform configuration.
2. The `send_notification` method. This method takes as input a list of `lambda_py.types.ReportEntry` objects, and does whatever needs to be done to send the notification to an external service.
3. It is also possible to add an `__init__` method, e.g. to fetch parameter values from environment variables.

Finally, you need to modify the `lambda_py/notifiers/__init__.py` file:

1. Import your notifier class.
2. Add it to the `NOTIFIER_CLASSES` list.

### Extend the terraform configuration

You will need to modify the `variables.tf` file:

1. Add a variable specific to your notifier, for example `Custom_notifier`. This variable must have two fields:

- `enabled` (`bool`), which will specify whether this notifier is enabled
- `parameters` (`object`), which will hold configuration bits specific to this notifier. The subfields of the `parameters` field will be passed as-is to the lambda function, as environment variables. This means `parameters` should be a mapping from string to string.

2. Extend the `locals.parameters` block with the configuration for you notifier.

- The `name` field should be the same as the one used in your notifier class (comparison will be made case-independant).
- The `enabled` and `parameters` take the values from the variable declared above.

### Example

Python class: `lambda/lambda_py/notifiers/my_notifier.py`

```python
import os
from ..types import ReportEntry
from .abstract_notifier import INotifier

class MyNotifier(INotifier):
    NAME = "MY_NOTIFIER"

    def __init__(self):
        self.param = os.environ["MY_PARAM"]

    def send_notification(self, report_entries: List[ReportEntry]):
        # format entries and send message
        pass

```

Update nofiers `__init__.py` file:

```python
from typing import List, Type

from .abstract_notifier import INotifier
from .ses_notifier import SESNotifier
...
from .my_notifier import MyNotifier

NOTIFIER_CLASSES: List[Type[INotifier]] = [SESNotifier, ..., MyNotifier]

__all__ = (NOTIFIER_CLASSES)
```

Update `variables.tf`:

```terraform
variable my_notifier {
  type = object({
    enabled = bool
    parameters = object({
      MY_PARAM = string
    })
  })
  default = {
    enabled    = false
    parameters = null
  }
}

locals {
  notifiers = [
    {
      name       = "SES"
      enabled    = var.SES_notifier.enabled
      parameters = var.SES_notifier.parameters
    },
    {
      ...
    },
    {
      name       = "MY_NOTIFIER"
      enabled    = var.my_notifier.enabled
      parameters = var.my_notifier.parameters
    }
  ]
}
```
