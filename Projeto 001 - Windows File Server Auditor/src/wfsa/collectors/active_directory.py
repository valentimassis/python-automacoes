import json
import subprocess
from pathlib import Path

from wfsa.models.directory_identity import DirectoryIdentity


def resolve_directory_identity(
    account_name: str,
) -> DirectoryIdentity | None:
    """Consulta uma identidade no Active Directory."""

    script_path = (
        Path(__file__).resolve().parent.parent
        / "powershell"
        / "resolve_identity.ps1"
    )

    command = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script_path),
        "-AccountName",
        account_name,
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
        return None

    data = json.loads(stdout)

    if not data:
        return None

    return DirectoryIdentity(
        name=data["Name"],
        sam_account_name=data["SamAccountName"],
        object_type=data["ObjectType"],
        sid=data["SID"],
        distinguished_name=data["DistinguishedName"],
    )
