param(
    [Parameter(Mandatory)]
    [string]$Server
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Credential = Get-Credential

Invoke-Command -ComputerName $Server -Credential $Credential -ScriptBlock {
    Get-SmbShare |
        Select-Object Name, Path, Description, @{
            Name = "ShareType"
            Expression = { $_.ShareType.ToString() }
        } |
        ConvertTo-Json
}