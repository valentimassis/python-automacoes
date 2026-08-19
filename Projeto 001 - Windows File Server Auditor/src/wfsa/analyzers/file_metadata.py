from datetime import datetime, timedelta
from collections.abc import Iterable

from wfsa.models.file_metadata import FileMetadata
from wfsa.models.finding import Finding


def _normalize_datetime(value: datetime, reference: datetime) -> datetime:
    """Normaliza datetime naive/aware para o mesmo formato."""

    if reference.tzinfo is None:
        if value.tzinfo is not None:
            return value.replace(tzinfo=None)
        return value

    if value.tzinfo is None:
        return value.replace(tzinfo=reference.tzinfo)

    return value.astimezone(reference.tzinfo)


def analyze_old_files(
    files: Iterable[FileMetadata],
    reference_date: datetime,
    years: int = 2,
) -> list[Finding]:
    """Identifica arquivos sem alteração ou acesso há mais de N anos."""

    cutoff_date = reference_date - timedelta(days=365 * years)

    findings: list[Finding] = []

    for file in files:
        last_write_time = _normalize_datetime(
            file.last_write_time,
            reference_date,
        )

        last_access_time = _normalize_datetime(
            file.last_access_time,
            reference_date,
        )

        old_write = last_write_time < cutoff_date
        old_access = last_access_time < cutoff_date

        if not old_write and not old_access:
            continue

        if old_write and old_access:
            title = "Arquivo sem alteração e acesso há mais de 2 anos"
            description = (
                "O arquivo não é alterado nem acessado há mais de "
                f"{years} anos."
            )
        elif old_write:
            title = "Arquivo sem alteração há mais de 2 anos"
            description = (
                f"O arquivo não é alterado há mais de {years} anos."
            )
        else:
            title = "Arquivo sem acesso há mais de 2 anos"
            description = (
                f"O arquivo não é acessado há mais de {years} anos."
            )

        findings.append(
            Finding(
                server=file.server,
                share_name="",
                path=file.path,
                severity="MEDIUM",
                title=title,
                description=description,
            )
        )

    return findings
