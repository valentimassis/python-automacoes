from wfsa.models.group_membership import GroupMembership


PRIVILEGED_GROUPS = {
    "domain admins",
    "enterprise admins",
    "administrators",
    "schema admins",
    "account operators",
    "server operators",
    "backup operators",
}


def is_privileged_group(group_name: str) -> bool:
    """Indica se um grupo é considerado privilegiado."""

    return group_name.strip().lower() in PRIVILEGED_GROUPS


def find_privileged_groups(
    group_name: str,
    memberships: list[GroupMembership],
) -> list[str]:
    """Encontra grupos privilegiados alcançáveis a partir de um grupo."""

    by_group: dict[str, list[GroupMembership]] = {}

    for membership in memberships:
        key = membership.group_name.strip().lower()
        by_group.setdefault(key, []).append(membership)

    privileged: list[str] = []
    visited: set[str] = set()

    def visit(current_group: str) -> None:
        key = current_group.strip().lower()

        if key in visited:
            return

        visited.add(key)

        if is_privileged_group(current_group):
            if current_group not in privileged:
                privileged.append(current_group)
            return

        for membership in by_group.get(key, []):
            if membership.member_object_type.upper() == "GROUP":
                visit(membership.member_name)

    visit(group_name)

    return privileged
