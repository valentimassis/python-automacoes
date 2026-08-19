param(
    [Parameter(Mandatory = $true)]
    [string]$Server,

    [Parameter(Mandatory = $true)]
    [string]$Path
)

$Credential = Get-Credential

Invoke-Command -ComputerName $Server -Credential $Credential -ScriptBlock {
    param($Path)

    function ConvertTo-Base64Utf8 {
        param(
            [AllowNull()]
            [string]$Value
        )

        if ($null -eq $Value) {
            return ""
        }

        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Value)
        return [Convert]::ToBase64String($bytes)
    }

    Get-ChildItem `
        -LiteralPath $Path `
        -File `
        -Recurse `
        -ErrorAction SilentlyContinue |
        ForEach-Object {

            $creationTime = $_.CreationTime.ToString("o")
            $lastWriteTime = $_.LastWriteTime.ToString("o")
            $lastAccessTime = $_.LastAccessTime.ToString("o")

            $fields = @(
                (ConvertTo-Base64Utf8 $_.Name)
                (ConvertTo-Base64Utf8 $_.FullName)
                (ConvertTo-Base64Utf8 $_.Extension)
                ([string]$_.Length)
                (ConvertTo-Base64Utf8 $creationTime)
                (ConvertTo-Base64Utf8 $lastWriteTime)
                (ConvertTo-Base64Utf8 $lastAccessTime)
            )

            $fields -join "|"
        }

} -ArgumentList $Path