from dataclasses import dataclass


@dataclass
class NtfsPermission:
    """Representa uma permissão NTFS de uma pasta ou arquivo."""

    account_name: str
    access_control_type: str
    access_rights: str
    is_inherited: bool
    inheritance_flags: str
    propagation_flags: str