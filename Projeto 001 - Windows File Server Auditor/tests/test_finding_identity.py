from wfsa.models.directory_identity import DirectoryIdentity
from wfsa.models.finding import Finding
from wfsa.services.finding_identity import enrich_finding_identity


def test_enrich_finding_with_directory_identity():
    finding = Finding(
        server="LST-FS01",
        share_name="Financeiro",
        path=r"E:\Shares\Financeiro",
        severity="HIGH",
        title="Permissão elevada",
        description="Permissão elevada identificada.",
        account_name=r"LST-DOMAIN\Acesso_Financeiro",
        access_right="Modify",
        access_control_type="Allow",
    )

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

    result = enrich_finding_identity(
        finding,
        identity,
    )

    assert result.identity_type == "GROUP"
    assert result.identity_name == "Acesso_Financeiro"
    assert result.identity_sid.endswith("-1606")
    assert result.identity_sam_account_name == "Acesso_Financeiro"
    assert "CN=Acesso_Financeiro" in result.identity_distinguished_name
