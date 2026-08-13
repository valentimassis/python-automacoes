import json

from wfsa.collectors import smb


def test_get_shares(monkeypatch):
    powershell_output = json.dumps(
        [
            {
                "Name": "Financeiro$",
                "Path": r"E:\Shares\Financeiro",
                "Description": "Financeiro",
                "ShareType": "FileSystemDirectory",
            }
        ]
    )

    class FakeResult:
        stdout = powershell_output

    def fake_run(*args, **kwargs):
        return FakeResult()

    monkeypatch.setattr(smb.subprocess, "run", fake_run)

    shares = smb.get_shares("lst-fs01")

    assert len(shares) == 1
    assert shares[0].name == "Financeiro$"
    assert shares[0].path == r"E:\Shares\Financeiro"
    assert shares[0].description == "Financeiro"
    assert shares[0].share_type == "FileSystemDirectory"