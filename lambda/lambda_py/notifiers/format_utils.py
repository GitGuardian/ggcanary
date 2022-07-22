from typing import List

from ..types import LogRecord, ReportEntry


def format_record(record: LogRecord) -> str:
    eventSource = record.raw_data.get("eventSource")
    eventName = record.raw_data.get("eventName")
    return f"- At *{record.time}*, from *{record.sourceIPAddress}* - called {eventSource}:{eventName}"


def format_report_entry(report_entry: ReportEntry) -> str:
    if report_entry.tags:
        tags = "User tags:\n" + "\n".join(
            [f"- *{key}*: {value}" for key, value in report_entry.tags.items()]
        )
    else:
        tags = "No user tag."

    records_formatted = "\n".join(
        [format_record(record) for record in report_entry.records]
    )

    entry_formatted = (
        f"User *{report_entry.username}*: {len(report_entry.records)} usage occurences.\n"
        f"{tags}\n"
        f"Usage details:\n"
        f"{records_formatted}"
    )
    return entry_formatted


def create_email_subject(report_entries: List[ReportEntry]) -> str:
    nb_entries = len(report_entries)
    if nb_entries > 1:
        return f"GGCanary report: {nb_entries} keys triggered"
    else:
        return "GGCanary report: 1 key triggered"


def create_email_body(report_entries: List[ReportEntry]) -> str:
    return "\n\n".join(format_report_entry(x) for x in report_entries)
