param(
    [Parameter(Mandatory = $true)]
    [string]$Server,

    [Parameter(Mandatory = $true)]
    [string]$Path
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Credential = Get-Credential

Invoke-Command -ComputerName $Server -Credential $Credential -ScriptBlock {
    param($Path)

    Get-Acl $Path |
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
                Name = "AccessRights"
                Expression = { $_.FileSystemRights.ToString() }
            },
            IsInherited,
            @{
                Name = "InheritanceFlags"
                Expression = { $_.InheritanceFlags.ToString() }
            },
            @{
                Name = "PropagationFlags"
                Expression = { $_.PropagationFlags.ToString() }
            } |
        ConvertTo-Json
} -ArgumentList $Path