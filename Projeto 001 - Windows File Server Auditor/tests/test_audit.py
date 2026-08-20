from datetime import datetime

from wfsa.models.audit import AuditResult
from wfsa.models.file_metadata import FileMetadata
from wfsa.models.finding import Finding
from wfsa.models.share import Share


def test_audit_result():
    finding = Finding(
        server="lst-fs01",
        share_name="Financeiro$",
        path=r"E:\Shares\Financeiro",
        severity="HIGH",
        title="Teste",
        description="Finding de teste.",
    )

    share = Share(
        name="Financeiro$",
        path=r"E:\Shares\Financeiro",
        description="Financeiro",
        share_type="FileSystemDirectory",
    )

    file_metadata = FileMetadata(
        server="lst-fs01",
        path=r"E:\Shares\Financeiro\arquivo.xlsx",
        name="arquivo.xlsx",
        extension=".xlsx",
        size=1024,
        creation_time=datetime(2020, 1, 1),
        last_write_time=datetime(2022, 1, 1),
        last_access_time=datetime(2022, 1, 1),
    )

    result = AuditResult(
        server="lst-fs01",
        reference_date=datetime(2026, 8, 20),
        shares=[share],
        files=[file_metadata],
        findings=[finding],
    )

    assert result.server == "lst-fs01"
    assert result.reference_date.year == 2026
    assert result.total_shares == 1
    assert result.total_files == 1
    assert result.total_findings == 1
    assert result.findings[0].severity == "HIGH"
    assert result.shares[0].name == "Financeiro$"
    assert result.files[0].name == "arquivo.xlsx"
