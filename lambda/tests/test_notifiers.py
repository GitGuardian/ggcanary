from lambda_py.notifiers import NOTIFIER_CLASSES


def test_notifiers_distinct_names():
    notifier_classes_by_kind = {
        notif_class.kind: notif_class for notif_class in NOTIFIER_CLASSES
    }
    assert len(notifier_classes_by_kind) == len(
        NOTIFIER_CLASSES
    ), "multiple notifier classes have the same kind"
