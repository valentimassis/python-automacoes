from wfsa.analyzers.permissions import analyze_permissions
from wfsa.models.ntfs_permission import NtfsPermission
from wfsa.models.share import Share


def test_detect_everyone_full_access_on_ntfs():
    share = Share(
        name="Financeiro$",
        path=r"E:\Shares\Financeiro",
        description="Financeiro",
        share_type="FileSystemDirectory",
    )

    ntfs_permissions = [
        NtfsPermission(
            account_name="Everyone",
            access_control_type="Allow",
            access_rights="FullControl",
            is_inherited=False,
            inheritance_flags="ContainerInherit, ObjectInherit",
            propagation_flags="None",
        )
    ]

    findings = analyze_permissions(
        server="lst-fs01",
        share=share,
        share_permissions=[],
        ntfs_permissions=ntfs_permissions,
    )

    assert len(findings) == 1
    assert findings[0].severity == "HIGH"
    assert findings[0].share_name == "Financeiro$"
    assert findings[0].title == "Pasta NTFS com Everyone em FullControl"

    assert findings[0].account_name == "Everyone"
    assert findings[0].access_right == "FullControl"
    assert findings[0].access_control_type == "Allow"
    assert findings[0].is_inherited is False


def test_detect_inherited_everyone_full_access_on_ntfs():
    share = Share(
        name="Financeiro$",
        path=r"E:\Shares\Financeiro",
        description="Financeiro",
        share_type="FileSystemDirectory",
    )

    ntfs_permissions = [
        NtfsPermission(
            account_name="Everyone",
            access_control_type="Allow",
            access_rights="FullControl",
            is_inherited=True,
            inheritance_flags="ContainerInherit, ObjectInherit",
            propagation_flags="None",
        )
    ]

    findings = analyze_permissions(
        server="lst-fs01",
        share=share,
        share_permissions=[],
        ntfs_permissions=ntfs_permissions,
    )

    assert len(findings) == 1
    assert findings[0].severity == "HIGH"
    assert findings[0].title == (
        "Pasta NTFS com Everyone em FullControl (Herdada)"
    )

    assert findings[0].account_name == "Everyone"
    assert findings[0].access_right == "FullControl"
    assert findings[0].access_control_type == "Allow"
    assert findings[0].is_inherited is True
from wfsa.analyzers.permissions import analyze_permissions
from wfsa.models.ntfs_permission import NtfsPermission
from wfsa.models.share import Share


def test_detect_everyone_modify_access_on_ntfs():
    share = Share(
        name="Financeiro$",
        path=r"E:\Shares\Financeiro",
        description="Financeiro",
        share_type="FileSystemDirectory",
    )

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
        share_permissions=[],
        ntfs_permissions=ntfs_permissions,
    )

    assert len(findings) == 1
    assert findings[0].severity == "HIGH"
    assert findings[0].title == "Pasta NTFS com Everyone em Modify"

    assert findings[0].account_name == "Everyone"
    assert findings[0].access_right == "Modify"
    assert findings[0].access_control_type == "Allow"
    assert findings[0].is_inherited is False
