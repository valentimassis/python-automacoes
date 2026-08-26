param(
    [Parameter(Mandatory = $true)]
    [string]$Server,

    [Parameter(Mandatory = $true)]
    [string]$Path,

    [Parameter(Mandatory = $true)]
    [string]$CredentialFile
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Credential = Import-Clixml -Path $CredentialFile

Invoke-Command `
    -ComputerName $Server `
    -Credential $Credential `
    -ScriptBlock {
        param($RemotePath)

        Get-Acl -Path $RemotePath |
            Select-Object -ExpandProperty Access |
            Select-Object `
                @{
                    Name = "AccountName"
                    Expression = { $_.IdentityReference.Value }
                },
                @{
                    Name = "AccessControlType"
                    Expression = { $_.AccessControlType.ToString() }
                },
                @{
                    Name = "AccessRight"
                    Expression = { $_.FileSystemRights.ToString() }
                },
                @{
                    Name = "ScopeName"
                    Expression = { $RemotePath }
                },
                @{
                    Name = "IsInherited"
                    Expression = { $_.IsInherited }
                },
                @{
                    Name = "InheritanceFlags"
                    Expression = { $_.InheritanceFlags.ToString() }
                },
                @{
                    Name = "PropagationFlags"
                    Expression = { $_.PropagationFlags.ToString() }
                } |
            ConvertTo-Json -Depth 5

    } `
    -ArgumentList $Path
