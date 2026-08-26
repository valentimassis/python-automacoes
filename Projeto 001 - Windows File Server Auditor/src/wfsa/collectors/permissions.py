import json
import subprocess
from pathlib import Path

from wfsa.models.permission import Permission


def get_permissions(
    server: str,
    share_name: str,
    credential_file: str | None = None,
) -> list[Permission]:
    """Coleta as permissões SMB de um compartilhamento."""

    script_path = (
        Path(__file__).resolve().parent.parent
        / "powershell"
        / "smb_permissions.ps1"
    )

    command = [
        r"C:\Program Files\PowerShell\7\pwsh.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script_path),
        "-Server",
        server,
        "-ShareName",
        share_name,
    ]

    if credential_file is not None:
        command.extend([
            "-CredentialFile",
            credential_file,
        ])

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        check=True,
    )

    stdout = result.stdout.strip()

    if not stdout:
        return []

    data = json.loads(stdout)

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
