$global:LOG_FILE = $null

$global:bold = "`e[1m"
$global:reset = "`e[0m"

function Log-Progress {
    param ([string]$message)
    Add-Content -Path $global:LOG_FILE -Value $message
}

function Init-Log {
    param ([string]$LogFile)
    $global:LOG_FILE = $LogFile
    if (Test-Path -Path $LogFile -PathType Leaf) {
        $LogFile = Resolve-Path -Path $LogFile
        Clear-Content -Path $LogFile -Force
        Write-Host "Clear log file: ${LogFile}" -ForegroundColor White
    } else {
        New-Item -Path $LogFile -ItemType File -Force
        $LogFile = Resolve-Path -Path $LogFile
        Write-Host "Created log file: ${LogFile}" -ForegroundColor White
    }
    $output = Set-FilePermissions -Path $LogFile
    return $LogFile
}

function Set-FilePermissions {
    param ([string]$Path)

    # Get the ACL for the file
    $acl = Get-Acl -Path $Path
    $owner = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

    # Remove existing access rules
    $acl.SetAccessRuleProtection($true, $false) # Prevent inheritance
    $acl.Access | ForEach-Object { $acl.RemoveAccessRule($_) }

    # Define and add new access rules
    #$writeRule = New-Object System.Security.AccessControl.FileSystemAccessRule($owner, "Read,Write", "Allow")
    $writeRule = New-Object System.Security.AccessControl.FileSystemAccessRule("Everyone", "Read,Write", "Allow") # use "Everyone" instead of $owner, which doesn't allow me to delete from Ubuntu app. permission denied.
    $deleteRule = New-Object System.Security.AccessControl.FileSystemAccessRule("Everyone", "Delete", "Allow")

    $acl.AddAccessRule($writeRule)
    $acl.AddAccessRule($deleteRule)

    # Apply updated ACL
    Set-Acl -Path $Path -AclObject $acl
}

<#
function Get-ErrorOutputString {
    param (
        [Parameter(Mandatory=$true)]
        [Object[]]$output
    )
    $str_output = ""
    foreach ($item in $output) {
        if ($item.writeErrorStream -eq $true) {
            $str_output += $item.value.ToString() + "`n"
        }
    }
    return $str_output
}
#>