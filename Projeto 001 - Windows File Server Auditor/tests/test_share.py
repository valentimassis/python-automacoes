from wfsa.models.share import Share


def test_create_share():
    share = Share(
        name="Financeiro$",
        path=r"E:\Shares\Financeiro",
        protocol="SMB",
        clustered=False,
    )

    assert share.name == "Financeiro$"
    assert share.path == r"E:\Shares\Financeiro"
    assert share.protocol == "SMB"
    assert share.clustered is False