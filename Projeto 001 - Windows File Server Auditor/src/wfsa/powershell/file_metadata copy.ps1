param(
    [Parameter(Mandatory = $true)]
    [string]$Server,

    [Parameter(Mandatory = $true)]
    [string]$Path
)

$Credential = Get-Credential

Invoke-Command -ComputerName $Server -Credential $Credential -ScriptBlock {
    param($Path)

    Get-ChildItem `
        -LiteralPath $Path `
        -File `
        -Recurse `
        -ErrorAction SilentlyContinue |
        ForEach-Object {
            [PSCustomObject]@{
                Name           = $_.Name
                FullName       = $_.FullName
                Extension      = $_.Extension
                Length         = $_.Length
                CreationTime   = $_.CreationTime.ToString("o")
                LastWriteTime  = $_.LastWriteTime.ToString("o")
                LastAccessTime = $_.LastAccessTime.ToString("o")
            } | ConvertTo-Json -Compress
        }

} -ArgumentList $Path