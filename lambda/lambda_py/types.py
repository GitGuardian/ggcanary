from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class LogRecord:
    username: str
    sourceIPAddress: str
    time: str
    raw_data: Dict
    user_agent: str

    @classmethod
    def from_raw_record(cls, raw_record: Dict) -> Optional["LogRecord"]:
        username = raw_record.get("userIdentity", {}).get("userName")
        if username is None:
            return None
        sourceIPAddress = raw_record["sourceIPAddress"]
        time = raw_record["eventTime"]
        user_agent = raw_record["userAgent"]
        return cls(
            username=username,
            sourceIPAddress=sourceIPAddress,
            time=time,
            raw_data=raw_record,
            user_agent=user_agent,
        )


@dataclass
class ReportEntry:
    username: str
    tags: Dict[str, str]
    records: List[LogRecord]
