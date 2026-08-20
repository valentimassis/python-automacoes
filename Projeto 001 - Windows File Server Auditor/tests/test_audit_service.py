from datetime import datetime
from unittest.mock import patch

from wfsa.models.file_metadata import FileMetadata
from wfsa.services.audit import run_audit


def test_run_audit():
    files = [
        FileMetadata(
            server="lst-fs01",
            path=r"E:\Shares\Financeiro\arquivo.xlsx",
            name="arquivo.xlsx",
            extension=".xlsx",
            size=1024,
            creation_time=datetime(2020, 1, 1),
            last_write_time=datetime(2022, 1, 1),
            last_access_time=datetime(2022, 1, 1),
        )
    ]

    with patch(
        "wfsa.services.audit.get_file_metadata",
        return_value=files,
    ):
        result = run_audit(
            server="lst-fs01",
            path=r"E:\Shares\Financeiro",
            reference_date=datetime(2026, 8, 20),
        )

    assert result.server == "lst-fs01"
    assert result.reference_date.year == 2026
    assert result.total_findings == 1
    assert result.findings[0].severity == "MEDIUM"
