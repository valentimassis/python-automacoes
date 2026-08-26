from wfsa.collectors.active_directory import resolve_directory_identity
from wfsa.models.resolved_identity import ResolvedIdentity


class IdentityResolver:
    """Resolve identidades de ACL usando informações fornecidas pelo AD."""

    def resolve(
        self,
        account_name: str,
        *,
        identity_type: str = "UNKNOWN",
        name: str | None = None,
        sam_account_name: str | None = None,
        sid: str | None = None,
        distinguished_name: str | None = None,
    ) -> ResolvedIdentity:
        """Retorna a identidade estruturada."""

        resolved = (
            identity_type in {"USER", "GROUP"}
            and name is not None
            and sid is not None
        )

        return ResolvedIdentity(
            original_name=account_name,
            identity_type=identity_type,
            resolved=resolved,
            name=name,
            sam_account_name=sam_account_name,
            sid=sid,
            distinguished_name=distinguished_name,
        )


def resolve_identity_from_ad(account_name: str) -> ResolvedIdentity:
    """Resolve uma identidade de ACL utilizando o Active Directory."""

    directory_identity = resolve_directory_identity(account_name)

    if directory_identity is None:
        identity_type = "UNKNOWN"

        if account_name.startswith("S-1-"):
            sid = account_name
        else:
            sid = None

        return ResolvedIdentity(
            original_name=account_name,
            identity_type=identity_type,
            resolved=False,
            sid=sid,
        )

    identity_type = directory_identity.object_type

    if identity_type not in {"USER", "GROUP"}:
        identity_type = "UNKNOWN"

    return IdentityResolver().resolve(
        account_name,
        identity_type=identity_type,
        name=directory_identity.name,
        sam_account_name=directory_identity.sam_account_name,
        sid=directory_identity.sid,
        distinguished_name=directory_identity.distinguished_name,
    )
