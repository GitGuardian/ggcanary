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

1. Add a variable specific to your notifier, for example `Custom_notifier`. The variable type must be a list of object, where each object holds the configuration for a notifier instance (allowing to configure multiple notifiers of the same kind).

2. Extend the `locals.ggcanary_lambda_parameters` block with the configuration for your notifier.

### Update dependencies

If new dependencies were added, it is mandatory to add them to the Pipfile and run the following commands in the environment:

```
pipenv update
pipenv run pipfile2req | grep -v botocore | grep -v boto3 | grep -v s3transfer > requirements.txt
```

This will update the requirements.txt file.

### Example

Python class: `lambda/lambda_py/notifiers/my_notifier.py`

```python
import os
from ..types import ReportEntry
from .abstract_notifier import INotifier

class MyNotifier(INotifier):
    kind = "my_notifier"

    def __init__(self, param1, param2, **kwargs):
        self.param1 = param1
        self.param2 = param2

    def send_notification(self, report_entries: List[ReportEntry]):
        # format entries and send message
        pass

```

Update nofiers `__init__.py` file:

```python
from .ses_notifier import SESNotifier
...
from .my_notifier import MyNotifier

NOTIFIER_CLASSES = (SESNotifier, ..., MyNotifier)

__all__ = (NOTIFIER_CLASSES,)
```

Update `variables.tf`:

```terraform
variable my_notifiers {
  type = list(object({
    my_param = string
  }))
  default = []
}

locals {
  ggcanary_lambda_parameters = concat(
    [
      for notifier_config in var.SES_notifiers :
      {
        kind       = "ses"
        parameters = notifier_config
      }
    ],
    [
      ...
    ],
    [
      for notifier_config in var.my_notifiers :
      {
        kind       = "my_notifier"  # must correspond to the `kind` attribute of `MyNotifier`
        parameters = notifier_config
      }
    ]
  ]
}
```
