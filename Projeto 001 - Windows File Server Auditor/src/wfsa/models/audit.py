from dataclasses import dataclass, field
from datetime import datetime

from wfsa.models.file_metadata import FileMetadata
from wfsa.models.finding import Finding
from wfsa.models.share import Share


@dataclass
class AuditResult:
    """Representa o resultado consolidado de uma auditoria."""

    server: str
    reference_date: datetime
    shares: list[Share] = field(default_factory=list)
    files: list[FileMetadata] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)

    @property
    def total_findings(self) -> int:
        """Retorna a quantidade total de findings."""
        return len(self.findings)

    @property
    def total_shares(self) -> int:
        """Retorna a quantidade de compartilhamentos encontrados."""
        return len(self.shares)

    @property
    def total_files(self) -> int:
        """Retorna a quantidade total de arquivos coletados."""
        return len(self.files)
