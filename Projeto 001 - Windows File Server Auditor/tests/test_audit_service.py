from datetime import datetime
from unittest.mock import patch

from wfsa.models.file_metadata import FileMetadata
from wfsa.models.ntfs_permission import NtfsPermission
from wfsa.models.permission import Permission
from wfsa.models.share import Share
from wfsa.services.audit import run_audit


def test_run_audit():
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

    files = [
        FileMetadata(
            server="lst-fs01",
            path=r"E:\Shares\Financeiro\arquivo.xlsx",
            name="arquivo.xlsx",
            extension=".xlsx",
            size=1024,
            creation_time=datetime(2020, 1, 1),
            last_write_time=datetime(2022, 1, 1),
            last_access_time=datetime(2022, 1, 1),
        )
    ]

    with patch(
        "wfsa.services.audit.get_shares",
        return_value=[share],
    ), patch(
        "wfsa.services.audit.get_permissions",
        return_value=permissions,
    ), patch(
        "wfsa.services.audit.get_ntfs_permissions",
        return_value=ntfs_permissions,
    ), patch(
        "wfsa.services.audit.get_file_metadata",
        return_value=files,
    ):
        result = run_audit(
            server="lst-fs01",
            path=r"E:\Shares\Financeiro",
            reference_date=datetime(2026, 8, 20),
        )

    assert result.server == "lst-fs01"
    assert result.reference_date.year == 2026

    assert result.total_shares == 1
    assert result.total_permissions == 1
    assert result.total_ntfs_permissions == 1
    assert result.total_files == 1

    assert result.total_findings == 2

    assert result.findings[0].severity == "HIGH"
    assert result.findings[0].title == "Acesso efetivo elevado para Everyone"

    assert result.findings[1].severity == "MEDIUM"
    assert result.findings[1].title == "Arquivo sem alteração e acesso há mais de 2 anos"


    assert result.shares[0].name == "Financeiro$"
    assert result.permissions[0].account_name == "Everyone"
    assert result.ntfs_permissions[0].account_name == "Everyone"
    assert result.files[0].name == "arquivo.xlsx"
