param(
    [Parameter(Mandatory = $true)]
    [string]$AccountName
)

Import-Module ActiveDirectory

$identity = $AccountName

if ($identity -match "\\") {
    $identity = $identity.Split("\")[-1]
}

$user = Get-ADUser `
    -Identity $identity `
    -Properties DistinguishedName `
    -ErrorAction Ignore

if ($user) {
    [PSCustomObject]@{
        Name              = $user.Name
        SamAccountName    = $user.SamAccountName
        ObjectType        = "USER"
        SID               = $user.SID.Value
        DistinguishedName = $user.DistinguishedName
    } | ConvertTo-Json -Compress

    exit
}

$group = Get-ADGroup `
    -Identity $identity `
    -Properties DistinguishedName `
    -ErrorAction Ignore

if ($group) {
    [PSCustomObject]@{
        Name              = $group.Name
        SamAccountName    = $group.SamAccountName
        ObjectType        = "GROUP"
        SID               = $group.SID.Value
        DistinguishedName = $group.DistinguishedName
    } | ConvertTo-Json -Compress

    exit
}
