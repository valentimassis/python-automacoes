from wfsa.models.resolved_identity import ResolvedIdentity


def test_create_resolved_identity():
    identity = ResolvedIdentity(
        original_name=r"LST-DOMAIN\Acesso_Financeiro",
        identity_type="GROUP",
        resolved=True,
        name="Acesso_Financeiro",
        sam_account_name="Acesso_Financeiro",
        sid="S-1-5-21-769638203-758265617-4166216668-1606",
        distinguished_name=(
            "CN=Acesso_Financeiro,"
            "OU=Grupos,DC=LST-Domain,DC=local"
        ),
    )

    assert identity.original_name == r"LST-DOMAIN\Acesso_Financeiro"
    assert identity.identity_type == "GROUP"
    assert identity.resolved is True
    assert identity.name == "Acesso_Financeiro"
    assert identity.sam_account_name == "Acesso_Financeiro"
    assert identity.sid.endswith("-1606")


def test_create_unresolved_identity():
    identity = ResolvedIdentity(
        original_name="S-1-5-21-769638203-758265617-4166216668-13198",
        identity_type="UNKNOWN",
        resolved=False,
        sid="S-1-5-21-769638203-758265617-4166216668-13198",
    )

    assert identity.original_name.startswith("S-1-5-21-")
    assert identity.identity_type == "UNKNOWN"
    assert identity.resolved is False
