from datetime import datetime
from unittest.mock import patch

from wfsa.models.directory_identity import DirectoryIdentity
from wfsa.models.group_membership import GroupMembership
from wfsa.models.share import Share
from wfsa.services.audit import run_audit


def test_run_audit_collects_group_memberships():
    share = Share(
        name="Financeiro",
        path=r"E:\Shares\Financeiro",
        description="",
        share_type="Disk",
    )

    identity = DirectoryIdentity(
        name="Acesso_Financeiro",
        sam_account_name="Acesso_Financeiro",
        object_type="GROUP",
        sid="S-1-5-21-769638203-758265617-4166216668-1606",
        distinguished_name=(
            "CN=Acesso_Financeiro,"
            "OU=Grupos,DC=LST-Domain,DC=local"
        ),
    )

    membership = GroupMembership(
        group_name="Acesso_Financeiro",
        group_sid="S-1-5-21-769638203-758265617-4166216668-1606",
        member_name="da.valentim.assis",
        member_object_type="USER",
        member_sid="S-1-5-21-769638203-758265617-4166216668-1234",
    )

    with (
        patch(
            "wfsa.services.audit.get_shares",
            return_value=[share],
        ),
        patch(
            "wfsa.services.audit.get_permissions",
            return_value=[],
        ),
        patch(
            "wfsa.services.audit.get_ntfs_permissions",
            return_value=[],
        ),
        patch(
            "wfsa.services.audit.get_file_metadata",
            return_value=[],
        ),
        patch(
            "wfsa.services.audit.collect_identities",
            return_value=[identity],
        ),
        patch(
            "wfsa.services.audit.get_group_members",
            return_value=[membership],
        ),
    ):
        result = run_audit(
            server="LST-FS01",
            path=r"E:\Shares",
            reference_date=datetime(2026, 8, 24),
        )

    assert result.total_identities == 1
    assert result.total_group_memberships == 1

    assert (
        result.group_memberships[0].group_name
        == "Acesso_Financeiro"
    )

    assert (
        result.group_memberships[0].member_name
        == "da.valentim.assis"
    )

    assert (
        result.group_memberships[0].member_object_type
        == "USER"
    )
