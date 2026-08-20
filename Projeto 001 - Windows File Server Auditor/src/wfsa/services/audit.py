from datetime import datetime

from wfsa.analyzers.file_metadata import analyze_old_files
from wfsa.analyzers.permissions import analyze_permissions
from wfsa.collectors.file_metadata import get_file_metadata
from wfsa.collectors.permissions import get_permissions
from wfsa.collectors.smb import get_shares
from wfsa.models.audit import AuditResult
from wfsa.models.permission import Permission


def run_audit(
    server: str,
    path: str,
    reference_date: datetime,
) -> AuditResult:
    """Executa a auditoria e retorna o resultado consolidado."""

    shares = get_shares(
        server=server,
    )

    permissions: list[Permission] = []
    findings = []

    for share in shares:
        share_permissions = get_permissions(
            server=server,
            share_name=share.name,
        )

        permissions.extend(share_permissions)

        findings.extend(
            analyze_permissions(
                server=server,
                share=share,
                share_permissions=share_permissions,
                ntfs_permissions=[],
            )
        )

    files = list(
        get_file_metadata(
            server=server,
            path=path,
        )
    )

    findings.extend(
        analyze_old_files(
            files=files,
            reference_date=reference_date,
        )
    )

    return AuditResult(
        server=server,
        reference_date=reference_date,
        shares=shares,
        permissions=permissions,
        files=files,
        findings=findings,
    )
