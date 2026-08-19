import subprocess

from pathlib import Path


script_path = Path("src/wfsa/powershell/file_metadata.ps1").resolve()

command = [
    "powershell.exe",
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

lines = result.stdout.splitlines()

target = '2021-Termo de Autorização de Computador, Dispositivo móvel e Número de Celular".pdf'

for number, line in enumerate(lines, start=1):
    if target in line:
        print()
        print("=== ARQUIVO ENCONTRADO ===")
        print("Linha:", number)
        print()
        print(line)
        print()
        break
else:
    print("Arquivo não encontrado.")

print("Return code:", result.returncode)

if result.stderr:
    print()
    print("=== STDERR ===")
    print(result.stderr[:5000])