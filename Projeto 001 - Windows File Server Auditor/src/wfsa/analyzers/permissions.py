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

    # SMB
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

    # NTFS
    for permission in ntfs_permissions:
        if (
            permission.account_name.lower() == "everyone"
            and permission.access_control_type.lower() == "allow"
        ):
            access_right = permission.access_rights.lower()

            if access_right == "fullcontrol":
                if permission.is_inherited:
                    title = (
                        "Pasta NTFS com Everyone em FullControl "
                        "(Herdada)"
                    )
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
                    title = (
                        "Pasta NTFS com Everyone em Modify "
                        "(Herdada)"
                    )
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

    return findings
