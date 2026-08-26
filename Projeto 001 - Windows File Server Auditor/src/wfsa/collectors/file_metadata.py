import base64
import subprocess
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path

from wfsa.models.file_metadata import FileMetadata


def _decode_base64(value: str) -> str:
    return base64.b64decode(value).decode("utf-8")


def get_file_metadata(
    server: str,
    path: str,
    credential_file: str | None = None,
) -> Iterator[FileMetadata]:
    """Coleta metadados dos arquivos em streaming."""

    script_path = (
        Path(__file__).resolve().parent.parent
        / "powershell"
        / "file_metadata.ps1"
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
        command.extend(["-CredentialFile", credential_file])

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        check=True,
    )

    if not result.stdout:
        return

    for line_number, line in enumerate(
        result.stdout.splitlines(),
        start=1,
    ):
        line = line.strip()

        if not line:
            continue

        fields = line.split("|")

        if len(fields) != 7:
            raise ValueError(
                f"Registro inválido na linha {line_number}: "
                f"esperados 7 campos, encontrados {len(fields)}"
            )

        (
            name_encoded,
            path_encoded,
            extension_encoded,
            length_text,
            creation_time_encoded,
            last_write_time_encoded,
            last_access_time_encoded,
        ) = fields

        yield FileMetadata(
            server=server,
            path=_decode_base64(path_encoded),
            name=_decode_base64(name_encoded),
            extension=_decode_base64(extension_encoded),
            size=int(length_text),
            creation_time=datetime.fromisoformat(
                _decode_base64(creation_time_encoded)
            ),
            last_write_time=datetime.fromisoformat(
                _decode_base64(last_write_time_encoded)
            ),
            last_access_time=datetime.fromisoformat(
                _decode_base64(last_access_time_encoded)
            ),
        )
