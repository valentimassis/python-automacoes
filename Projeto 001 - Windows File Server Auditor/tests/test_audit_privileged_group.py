from datetime import datetime
from unittest.mock import patch

from wfsa.models.directory_identity import DirectoryIdentity
from wfsa.models.file_metadata import FileMetadata
from wfsa.models.group_membership import GroupMembership
from wfsa.models.ntfs_permission import NtfsPermission
from wfsa.models.permission import Permission
from wfsa.models.share import Share
from wfsa.services.audit import run_audit


def test_run_audit_detects_indirect_privileged_group():
    share = Share(
        name="Financeiro$",
        path=r"E:\Shares\Financeiro",
        description="Financeiro",
        share_type="FileSystemDirectory",
    )

    permissions = [
        Permission(
            account_name="Acesso_Financeiro",
            access_control_type="Allow",
            access_right="Full",
            scope_name="*",
        )
    ]

    ntfs_permissions = [
        NtfsPermission(
            account_name="Acesso_Financeiro",
            access_control_type="Allow",
            access_rights="Modify",
            is_inherited=False,
            inheritance_flags="ContainerInherit, ObjectInherit",
            propagation_flags="None",
        )
    ]

    identity = DirectoryIdentity(
        name="Acesso_Financeiro",
        sam_account_name="Acesso_Financeiro",
        object_type="GROUP",
        sid="S-1-5-21-1606",
        distinguished_name=(
            "CN=Acesso_Financeiro,"
            "OU=Grupos,DC=LST-Domain,DC=local"
        ),
    )

    memberships = {
        "Acesso_Financeiro": [
            GroupMembership(
                group_name="Acesso_Financeiro",
                group_sid="S-1-5-21-1606",
                member_name="Financeiro_Admin",
                member_object_type="GROUP",
                member_sid="S-1-5-21-2000",
            )
        ],
        "Financeiro_Admin": [
            GroupMembership(
                group_name="Financeiro_Admin",
                group_sid="S-1-5-21-2000",
                member_name="Domain Admins",
                member_object_type="GROUP",
                member_sid="S-1-5-21-512",
            )
        ],
        "Domain Admins": [],
    }

    files = [
        FileMetadata(
            server="lst-fs01",
            path=r"E:\Shares\Financeiro\arquivo.xlsx",
            name="arquivo.xlsx",
            extension=".xlsx",
            size=1024,
            creation_time=datetime(2020, 1, 1),
            last_write_time=datetime(2026, 8, 20),
            last_access_time=datetime(2026, 8, 20),
        )
    ]

    def fake_get_group_members(group_name):
        return memberships.get(group_name, [])

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
    ), patch(
        "wfsa.services.audit.collect_identities",
        return_value=[identity],
    ), patch(
        "wfsa.services.audit.get_group_members",
        side_effect=fake_get_group_members,
    ):
        result = run_audit(
            server="lst-fs01",
            path=r"E:\Shares\Financeiro",
            reference_date=datetime(2026, 8, 24),
        )

    privileged_findings = [
        finding
        for finding in result.findings
        if finding.title
        == "Acesso concedido a grupo com privilégio elevado"
    ]

    assert len(privileged_findings) == 1
    assert privileged_findings[0].severity == "HIGH"
    assert privileged_findings[0].account_name == "Acesso_Financeiro"
    assert "Domain Admins" in privileged_findings[0].description
