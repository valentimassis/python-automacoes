import json
import subprocess
from pathlib import Path

from wfsa.models.group_membership import GroupMembership


def get_group_members(
    group_name: str,
) -> list[GroupMembership]:
    """Consulta os membros de um grupo no Active Directory."""

    script_path = (
        Path(__file__).resolve().parent.parent
        / "powershell"
        / "group_members.ps1"
    )

    command = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script_path),
        "-GroupName",
        group_name,
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )

    stdout = result.stdout.strip()

    if not stdout:
        return []

    data = json.loads(stdout)

    if isinstance(data, dict):
        data = [data]

    return [
        GroupMembership(
            group_name=item["GroupName"],
            group_sid=item["GroupSID"],
            member_name=item["MemberName"],
            member_object_type=item["MemberObjectType"],
            member_sid=item["MemberSID"],
        )
        for item in data
    ]
