import json
from unittest.mock import patch

from wfsa.collectors.group_members import get_group_members


def test_get_group_members():
    ad_result = [
        {
            "GroupName": "Acesso_Financeiro",
            "GroupSID": (
                "S-1-5-21-769638203-758265617-4166216668-1606"
            ),
            "MemberName": "da.valentim.assis",
            "MemberObjectType": "USER",
            "MemberSID": (
                "S-1-5-21-769638203-758265617-4166216668-1234"
            ),
        },
        {
            "GroupName": "Acesso_Financeiro",
            "GroupSID": (
                "S-1-5-21-769638203-758265617-4166216668-1606"
            ),
            "MemberName": "Financeiro_Admin",
            "MemberObjectType": "GROUP",
            "MemberSID": (
                "S-1-5-21-769638203-758265617-4166216668-2000"
            ),
        },
    ]

    with patch(
        "wfsa.collectors.group_members.subprocess.run"
    ) as mock_run:
        mock_run.return_value.stdout = json.dumps(ad_result)

        result = get_group_members("Acesso_Financeiro")

    assert len(result) == 2

    assert result[0].group_name == "Acesso_Financeiro"
    assert result[0].member_name == "da.valentim.assis"
    assert result[0].member_object_type == "USER"

    assert result[1].member_name == "Financeiro_Admin"
    assert result[1].member_object_type == "GROUP"
