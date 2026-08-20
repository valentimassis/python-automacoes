from wfsa.models.finding import Finding


def test_finding_contains_permission_context():
    finding = Finding(
        server="lst-fs01",
        share_name="Financeiro$",
        path=r"E:\Shares\Financeiro",
        severity="HIGH",
        title="Teste",
        description="Finding de teste.",
        account_name="Everyone",
        access_right="FullControl",
        access_control_type="Allow",
        is_inherited=True,
    )

    assert finding.account_name == "Everyone"
    assert finding.access_right == "FullControl"
    assert finding.access_control_type == "Allow"
    assert finding.is_inherited is True
