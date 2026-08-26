from wfsa.services.effective_access import calculate_effective_access


def test_write_and_full_is_full():
    result = calculate_effective_access(
        account_name="Acesso_Financeiro",
        identity_type="GROUP",
        smb_access="Write",
        ntfs_access="Full",
    )

    assert result.effective_access == "FULL"
    assert result.risk_level == "HIGH"


def test_full_and_write_is_full():
    result = calculate_effective_access(
        account_name="Acesso_Financeiro",
        identity_type="GROUP",
        smb_access="Full",
        ntfs_access="Write",
    )

    assert result.effective_access == "FULL"
    assert result.risk_level == "HIGH"


def test_read_execute_and_full_is_full():
    result = calculate_effective_access(
        account_name="Acesso_Financeiro",
        identity_type="GROUP",
        smb_access="Read_Execute",
        ntfs_access="Full",
    )

    assert result.effective_access == "FULL"
    assert result.risk_level == "HIGH"


def test_full_and_read_execute_is_full():
    result = calculate_effective_access(
        account_name="Acesso_Financeiro",
        identity_type="GROUP",
        smb_access="Full",
        ntfs_access="Read_Execute",
    )

    assert result.effective_access == "FULL"
    assert result.risk_level == "HIGH"


def test_modify_and_write_is_modify():
    result = calculate_effective_access(
        account_name="Acesso_Financeiro",
        identity_type="GROUP",
        smb_access="Modify",
        ntfs_access="Write",
    )

    assert result.effective_access == "MODIFY"
    assert result.risk_level == "MEDIUM"


def test_write_and_modify_is_modify():
    result = calculate_effective_access(
        account_name="Acesso_Financeiro",
        identity_type="GROUP",
        smb_access="Write",
        ntfs_access="Modify",
    )

    assert result.effective_access == "MODIFY"
    assert result.risk_level == "MEDIUM"
