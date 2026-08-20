from datetime import datetime

from wfsa.analyzers.file_metadata import analyze_old_files
from wfsa.collectors.file_metadata import get_file_metadata
from wfsa.models.audit import AuditResult


def run_audit(
    server: str,
    path: str,
    reference_date: datetime,
) -> AuditResult:
    """Executa a auditoria de metadados e retorna o resultado consolidado."""

    files = list(
        get_file_metadata(
            server=server,
            path=path,
        )
    )

    findings = analyze_old_files(
        files=files,
        reference_date=reference_date,
    )

    return AuditResult(
        server=server,
        reference_date=reference_date,
        files=files,
        findings=findings,
    )
