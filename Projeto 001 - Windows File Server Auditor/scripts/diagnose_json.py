import json
import subprocess
from pathlib import Path

script_path = (
    Path("src/wfsa/powershell/file_metadata.ps1").resolve()
)

command = [
    #"powershell.exe",
    "pwsh.exe",
    "-NoProfile",
    "-ExecutionPolicy",
    "Bypass",
    "-File",
    str(script_path),
    "-Server",
    "lst-fs01",
    "-Path",
    r"E:\Shares\Financeiro",
]

print("Executando coleta...")

result = subprocess.run(
    command,
    capture_output=True,
    text=True,
    encoding="cp850",
    errors="replace",
)

print("Return code:", result.returncode)
print("Linhas:", len(result.stdout.splitlines()))

for number, line in enumerate(result.stdout.splitlines(), start=1):
    line = line.strip()

    if not line:
        continue

    try:
        json.loads(line)
    except json.JSONDecodeError as error:
        print()
        print("=== JSON INVALIDO ===")
        print("Linha:", number)
        print("Erro:", error)
        print("Conteudo:")
        print(repr(line))
        print()
        break
else:
    print("Nenhuma linha JSON invalida encontrada.")

if result.stderr:
    print()
    print("=== STDERR ===")
    print(result.stderr[:5000])
