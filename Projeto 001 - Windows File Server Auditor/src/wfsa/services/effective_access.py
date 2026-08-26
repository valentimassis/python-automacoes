from wfsa.models.effective_access import EffectiveAccess


def calculate_effective_access(
    *,
    account_name: str,
    identity_type: str,
    smb_access: str | None,
    ntfs_access: str | None,
) -> EffectiveAccess:
    """Calcula uma representação inicial do acesso efetivo."""

    if smb_access is None or ntfs_access is None:
        return EffectiveAccess(
            account_name=account_name,
            identity_type=identity_type,
            smb_access=smb_access,
            ntfs_access=ntfs_access,
            effective_access=None,
            risk_level="UNKNOWN",
        )

    if smb_access.lower() == "full":
        effective_access = "FULL"
    elif smb_access.lower() in {"change", "modify"}:
        effective_access = "MODIFY"
    else:
        effective_access = smb_access.upper()

    if ntfs_access.lower() == "full":
        effective_access = "FULL"
    elif ntfs_access.lower() in {"modify", "write"} and effective_access != "FULL":
        effective_access = "MODIFY"

    if effective_access == "FULL":
        risk_level = "HIGH"
    elif effective_access == "MODIFY":
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return EffectiveAccess(
        account_name=account_name,
        identity_type=identity_type,
        smb_access=smb_access,
        ntfs_access=ntfs_access,
        effective_access=effective_access,
        risk_level=risk_level,
    )
