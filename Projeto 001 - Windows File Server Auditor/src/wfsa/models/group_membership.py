from dataclasses import dataclass


@dataclass
class GroupMembership:
    """Representa a associação de uma identidade a um grupo do AD."""

    group_name: str
    group_sid: str
    member_name: str
    member_object_type: str
    member_sid: str
