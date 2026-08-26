from wfsa.models.finding import Finding


def create_privileged_group_finding(
    *,
    server: str,
    share_name: str,
    path: str,
    account_name: str,
    privileged_groups: list[str],
) -> Finding | None:
    """Cria um finding quando uma ACL alcança grupo privilegiado."""

    if not privileged_groups:
        return None

    groups = ", ".join(privileged_groups)

    return Finding(
        server=server,
        share_name=share_name,
        path=path,
        severity="HIGH",
        title="Acesso concedido a grupo com privilégio elevado",
        description=(
            f"A identidade '{account_name}' possui acesso neste recurso "
            f"e pertence, direta ou indiretamente, aos grupos privilegiados: "
            f"{groups}."
        ),
        account_name=account_name,
        access_right=None,
        access_control_type="Allow",
        is_inherited=None,
    )
