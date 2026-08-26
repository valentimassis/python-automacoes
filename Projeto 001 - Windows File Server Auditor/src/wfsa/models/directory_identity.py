from dataclasses import dataclass


@dataclass
class DirectoryIdentity:
    """Representa uma identidade encontrada no Active Directory."""

    name: str
    sam_account_name: str
    object_type: str
    sid: str
    distinguished_name: str
