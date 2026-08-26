from datetime import datetime

from wfsa.analyzers.file_metadata import analyze_old_files
from wfsa.analyzers.permissions import analyze_permissions
from wfsa.collectors.file_metadata import get_file_metadata
from wfsa.collectors.group_members import get_group_members
from wfsa.collectors.ntfs import get_ntfs_permissions
from wfsa.collectors.permissions import get_permissions
from wfsa.collectors.smb import get_shares
from wfsa.models.audit import AuditResult
from wfsa.models.group_membership import GroupMembership
from wfsa.models.permission import Permission
from wfsa.services.finding_identity import enrich_finding_identity
from wfsa.services.identity_collection import collect_identities
from wfsa.services.privileged_group_finding import create_privileged_group_finding
from wfsa.services.privileged_groups import find_privileged_groups


def run_audit(
    server: str,
    path: str,
    reference_date: datetime,
    credential_file: str | None = None,
) -> AuditResult:
    """Executa a auditoria e retorna o resultado consolidado."""

    shares = get_shares(
        server=server,
        credential_file=credential_file,
    )

    permissions: list[Permission] = []
    ntfs_permissions: list[Permission] = []
    findings = []
    account_names: list[str] = []

    permissions_by_share: dict[str, list[Permission]] = {}
    ntfs_permissions_by_share: dict[str, list[Permission]] = {}

    for share in shares:
        share_permissions = get_permissions(
            server=server,
            share_name=share.name,
            credential_file=credential_file,
        )

        share_ntfs_permissions: list[Permission] = []

        if share.path:
            share_ntfs_permissions = get_ntfs_permissions(
                server=server,
                path=share.path,
                credential_file=credential_file,
            )

        share_key = share.name.lower()

        permissions_by_share[share_key] = share_permissions
        ntfs_permissions_by_share[share_key] = share_ntfs_permissions

        permissions.extend(share_permissions)
        ntfs_permissions.extend(share_ntfs_permissions)

        account_names.extend(
            permission.account_name
            for permission in share_permissions
        )

        account_names.extend(
            permission.account_name
            for permission in share_ntfs_permissions
        )

        findings.extend(
            analyze_permissions(
                server=server,
                share=share,
                share_permissions=share_permissions,
                ntfs_permissions=share_ntfs_permissions,
            )
        )

    identities = collect_identities(account_names)

    identities_by_account = {
        identity.sam_account_name.lower(): identity
        for identity in identities
    }

    group_memberships: list[GroupMembership] = []
    collected_groups: set[str] = set()
    pending_groups: list[str] = []

    for identity in identities:
        if identity.object_type.upper() != "GROUP":
            continue

        group_name = identity.sam_account_name
        key = group_name.lower()

        if key in collected_groups:
            continue

        collected_groups.add(key)
        pending_groups.append(group_name)

    while pending_groups:
        group_name = pending_groups.pop(0)

        memberships = get_group_members(group_name)
        group_memberships.extend(memberships)

        for membership in memberships:
            if membership.member_object_type.upper() != "GROUP":
                continue

            nested_group = membership.member_name
            key = nested_group.lower()

            if key in collected_groups:
                continue

            collected_groups.add(key)
            pending_groups.append(nested_group)

    for finding in findings:
        if not finding.account_name:
            continue

        account_name = finding.account_name

        if "\\" in account_name:
            account_name = account_name.split("\\", 1)[1]

        identity = identities_by_account.get(
            account_name.lower()
        )

        enrich_finding_identity(
            finding,
            identity,
        )

    privileged_keys: set[tuple[str, str, str]] = set()

    for share in shares:
        share_key = share.name.lower()

        share_permissions = permissions_by_share.get(
            share_key,
            [],
        )

        share_ntfs_permissions = ntfs_permissions_by_share.get(
            share_key,
            [],
        )

        acl_accounts = [
            permission.account_name
            for permission in share_permissions
        ]

        acl_accounts.extend(
            permission.account_name
            for permission in share_ntfs_permissions
        )

        for raw_account_name in acl_accounts:
            account_name = raw_account_name

            if "\\" in account_name:
                account_name = account_name.split("\\", 1)[1]

            identity = identities_by_account.get(
                account_name.lower()
            )

            if identity is None:
                continue

            if identity.object_type.upper() != "GROUP":
                continue

            privileged_groups = find_privileged_groups(
                identity.sam_account_name,
                group_memberships,
            )

            if not privileged_groups:
                continue

            key = (
                share.name.lower(),
                share.path.lower(),
                identity.sam_account_name.lower(),
            )

            if key in privileged_keys:
                continue

            privileged_keys.add(key)

            privileged_finding = create_privileged_group_finding(
                server=server,
                share_name=share.name,
                path=share.path,
                account_name=raw_account_name,
                privileged_groups=privileged_groups,
            )

            if privileged_finding is not None:
                findings.append(privileged_finding)

    files = list(
        get_file_metadata(
            server=server,
            path=path,
            credential_file=credential_file,
        )
    )

    findings.extend(
        analyze_old_files(
            files=files,
            reference_date=reference_date,
        )
    )

    return AuditResult(
        server=server,
        reference_date=reference_date,
        shares=shares,
        permissions=permissions,
        ntfs_permissions=ntfs_permissions,
        identities=identities,
        group_memberships=group_memberships,
        files=files,
        findings=findings,
    )
