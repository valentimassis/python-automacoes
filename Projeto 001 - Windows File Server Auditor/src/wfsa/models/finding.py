from dataclasses import dataclass


@dataclass
class Finding:
    """Representa um risco identificado pelo auditor."""

    server: str
    share_name: str
    path: str
    severity: str
    title: str
    description: str
    account_name: str | None = None
    access_right: str | None = None
    access_control_type: str | None = None
    is_inherited: bool | None = None
