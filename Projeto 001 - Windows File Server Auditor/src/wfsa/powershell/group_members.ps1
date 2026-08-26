param(
    [Parameter(Mandatory = $true)]
    [string]$GroupName
)

Import-Module ActiveDirectory

$group = Get-ADGroup `
    -Identity $GroupName `
    -Properties SID, SamAccountName

Get-ADGroupMember `
    -Identity $group `
    -Recursive |
    ForEach-Object {
        $object = Get-ADObject `
            -Identity $_.DistinguishedName `
            -Properties objectSid, objectClass, SamAccountName

        [PSCustomObject]@{
            GroupName = $group.Name
            GroupSID = $group.SID.Value
            MemberName = $_.Name
            MemberObjectType = if ($_.objectClass -eq "group") { "GROUP" } else { "USER" }
            MemberSID = $object.objectSid.Value
        }
    } |
    ConvertTo-Json -Depth 5
