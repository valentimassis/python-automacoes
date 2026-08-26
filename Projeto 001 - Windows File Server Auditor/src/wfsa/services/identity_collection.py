from wfsa.collectors.active_directory import resolve_directory_identity
from wfsa.models.directory_identity import DirectoryIdentity


def collect_identities(
    account_names: list[str],
) -> list[DirectoryIdentity]:
    """Resolve identidades de ACL no Active Directory."""

    identities: list[DirectoryIdentity] = []
    seen: set[str] = set()

    for account_name in account_names:
        normalized = account_name.strip()

        if not normalized:
            continue

        key = normalized.lower()

        if key in seen:
            continue

        seen.add(key)

        if (
            normalized.lower().startswith("nt authority\\")
            or normalized.lower().startswith("builtin\\")
            or normalized.lower() == "everyone"
        ):
            continue

        identity = resolve_directory_identity(normalized)

        if identity is not None:
            identities.append(identity)

    return identities
