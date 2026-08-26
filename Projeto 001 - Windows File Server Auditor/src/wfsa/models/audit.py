from dataclasses import dataclass, field
from datetime import datetime

from wfsa.models.directory_identity import DirectoryIdentity
from wfsa.models.file_metadata import FileMetadata
from wfsa.models.finding import Finding
from wfsa.models.group_membership import GroupMembership
from wfsa.models.ntfs_permission import NtfsPermission
from wfsa.models.permission import Permission
from wfsa.models.share import Share


@dataclass
class AuditResult:
    """Representa o resultado consolidado de uma auditoria."""

    server: str
    reference_date: datetime
    shares: list[Share] = field(default_factory=list)
    permissions: list[Permission] = field(default_factory=list)
    ntfs_permissions: list[NtfsPermission] = field(default_factory=list)
    identities: list[DirectoryIdentity] = field(default_factory=list)
    group_memberships: list[GroupMembership] = field(default_factory=list)
    files: list[FileMetadata] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)

    @property
    def total_findings(self) -> int:
        return len(self.findings)

    @property
    def total_shares(self) -> int:
        return len(self.shares)

    @property
    def total_permissions(self) -> int:
        return len(self.permissions)

    @property
    def total_ntfs_permissions(self) -> int:
        return len(self.ntfs_permissions)

    @property
    def total_identities(self) -> int:
        return len(self.identities)

    @property
    def total_group_memberships(self) -> int:
        return len(self.group_memberships)

    @property
    def total_files(self) -> int:
        return len(self.files)
