import json
import subprocess
from pathlib import Path

from wfsa.models.share import Share


def get_shares(
    server: str,
    credential_file: str | None = None,
) -> list[Share]:
    """Coleta os compartilhamentos SMB de um servidor Windows."""

    script = (
        Path(__file__).resolve().parent.parent
        / "powershell"
        / "smb_shares.ps1"
    )

    command = [
        r"C:\Program Files\PowerShell\7\pwsh.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script),
        "-Server",
        server,
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
        Share(
            name=item["Name"],
            path=item["Path"],
            description=item["Description"] or "",
            share_type=item["ShareType"],
        )
        for item in data
    ]
