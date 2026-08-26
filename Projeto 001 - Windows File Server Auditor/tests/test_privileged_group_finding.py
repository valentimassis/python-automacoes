from wfsa.services.privileged_group_finding import (
    create_privileged_group_finding,
)


def test_create_privileged_group_finding():
    finding = create_privileged_group_finding(
        server="LST-FS01",
        share_name="Financeiro",
        path=r"E:\Shares\Financeiro",
        account_name="Acesso_Financeiro",
        privileged_groups=["Domain Admins"],
    )

    assert finding is not None
    assert finding.severity == "HIGH"
    assert finding.account_name == "Acesso_Financeiro"
    assert "Domain Admins" in finding.description


def test_no_finding_without_privileged_groups():
    finding = create_privileged_group_finding(
        server="LST-FS01",
        share_name="Financeiro",
        path=r"E:\Shares\Financeiro",
        account_name="Acesso_Financeiro",
        privileged_groups=[],
    )

    assert finding is None


def test_multiple_privileged_groups_are_reported():
    finding = create_privileged_group_finding(
        server="LST-FS01",
        share_name="Financeiro",
        path=r"E:\Shares\Financeiro",
        account_name="Acesso_Financeiro",
        privileged_groups=[
            "Domain Admins",
            "Enterprise Admins",
        ],
    )

    assert finding is not None
    assert "Domain Admins" in finding.description
    assert "Enterprise Admins" in finding.description
