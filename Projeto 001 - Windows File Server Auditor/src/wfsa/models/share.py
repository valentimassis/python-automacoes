from dataclasses import dataclass


@dataclass
class Share:
    """Representa um compartilhamento SMB de um servidor Windows."""

    name: str
    path: str
    protocol: str
    clustered: bool