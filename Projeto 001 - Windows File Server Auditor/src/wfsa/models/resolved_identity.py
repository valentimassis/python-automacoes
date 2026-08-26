from dataclasses import dataclass


@dataclass
class ResolvedIdentity:
    """Representa uma identidade resolvida a partir de uma ACL."""

    original_name: str
    identity_type: str
    resolved: bool
    name: str | None = None
    sam_account_name: str | None = None
    sid: str | None = None
    distinguished_name: str | None = None
