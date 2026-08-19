import base64
import json
import subprocess
from pathlib import Path


script = r'''
$target = Get-ChildItem `
    -LiteralPath 'E:\Shares\Financeiro' `
    -File `
    -Recurse `
    -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Name -eq '2021-Termo de Autorização de Computador, Dispositivo móvel e Número de Celular".pdf'
    } |
    Select-Object -First 1

if ($null -eq $target) {
    Write-Output "ARQUIVO_NAO_ENCONTRADO"
    exit
}

$obj = [PSCustomObject]@{
    Name           = $target.Name
    FullName       = $target.FullName
    Extension      = $target.Extension
    Length         = $target.Length
    CreationTime   = $target.CreationTime.ToString("o")
    LastWriteTime  = $target.LastWriteTime.ToString("o")
    LastAccessTime = $target.LastAccessTime.ToString("o")
}

$json = $obj | ConvertTo-Json -Compress

$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
$base64 = [Convert]::ToBase64String($bytes)

Write-Output $base64
'''


print("Executando teste diretamente no servidor...")

encoded_script = [script]

command = [
    "powershell.exe",
    "-NoProfile",
    "-ExecutionPolicy",
    "Bypass",
    "-Command",
    f"""
    $script = @'
{script}
'@

    $encoded = [Convert]::ToBase64String(
        [System.Text.Encoding]::Unicode.GetBytes($script)
    )

    Invoke-Command -ComputerName "lst-fs01" -ScriptBlock {{
        param($RemoteScript)

        $result = Invoke-Expression $RemoteScript
        $result
    }} -ArgumentList $script
    """,
]

result = subprocess.run(
    command,
    capture_output=True,
    text=True,
    encoding="cp850",
    errors="replace",
)

print()
print("Return code:", result.returncode)
print()

print("=== STDOUT ===")
print(result.stdout)

if result.stderr:
    print()
    print("=== STDERR ===")
    print(result.stderr)