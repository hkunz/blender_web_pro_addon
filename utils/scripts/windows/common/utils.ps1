$LOG_FILE = $null

function Log-Progress {
    param ([string]$message)
    Add-Content -Path $LOG_FILE -Value $message
}

function Init-Log {
    param ([string]$LogFile)
    $LOG_FILE = $LogFile
    if (Test-Path $LogFile) {
        Clear-Content -Path $LogFile -Force
    } else {
        New-Item -Path $LogFile -ItemType File -Force
    }
    Set-FilePermissions -Path $LogFile
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
    $writeRule = New-Object System.Security.AccessControl.FileSystemAccessRule($owner, "Read,Write", "Allow")
    $readRule = New-Object System.Security.AccessControl.FileSystemAccessRule("Everyone", "Read", "Allow")

    $acl.AddAccessRule($writeRule)
    $acl.AddAccessRule($readRule)

    # Apply updated ACL
    Set-Acl -Path $Path -AclObject $acl
}
