from wfsa.collectors.permissions import get_permissions


def test_get_permissions():
    permissions = get_permissions(
        server="lst-fs01",
        share_name="Financeiro$",
    )

    assert len(permissions) >= 1
    assert permissions[0].account_name
    assert permissions[0].access_control_type
    assert permissions[0].access_right