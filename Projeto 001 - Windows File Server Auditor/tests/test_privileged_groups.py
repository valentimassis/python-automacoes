from wfsa.models.group_membership import GroupMembership
from wfsa.services.privileged_groups import (
    find_privileged_groups,
    is_privileged_group,
)


def test_domain_admins_is_privileged():
    assert is_privileged_group("Domain Admins") is True


def test_enterprise_admins_is_privileged():
    assert is_privileged_group("Enterprise Admins") is True


def test_administrators_is_privileged():
    assert is_privileged_group("Administrators") is True


def test_regular_group_is_not_privileged():
    assert is_privileged_group("Acesso_Financeiro") is False


def test_comparison_is_case_insensitive():
    assert is_privileged_group("DOMAIN ADMINS") is True


def test_comparison_ignores_whitespace():
    assert is_privileged_group("  Domain Admins  ") is True


def test_find_direct_privileged_group():
    memberships = [
        GroupMembership(
            group_name="Acesso_Financeiro",
            group_sid="GROUP-1",
            member_name="Domain Admins",
            member_object_type="GROUP",
            member_sid="GROUP-ADMIN",
        )
    ]

    result = find_privileged_groups(
        "Acesso_Financeiro",
        memberships,
    )

    assert result == ["Domain Admins"]


def test_find_nested_privileged_group():
    memberships = [
        GroupMembership(
            group_name="Acesso_Financeiro",
            group_sid="GROUP-1",
            member_name="Financeiro_Admin",
            member_object_type="GROUP",
            member_sid="GROUP-2",
        ),
        GroupMembership(
            group_name="Financeiro_Admin",
            group_sid="GROUP-2",
            member_name="Domain Admins",
            member_object_type="GROUP",
            member_sid="GROUP-ADMIN",
        ),
    ]

    result = find_privileged_groups(
        "Acesso_Financeiro",
        memberships,
    )

    assert result == ["Domain Admins"]


def test_no_privileged_group_returns_empty_list():
    memberships = [
        GroupMembership(
            group_name="Acesso_Financeiro",
            group_sid="GROUP-1",
            member_name="Financeiro_Usuarios",
            member_object_type="GROUP",
            member_sid="GROUP-2",
        )
    ]

    result = find_privileged_groups(
        "Acesso_Financeiro",
        memberships,
    )

    assert result == []


def test_group_cycle_does_not_loop_forever():
    memberships = [
        GroupMembership(
            group_name="Grupo_A",
            group_sid="GROUP-A",
            member_name="Grupo_B",
            member_object_type="GROUP",
            member_sid="GROUP-B",
        ),
        GroupMembership(
            group_name="Grupo_B",
            group_sid="GROUP-B",
            member_name="Grupo_A",
            member_object_type="GROUP",
            member_sid="GROUP-A",
        ),
    ]

    result = find_privileged_groups(
        "Grupo_A",
        memberships,
    )

    assert result == []
