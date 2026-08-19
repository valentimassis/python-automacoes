from datetime import datetime

from wfsa.models.file_metadata import FileMetadata


def test_create_file_metadata():
    metadata = FileMetadata(
        server="lst-fs01",
        path=r"E:\Shares\Financeiro\relatorio.xlsx",
        name="relatorio.xlsx",
        extension=".xlsx",
        size=1024,
        creation_time=datetime(2020, 1, 1),
        last_write_time=datetime(2022, 1, 1),
        last_access_time=datetime(2022, 6, 1),
    )

    assert metadata.server == "lst-fs01"
    assert metadata.name == "relatorio.xlsx"
    assert metadata.extension == ".xlsx"
    assert metadata.size == 1024
