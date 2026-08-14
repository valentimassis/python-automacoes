from dataclasses import dataclass


@dataclass
class Permission:
    """Representa uma permissão de acesso a um compartilhamento SMB."""

    account_name: str
    access_control_type: str
    access_right: str
    scope_name: str