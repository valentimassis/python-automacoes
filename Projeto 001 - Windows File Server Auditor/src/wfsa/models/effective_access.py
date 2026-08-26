from dataclasses import dataclass


@dataclass
class EffectiveAccess:
    """Representa o acesso efetivo identificado para uma identidade."""

    account_name: str
    identity_type: str
    smb_access: str | None
    ntfs_access: str | None
    effective_access: str | None
    risk_level: str
