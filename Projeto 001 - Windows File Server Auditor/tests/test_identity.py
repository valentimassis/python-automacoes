from wfsa.services.identity import IdentityResolver


def test_resolve_group():
    resolver = IdentityResolver()

    identity = resolver.resolve(
        r"LST-DOMAIN\Acesso_Financeiro",
        identity_type="GROUP",
        name="Acesso_Financeiro",
        sam_account_name="Acesso_Financeiro",
        sid="S-1-5-21-769638203-758265617-4166216668-1606",
        distinguished_name=(
            "CN=Acesso_Financeiro,"
            "OU=Grupos,DC=LST-Domain,DC=local"
        ),
    )

    assert identity.resolved is True
    assert identity.identity_type == "GROUP"
    assert identity.name == "Acesso_Financeiro"
    assert identity.sid.endswith("-1606")


def test_unresolved_sid():
    resolver = IdentityResolver()

    identity = resolver.resolve(
        "S-1-5-21-769638203-758265617-4166216668-13198",
        identity_type="UNKNOWN",
        sid="S-1-5-21-769638203-758265617-4166216668-13198",
    )

    assert identity.resolved is False
    assert identity.identity_type == "UNKNOWN"
    assert identity.sid.endswith("-13198")


def test_system_identity_is_not_ad_identity():
    resolver = IdentityResolver()

    identity = resolver.resolve(
        r"NT AUTHORITY\SYSTEM",
        identity_type="SYSTEM",
    )

    assert identity.resolved is False
    assert identity.identity_type == "SYSTEM"


def test_builtin_identity_is_not_ad_identity():
    resolver = IdentityResolver()

    identity = resolver.resolve(
        r"BUILTIN\Administrators",
        identity_type="BUILTIN",
    )

    assert identity.resolved is False
    assert identity.identity_type == "BUILTIN"
