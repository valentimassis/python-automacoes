from wfsa.analyzers.access import calculate_effective_access
from wfsa.models.finding import Finding
from wfsa.models.ntfs_permission import NtfsPermission
from wfsa.models.permission import Permission
from wfsa.models.share import Share


def analyze_permissions(
    server: str,
    share: Share,
    share_permissions: list[Permission],
    ntfs_permissions: list[NtfsPermission],
) -> list[Finding]:
    """Analisa permissões SMB e NTFS e retorna riscos encontrados."""

    findings: list[Finding] = []

    # ---------------------------------------------------------
    # 1. Análise individual das permissões SMB
    # ---------------------------------------------------------
    for permission in share_permissions:
        if (
            permission.account_name.lower() == "everyone"
            and permission.access_control_type.lower() == "allow"
            and permission.access_right.lower() == "full"
        ):
            findings.append(
                Finding(
                    server=server,
                    share_name=share.name,
                    path=share.path,
                    severity="HIGH",
                    title="Share SMB com Everyone em Full",
                    description=(
                        "O compartilhamento SMB concede acesso Full "
                        "para Everyone."
                    ),
                    account_name=permission.account_name,
                    access_right=permission.access_right,
                    access_control_type=permission.access_control_type,
                    is_inherited=None,
                )
            )

    # ---------------------------------------------------------
    # 2. Análise individual das permissões NTFS
    # ---------------------------------------------------------
    for permission in ntfs_permissions:
        if (
            permission.account_name.lower() != "everyone"
            or permission.access_control_type.lower() != "allow"
        ):
            continue

        access_right = permission.access_rights.lower()

        if access_right == "fullcontrol":
            if permission.is_inherited:
                title = "Pasta NTFS com Everyone em FullControl (Herdada)"
                description = (
                    "A pasta possui uma permissão NTFS herdada que "
                    "concede FullControl para Everyone."
                )
            else:
                title = "Pasta NTFS com Everyone em FullControl"
                description = (
                    "A pasta possui uma permissão NTFS explícita que "
                    "concede FullControl para Everyone."
                )

            findings.append(
                Finding(
                    server=server,
                    share_name=share.name,
                    path=share.path,
                    severity="HIGH",
                    title=title,
                    description=description,
                    account_name=permission.account_name,
                    access_right=permission.access_rights,
                    access_control_type=permission.access_control_type,
                    is_inherited=permission.is_inherited,
                )
            )

        elif access_right == "modify":
            if permission.is_inherited:
                title = "Pasta NTFS com Everyone em Modify (Herdada)"
                description = (
                    "A pasta possui uma permissão NTFS herdada que "
                    "concede Modify para Everyone."
                )
            else:
                title = "Pasta NTFS com Everyone em Modify"
                description = (
                    "A pasta possui uma permissão NTFS explícita que "
                    "concede Modify para Everyone."
                )

            findings.append(
                Finding(
                    server=server,
                    share_name=share.name,
                    path=share.path,
                    severity="HIGH",
                    title=title,
                    description=description,
                    account_name=permission.account_name,
                    access_right=permission.access_rights,
                    access_control_type=permission.access_control_type,
                    is_inherited=permission.is_inherited,
                )
            )

    # ---------------------------------------------------------
    # 3. Acesso efetivo SMB + NTFS
    #
    # Só calcula quando existe uma permissão Everyone Allow
    # nos dois níveis.
    #
    # Exemplo:
    # SMB   = Full
    # NTFS  = Modify
    # Efetivo = Modify
    # ---------------------------------------------------------
    smb_everyone = next(
        (
            permission
            for permission in share_permissions
            if (
                permission.account_name.lower() == "everyone"
                and permission.access_control_type.lower() == "allow"
            )
        ),
        None,
    )

    ntfs_everyone = next(
        (
            permission
            for permission in ntfs_permissions
            if (
                permission.account_name.lower() == "everyone"
                and permission.access_control_type.lower() == "allow"
            )
        ),
        None,
    )

    if smb_everyone and ntfs_everyone:
        effective_access = calculate_effective_access(
            smb_right=smb_everyone.access_right,
            ntfs_right=ntfs_everyone.access_rights,
        )

        # O finding individual de SMB Full + NTFS Modify já existe.
        # Neste cenário, substituímos os dois findings individuais
        # por um único finding de acesso efetivo.
        if effective_access == "MODIFY":
            findings = [
                finding
                for finding in findings
                if not (
                    finding.account_name
                    and finding.account_name.lower() == "everyone"
                    and finding.share_name == share.name
                )
            ]

            findings.append(
                Finding(
                    server=server,
                    share_name=share.name,
                    path=share.path,
                    severity="HIGH",
                    title="Acesso efetivo elevado para Everyone",
                    description=(
                        "A combinação das permissões SMB e NTFS resulta "
                        "em acesso efetivo Modify para Everyone."
                    ),
                    account_name="Everyone",
                    access_right=effective_access,
                    access_control_type="Allow",
                    is_inherited=ntfs_everyone.is_inherited,
                )
            )

    return findings
