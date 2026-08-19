import base64
from unittest.mock import patch

from wfsa.collectors.file_metadata import get_file_metadata


def b64(value: str) -> str:
    return base64.b64encode(
        value.encode("utf-8")
    ).decode("ascii")


def test_get_file_metadata():
    name = "relatorio.xlsx"
    path = r"E:\Shares\Financeiro\relatorio.xlsx"
    extension = ".xlsx"
    creation_time = "2020-01-01T00:00:00"
    last_write_time = "2022-01-01T00:00:00"
    last_access_time = "2022-06-01T00:00:00"

    powershell_output = "|".join(
        [
            b64(name),
            b64(path),
            b64(extension),
            "1024",
            b64(creation_time),
            b64(last_write_time),
            b64(last_access_time),
        ]
    )

    with patch("wfsa.collectors.file_metadata.subprocess.run") as mock_run:
        mock_run.return_value.stdout = powershell_output

        result = list(
            get_file_metadata(
                "lst-fs01",
                r"E:\Shares\Financeiro",
            )
        )

    assert len(result) == 1

    metadata = result[0]

    assert metadata.server == "lst-fs01"
    assert metadata.path == path
    assert metadata.name == name
    assert metadata.extension == extension
    assert metadata.size == 1024
    assert metadata.creation_time.year == 2020
    assert metadata.last_write_time.year == 2022
    assert metadata.last_access_time.year == 2022

    mock_run.assert_called_once()
