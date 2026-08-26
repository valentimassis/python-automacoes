from wfsa.models.directory_identity import DirectoryIdentity
from wfsa.models.finding import Finding


def enrich_finding_identity(
    finding: Finding,
    identity: DirectoryIdentity | None,
) -> Finding:
    """Adiciona ao finding os dados da identidade resolvida."""

    if identity is None:
        return finding

    finding.identity_type = identity.object_type
    finding.identity_name = identity.name
    finding.identity_sid = identity.sid
    finding.identity_sam_account_name = identity.sam_account_name
    finding.identity_distinguished_name = identity.distinguished_name

    return finding
