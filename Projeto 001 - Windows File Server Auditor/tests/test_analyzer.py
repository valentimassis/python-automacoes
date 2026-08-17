from wfsa.analyzers.permissions import analyze_permissions
from wfsa.models.permission import Permission
from wfsa.models.share import Share


def test_detect_everyone_full_access():
    share = Share(
        name="Financeiro$",
        path=r"E:\Shares\Financeiro",
        description="Financeiro",
        share_type="FileSystemDirectory",
    )

    permissions = [
        Permission(
            account_name="Everyone",
            access_control_type="Allow",
            access_right="Full",
            scope_name="*",
        )
    ]

    findings = analyze_permissions(
        server="lst-fs01",
        share=share,
        share_permissions=permissions,
        ntfs_permissions=[],
    )

    assert len(findings) == 1
    assert findings[0].severity == "HIGH"
    assert findings[0].share_name == "Financeiro$"