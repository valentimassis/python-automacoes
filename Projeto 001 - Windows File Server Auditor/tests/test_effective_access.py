from wfsa.services.effective_access import calculate_effective_access


def test_effective_full_access_is_high_risk():
    result = calculate_effective_access(
        account_name="Acesso_Financeiro",
        identity_type="GROUP",
        smb_access="Full",
        ntfs_access="Modify",
    )

    assert result.account_name == "Acesso_Financeiro"
    assert result.identity_type == "GROUP"
    assert result.effective_access == "FULL"
    assert result.risk_level == "HIGH"


def test_effective_modify_access_is_medium_risk():
    result = calculate_effective_access(
        account_name="Acesso_Financeiro",
        identity_type="GROUP",
        smb_access="Change",
        ntfs_access="Modify",
    )

    assert result.effective_access == "MODIFY"
    assert result.risk_level == "MEDIUM"


def test_effective_access_without_both_layers_is_unknown():
    result = calculate_effective_access(
        account_name="Acesso_Financeiro",
        identity_type="GROUP",
        smb_access="Full",
        ntfs_access=None,
    )

    assert result.effective_access is None
    assert result.risk_level == "UNKNOWN"
