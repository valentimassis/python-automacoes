param(
    [Parameter(Mandatory = $true)]
    [string]$Server,

    [Parameter(Mandatory = $true)]
    [string]$ShareName,

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
        param($RemoteShareName)

        Get-SmbShareAccess -Name $RemoteShareName |
            Select-Object `
                AccountName,
                @{
                    Name = "AccessControlType"
                    Expression = { $_.AccessControlType.ToString() }
                },
                @{
                    Name = "AccessRight"
                    Expression = { $_.AccessRight.ToString() }
                },
                ScopeName |
            ConvertTo-Json
    } `
    -ArgumentList $ShareName
