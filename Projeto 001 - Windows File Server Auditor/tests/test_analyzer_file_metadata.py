from datetime import datetime

from wfsa.analyzer import analyze_files
from wfsa.models.file_metadata import FileMetadata


def test_analyze_files_finds_old_file():
    file = FileMetadata(
        server="lst-fs01",
        path=r"E:\Shares\Financeiro\arquivo.xlsx",
        name="arquivo.xlsx",
        extension=".xlsx",
        size=1024,
        creation_time=datetime(2020, 1, 1),
        last_write_time=datetime(2022, 1, 1),
        last_access_time=datetime(2022, 6, 1),
    )

    findings = list(
        analyze_files(
            files=[file],
            reference_date=datetime(2026, 8, 18),
        )
    )

    assert len(findings) == 1
    assert findings[0].server == "lst-fs01"
    assert findings[0].path == r"E:\Shares\Financeiro\arquivo.xlsx"
