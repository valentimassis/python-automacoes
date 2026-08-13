import json
import subprocess
from pathlib import Path

from wfsa.models.share import Share


def get_shares(server: str) -> list[Share]:
    """Coleta os compartilhamentos SMB de um servidor Windows."""

    script = (
        Path(__file__).resolve().parent.parent
        / "powershell"
        / "smb_shares.ps1"
    )

    command = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script),
        "-Server",
        server,
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
        Share(
            name=item["Name"],
            path=item["Path"],
            description=item["Description"] or "",
            share_type=item["ShareType"],
        )
        for item in data
    ]