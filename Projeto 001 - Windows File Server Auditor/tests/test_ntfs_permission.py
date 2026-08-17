from wfsa.models.ntfs_permission import NtfsPermission


def test_create_ntfs_permission():
    permission = NtfsPermission(
        account_name=r"LST-DOMAIN\Financeiro",
        access_control_type="Allow",
        access_rights="Modify",
        is_inherited=True,
        inheritance_flags="ContainerInherit, ObjectInherit",
        propagation_flags="None",
    )

    assert permission.account_name == r"LST-DOMAIN\Financeiro"
    assert permission.access_control_type == "Allow"
    assert permission.access_rights == "Modify"
    assert permission.is_inherited is True
    assert permission.inheritance_flags == "ContainerInherit, ObjectInherit"
    assert permission.propagation_flags == "None"