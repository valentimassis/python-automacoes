import json
from unittest.mock import patch

from wfsa.collectors.active_directory import resolve_directory_identity


def test_resolve_group_from_ad():
    ad_result = {
        "Name": "Acesso_Financeiro",
        "SamAccountName": "Acesso_Financeiro",
        "ObjectType": "GROUP",
        "SID": "S-1-5-21-769638203-758265617-4166216668-1606",
        "DistinguishedName": (
            "CN=Acesso_Financeiro,"
            "OU=Grupos,DC=LST-Domain,DC=local"
        ),
    }

    with patch(
        "wfsa.collectors.active_directory.subprocess.run"
    ) as mock_run:
        mock_run.return_value.stdout = json.dumps(ad_result)

        result = resolve_directory_identity(
            r"LST-DOMAIN\Acesso_Financeiro"
        )

    assert result is not None
    assert result.object_type == "GROUP"
    assert result.name == "Acesso_Financeiro"
    assert result.sid.endswith("-1606")


def test_identity_not_found():
    with patch(
        "wfsa.collectors.active_directory.subprocess.run"
    ) as mock_run:
        mock_run.return_value.stdout = ""

        result = resolve_directory_identity(
            "S-1-5-21-769638203-758265617-4166216668-13198"
        )

    assert result is None
