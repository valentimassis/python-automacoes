from datetime import datetime

from wfsa.models.audit import AuditResult
from wfsa.models.directory_identity import DirectoryIdentity


def test_audit_result_contains_directory_identities():
    identity = DirectoryIdentity(
        name="Acesso_Financeiro",
        sam_account_name="Acesso_Financeiro",
        object_type="GROUP",
        sid="S-1-5-21-769638203-758265617-4166216668-1606",
        distinguished_name=(
            "CN=Acesso_Financeiro,"
            "OU=Grupos,DC=LST-Domain,DC=local"
        ),
    )

    result = AuditResult(
        server="LST-FS01",
        reference_date=datetime(2026, 8, 24),
        identities=[identity],
    )

    assert result.total_identities == 1
    assert result.identities[0].name == "Acesso_Financeiro"
    assert result.identities[0].object_type == "GROUP"
