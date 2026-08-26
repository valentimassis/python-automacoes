from wfsa.models.group_membership import GroupMembership


def test_create_group_membership():
    membership = GroupMembership(
        group_name="Acesso_Financeiro",
        group_sid="S-1-5-21-769638203-758265617-4166216668-1606",
        member_name="da.valentim.assis",
        member_object_type="USER",
        member_sid="S-1-5-21-769638203-758265617-4166216668-1234",
    )

    assert membership.group_name == "Acesso_Financeiro"
    assert membership.group_sid.endswith("-1606")
    assert membership.member_name == "da.valentim.assis"
    assert membership.member_object_type == "USER"
    assert membership.member_sid.endswith("-1234")
