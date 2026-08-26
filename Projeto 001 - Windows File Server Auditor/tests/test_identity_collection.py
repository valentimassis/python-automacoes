from unittest.mock import patch

from wfsa.models.directory_identity import DirectoryIdentity
from wfsa.services.identity_collection import collect_identities


def test_collect_identities_resolves_unique_ad_accounts():
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

    with patch(
        "wfsa.services.identity_collection.resolve_directory_identity",
        return_value=identity,
    ) as mock_resolve:
        result = collect_identities(
            [
                r"LST-DOMAIN\Acesso_Financeiro",
                r"LST-DOMAIN\Acesso_Financeiro",
                "Everyone",
                r"NT AUTHORITY\SYSTEM",
                r"BUILTIN\Administrators",
            ]
        )

    assert len(result) == 1
    assert result[0].object_type == "GROUP"
    assert result[0].name == "Acesso_Financeiro"
    assert result[0].sid.endswith("-1606")
    mock_resolve.assert_called_once_with(
        r"LST-DOMAIN\Acesso_Financeiro"
    )


def test_collect_identities_ignores_unresolved_accounts():
    with patch(
        "wfsa.services.identity_collection.resolve_directory_identity",
        return_value=None,
    ):
        result = collect_identities(
            [
                r"LST-DOMAIN\Conta_Inexistente",
            ]
        )

    assert result == []
