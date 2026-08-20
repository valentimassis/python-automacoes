from wfsa.analyzers.permissions import analyze_permissions
from wfsa.models.ntfs_permission import NtfsPermission
from wfsa.models.permission import Permission
from wfsa.models.share import Share


def test_detect_effective_everyone_modify_access():
    share = Share(
        name="Financeiro$",
        path=r"E:\Shares\Financeiro",
        description="Financeiro",
        share_type="FileSystemDirectory",
    )

    share_permissions = [
        Permission(
            account_name="Everyone",
            access_control_type="Allow",
            access_right="Full",
            scope_name="*",
        )
    ]

    ntfs_permissions = [
        NtfsPermission(
            account_name="Everyone",
            access_control_type="Allow",
            access_rights="Modify",
            is_inherited=False,
            inheritance_flags="ContainerInherit, ObjectInherit",
            propagation_flags="None",
        )
    ]

    findings = analyze_permissions(
        server="lst-fs01",
        share=share,
        share_permissions=share_permissions,
        ntfs_permissions=ntfs_permissions,
    )

    assert len(findings) == 1
    assert findings[0].severity == "HIGH"
    assert findings[0].title == "Acesso efetivo elevado para Everyone"
    assert "Modify" in findings[0].description
