import json
import subprocess

from wfsa.models.permission import Permission


def get_permissions(server: str, share_name: str) -> list[Permission]:
    """Coleta as permissões SMB de um compartilhamento."""

    script_path = (
        "src/wfsa/powershell/smb_permissions.ps1"
    )

    command = [
        "powershell.exe",
        "-NoProfile",
        "-File",
        script_path,
        "-Server",
        server,
        "-ShareName",
        share_name,
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )

    data = json.loads(result.stdout)

    if isinstance(data, dict):
        data = [data]

    return [
        Permission(
            account_name=item["AccountName"],
            access_control_type=item["AccessControlType"],
            access_right=item["AccessRight"],
            scope_name=item["ScopeName"],
        )
        for item in data
    ]