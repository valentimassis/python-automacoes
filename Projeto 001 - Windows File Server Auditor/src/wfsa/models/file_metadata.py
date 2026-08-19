from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileMetadata:
    """Representa os metadados de um arquivo em um servidor Windows."""

    server: str
    path: str
    name: str
    extension: str
    size: int
    creation_time: datetime
    last_write_time: datetime
    last_access_time: datetime
