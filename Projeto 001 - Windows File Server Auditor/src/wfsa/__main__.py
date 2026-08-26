import argparse
import json
import os
import subprocess
import tempfile
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path

from wfsa.services.audit import run_audit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Windows File Server Auditor",
    )

    parser.add_argument(
        "--server",
        required=True,
        help="Nome ou endereço do servidor de arquivos.",
    )

    parser.add_argument(
        "--path",
        required=True,
        help="Caminho raiz que será auditado.",
    )

    parser.add_argument(
        "--reference-date",
        default=None,
        help="Data de referência no formato YYYY-MM-DD.",
    )

    return parser


def json_default(value):
    """Converte objetos não suportados diretamente pelo JSON."""

    if isinstance(value, datetime):
        return value.isoformat()

    if is_dataclass(value):
        return asdict(value)

    if hasattr(value, "__dict__"):
        return value.__dict__

    raise TypeError(
        f"Objeto não serializável para JSON: {type(value).__name__}"
    )


def create_credential_file() -> str:
    """
    Solicita a credencial uma única vez e salva em um arquivo
    CLIXML temporário para reutilização pelos scripts PowerShell.
    """

    credential_file = Path(
        tempfile.gettempdir()
    ) / "wfsa-credential.xml"

    powershell = r"""
$credential = Get-Credential

if (-not $credential) {
    throw "Nenhuma credencial foi informada."
}

$credential | Export-Clixml -Path $env:WFSA_CREDENTIAL_FILE
"""

    env = os.environ.copy()
    env["WFSA_CREDENTIAL_FILE"] = str(credential_file)

    subprocess.run(
        [
            r"C:\Program Files\PowerShell\7\pwsh.exe",
            "-NoProfile",
            "-Command",
            powershell,
        ],
        env=env,
        check=True,
    )

    if not credential_file.exists():
        raise RuntimeError(
            "O arquivo de credencial não foi criado."
        )

    return str(credential_file)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.reference_date:
        reference_date = datetime.strptime(
            args.reference_date,
            "%Y-%m-%d",
        )
    else:
        reference_date = datetime.now()

    credential_file = create_credential_file()

    try:
        result = run_audit(
            server=args.server,
            path=args.path,
            reference_date=reference_date,
            credential_file=credential_file,
        )

        print(
            json.dumps(
                result,
                default=json_default,
                ensure_ascii=False,
                indent=2,
            )
        )

    finally:
        try:
            Path(credential_file).unlink(missing_ok=True)
        except OSError:
            pass


if __name__ == "__main__":
    main()