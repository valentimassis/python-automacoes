import json
import subprocess
from pathlib import Path

from wfsa.models.ntfs_permission import NtfsPermission


def get_ntfs_permissions(
    server: str,
    path: str,
    credential_file: str | None = None,
) -> list[NtfsPermission]:
    """Coleta as permissões NTFS de um caminho."""

    script_path = (
        Path(__file__).resolve().parent.parent
        / "powershell"
        / "ntfs_permissions.ps1"
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
        "-Path",
        path,
    ]

    if credential_file is not None:
        command.extend(
            [
                "-CredentialFile",
                credential_file,
            ]
        )

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
        NtfsPermission(
            account_name=item["AccountName"],
            access_control_type=item["AccessControlType"],
            access_rights=item["AccessRight"],
            is_inherited=item["IsInherited"],
            inheritance_flags=item["InheritanceFlags"],
            propagation_flags=item["PropagationFlags"],
        )
        for item in data
    ]