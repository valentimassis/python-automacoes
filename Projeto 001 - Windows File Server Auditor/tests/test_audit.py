from datetime import datetime

from wfsa.models.audit import AuditResult
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

    result = AuditResult(
        server="lst-fs01",
        reference_date=datetime(2026, 8, 20),
        shares=[share],
        findings=[finding],
    )

    assert result.server == "lst-fs01"
    assert result.reference_date.year == 2026
    assert result.total_shares == 1
    assert result.total_findings == 1
    assert result.findings[0].severity == "HIGH"
    assert result.shares[0].name == "Financeiro$"
