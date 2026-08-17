import json
import subprocess
from pathlib import Path

from wfsa.models.ntfs_permission import NtfsPermission


def get_ntfs_permissions(server: str, path: str) -> list[NtfsPermission]:
    """Coleta permissões NTFS de uma pasta em um servidor Windows."""

    script_path = (
        Path(__file__).resolve().parent.parent
        / "powershell"
        / "ntfs_permissions.ps1"
    )

    command = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script_path),
        "-Server",
        server,
        "-Path",
        path,
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        check=True,
    )

    stdout = result.stdout.decode("utf-8")
    data = json.loads(stdout)

    if isinstance(data, dict):
        data = [data]

    return [
        NtfsPermission(
            account_name=item["AccountName"],
            access_control_type=item["AccessControlType"],
            access_rights=item["AccessRights"],
            is_inherited=item["IsInherited"],
            inheritance_flags=item["InheritanceFlags"],
            propagation_flags=item["PropagationFlags"],
        )
        for item in data
    ]