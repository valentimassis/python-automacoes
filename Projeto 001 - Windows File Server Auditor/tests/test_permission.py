from wfsa.models.permission import Permission


def test_create_permission():
    permission = Permission(
        account_name="Everyone",
        access_control_type="Allow",
        access_right="Full",
        scope_name="*",
    )

    assert permission.account_name == "Everyone"
    assert permission.access_control_type == "Allow"
    assert permission.access_right == "Full"
    assert permission.scope_name == "*"