from datetime import datetime

from wfsa.analyzers.file_metadata import analyze_old_files
from wfsa.models.file_metadata import FileMetadata
from wfsa.models.finding import Finding


def analyze_files(
    files: list[FileMetadata],
    reference_date: datetime,
) -> list[Finding]:
    """Analisa metadados dos arquivos e retorna findings."""

    return analyze_old_files(
        files=files,
        reference_date=reference_date,
    )
