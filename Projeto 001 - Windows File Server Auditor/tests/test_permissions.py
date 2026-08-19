import json
from unittest.mock import patch

from wfsa.collectors.permissions import get_permissions


def test_get_permissions():
    powershell_output = json.dumps(
        [
            {
                "AccountName": "Everyone",
                "AccessControlType": "Allow",
                "AccessRight": "Read",
                "ScopeName": "Financeiro$",
            }
        ]
    )

    with patch(
        "wfsa.collectors.permissions.subprocess.run"
    ) as mock_run:
        mock_run.return_value.stdout = powershell_output

        permissions = get_permissions(
            server="lst-fs01",
            share_name="Financeiro$",
        )

    assert len(permissions) == 1

    permission = permissions[0]

    assert permission.account_name == "Everyone"
    assert permission.access_control_type == "Allow"
    assert permission.access_right == "Read"
    assert permission.scope_name == "Financeiro$"

    mock_run.assert_called_once()
