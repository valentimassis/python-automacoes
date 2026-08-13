from wfsa.models.share import Share


def test_create_share():
    share = Share(
        name="Financeiro$",
        path=r"E:\Shares\Financeiro",
        description="Financeiro",
        share_type="FileSystemDirectory",
    )

    assert share.name == "Financeiro$"
    assert share.path == r"E:\Shares\Financeiro"
    assert share.description == "Financeiro"
    assert share.share_type == "FileSystemDirectory"