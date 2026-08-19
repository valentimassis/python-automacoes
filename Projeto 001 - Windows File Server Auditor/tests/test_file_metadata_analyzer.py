from datetime import datetime

from wfsa.analyzers.file_metadata import analyze_old_files
from wfsa.models.file_metadata import FileMetadata


def make_file(
    last_write_time: datetime,
    last_access_time: datetime,
) -> FileMetadata:
    return FileMetadata(
        server="lst-fs01",
        path=r"E:\Shares\Financeiro\arquivo.xlsx",
        name="arquivo.xlsx",
        extension=".xlsx",
        size=1024,
        creation_time=datetime(2020, 1, 1),
        last_write_time=last_write_time,
        last_access_time=last_access_time,
    )


def test_file_old_by_write_and_access():
    files = [
        make_file(
            last_write_time=datetime(2022, 1, 1),
            last_access_time=datetime(2022, 6, 1),
        )
    ]

    findings = list(
        analyze_old_files(
            files,
            reference_date=datetime(2026, 8, 18),
        )
    )

    assert len(findings) == 1
    assert findings[0].severity == "MEDIUM"


def test_file_old_by_write_only():
    files = [
        make_file(
            last_write_time=datetime(2022, 1, 1),
            last_access_time=datetime(2026, 1, 1),
        )
    ]

    findings = list(
        analyze_old_files(
            files,
            reference_date=datetime(2026, 8, 18),
        )
    )

    assert len(findings) == 1
    assert findings[0].title == "Arquivo sem alteração há mais de 2 anos"


def test_file_old_by_access_only():
    files = [
        make_file(
            last_write_time=datetime(2026, 1, 1),
            last_access_time=datetime(2022, 1, 1),
        )
    ]

    findings = list(
        analyze_old_files(
            files,
            reference_date=datetime(2026, 8, 18),
        )
    )

    assert len(findings) == 1
    assert findings[0].title == "Arquivo sem acesso há mais de 2 anos"


def test_recent_file_has_no_finding():
    files = [
        make_file(
            last_write_time=datetime(2026, 8, 1),
            last_access_time=datetime(2026, 8, 1),
        )
    ]

    findings = list(
        analyze_old_files(
            files,
            reference_date=datetime(2026, 8, 18),
        )
    )

    assert findings == []
