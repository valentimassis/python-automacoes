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
                )
            )

    return findings