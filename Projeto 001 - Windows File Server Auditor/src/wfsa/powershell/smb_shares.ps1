param(
    [Parameter(Mandatory = $true)]
    [string]$Server,

    [Parameter(Mandatory = $false)]
    [PSCredential]$Credential,

    [Parameter(Mandatory = $false)]
    [string]$CredentialFile
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

if ($CredentialFile) {
    $Credential = Import-Clixml -Path $CredentialFile
}

if (-not $Credential) {
    $Credential = Get-Credential
}

Invoke-Command `
    -ComputerName $Server `
    -Credential $Credential `
    -ScriptBlock {
        Get-SmbShare |
            Select-Object `
                Name,
                Path,
                Description,
                ShareType |
            ConvertTo-Json
    }
