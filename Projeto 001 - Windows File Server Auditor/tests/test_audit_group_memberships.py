from datetime import datetime

from wfsa.models.audit import AuditResult
from wfsa.models.group_membership import GroupMembership


def test_audit_result_contains_group_memberships():
    membership = GroupMembership(
        group_name="Acesso_Financeiro",
        group_sid="S-1-5-21-769638203-758265617-4166216668-1606",
        member_name="da.valentim.assis",
        member_object_type="USER",
        member_sid="S-1-5-21-769638203-758265617-4166216668-1234",
    )

    result = AuditResult(
        server="LST-FS01",
        reference_date=datetime(2026, 8, 24),
        group_memberships=[membership],
    )

    assert result.total_group_memberships == 1
    assert result.group_memberships[0].group_name == "Acesso_Financeiro"
    assert result.group_memberships[0].member_object_type == "USER"
