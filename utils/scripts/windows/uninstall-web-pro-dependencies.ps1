. "$PSScriptRoot\exit-codes.ps1"
. "$PSScriptRoot\constants.ps1"

$commandOutput = @()
$no_choco_installed=$False # assume chocolatey is installed

# Check if Chocolatey is installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    $commandOutput += "Chocolatey is not installed." + $NEW_LINE
    $result = @{
        no_choco_installed = $True
        commandOutput = $commandOutput
    }
    $result | ConvertTo-Json
    exit $SUCCESS
}

# Uninstall chocolatey packages
try {
    $output = & { choco uninstall all -y *>&1 | Out-String }
    $commandOutput += $output + $NEW_LINE
} catch {
    $result = @{
        error = "Error uninstalling Chocolatey packages"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_UNINSTALLING_CHOCOLATEY_PACKAGES
}

try {
     $output = & { Remove-Item -Recurse -Force C:\ProgramData\chocolatey *>&1 | Out-String }
     $commandOutput += $output + $NEW_LINE
} catch {
    $result = @{
        error = "Error removing Chocolatey"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_UNINSTALLING_CHOCOLATEY_REMOVE_DIR
}

# Try removing any other folders related to Chocolatey but just output warnings when failed
try {
    $output = & { Remove-Item -Recurse -Force C:\ProgramData\ChocolateyHttpCache *>&1 | Out-String }
    $commandOutput += "Removed directories related to chocolatey." + $NEW_LINE
} catch {
    # Do nothing
}

# Clean up environment variables
try {
    [System.Environment]::SetEnvironmentVariable("ChocolateyInstall", $null, [System.EnvironmentVariableTarget]::Machine)
    [System.Environment]::SetEnvironmentVariable("ChocolateyHome", $null, [System.EnvironmentVariableTarget]::Machine)
    $commandOutput += "Removed environment variables related to Chocolatey" + $NEW_LINE
} catch {
    $result = @{
        error = "Error cleaning up environment variables."
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_UNINSTALLING_CHOCOLATEY
}

$commandOutput += "Successfully uninstalled Chocolatey!$NEW_LINE"
$result = @{
    no_choco_installed = $False
    commandOutput = $commandOutput
}
$result | ConvertTo-Json
exit $SUCCESS