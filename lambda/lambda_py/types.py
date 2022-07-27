from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class LogRecord:
    username: str
    sourceIPAddress: str
    time: str
    raw_data: Dict

    @classmethod
    def from_raw_record(cls, raw_record: Dict) -> Optional["LogRecord"]:
        username = raw_record.get("userIdentity", {}).get("userName")
        if username is None:
            return None
        sourceIPAddress = raw_record["sourceIPAddress"]
        time = raw_record["eventTime"]
        return cls(
            username=username,
            sourceIPAddress=sourceIPAddress,
            time=time,
            raw_data=raw_record,
        )


@dataclass
class ReportEntry:
    username: str
    tags: Dict[str, str]
    records: List[LogRecord]
