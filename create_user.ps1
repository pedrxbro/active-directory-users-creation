Param(
    [Parameter(Mandatory=$true)][string]$FullName,
    [Parameter(Mandatory=$true)][string]$SamAccountName,
    [Parameter(Mandatory=$true)][string]$OU,
    [Parameter(Mandatory=$false)][string]$Title = "",
    [Parameter(Mandatory=$false)][string]$Groups = "",
    [Parameter(Mandatory=$true)][string]$Email
)

# Log path
$logPath = 'C:\Users\adm.operator\Desktop\ad_user_creation_logs\ps_log.txt'
function Write-Log([string]$msg){
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $msg"
    Add-Content -Path $logPath -Value $line
}

Write-Log "Starting create_user.ps1 for $SamAccountName"

try {
    Import-Module ActiveDirectory -ErrorAction Stop
} catch {
    Write-Log "ERROR: Failed to import ActiveDirectory module: $_"
    Write-Output "ERROR: Failed to import ActiveDirectory module: $_"
    exit 2
}

# Split name into givenName and surname
$parts = $FullName.Trim() -split '\s+',2
$givenName = $parts[0]
$surname = if ($parts.Length -gt 1) { $parts[1] } else { "" }
Write-Log "givenName=$givenName; surname=$surname"

# Prepare password
$plainPwd = 'qwe123@'
$securePwd = ConvertTo-SecureString $plainPwd -AsPlainText -Force

try {
    Write-Log "Creating user $SamAccountName in $OU"
    New-ADUser -Name $FullName `
      -SamAccountName $SamAccountName `
      -UserPrincipalName "$SamAccountName@roderjan.com.br" `
      -DisplayName $FullName `
      -GivenName $givenName `
      -Surname $surname `
      -Path $OU `
      -AccountPassword $securePwd `
      -Enabled $true `
      -Title $Title -ErrorAction Stop

    Write-Log "New-ADUser succeeded for $SamAccountName"

    # If Email provided, set EmailAddress
    if ($Email -ne "" -and $Email -ne $null) {
        try {
            Set-ADUser -Identity $SamAccountName -EmailAddress $Email -ErrorAction Stop
            Write-Log "EmailAddress set for $($SamAccountName): $($Email)"
        } catch {
            Write-Log "WARN: Could not set EmailAddress: $($_)"
        }
    } else {
        Write-Log "WARN: No Email provided for $SamAccountName"
    }

    # Ensure password never expires
    try {
        Set-ADUser -Identity $SamAccountName -PasswordNeverExpires $true -ErrorAction Stop
        Write-Log "PasswordNeverExpires set for $SamAccountName"
    } catch {
        Write-Log "WARN: Could not set PasswordNeverExpires: $_"
    }

    # Process groups
    if ($Groups -ne "") {
        $groupList = $Groups -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' }
        foreach ($g in $groupList) {
            try {
                $grp = Get-ADGroup -Filter { Name -eq $g } -ErrorAction SilentlyContinue
                if ($grp) {
                    Add-ADGroupMember -Identity $grp -Members $SamAccountName -ErrorAction Stop
                    Write-Log "Added $SamAccountName to group $g"
                } else {
                    Write-Log "Group not found: $g"
                }
            } catch {
                Write-Log "ERROR adding to group $($g): $($_)"
            }
        }
    }

    Write-Log "Success: $SamAccountName created"
    Write-Output "SUCCESS"
    exit 0
} catch {
    Write-Log "ERROR creating user $($SamAccountName): $($_)"
    Write-Output "ERROR: $_"
    exit 1
}
