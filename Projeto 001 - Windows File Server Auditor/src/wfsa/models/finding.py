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