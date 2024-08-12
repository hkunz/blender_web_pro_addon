. "$PSScriptRoot\exit-codes.ps1"
. "$PSScriptRoot\constants.ps1"

# Check if Chocolatey is installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    $result = @{
        error = "Chocolatey is not installed."
    }
    $result | ConvertTo-Json
    exit $SUCCESS
}

try {
    # List installed packages
    $installedPackages = choco list --local-only

    if ($installedPackages) {
        # Uninstall all packages
        $installedPackages | ForEach-Object {
            if ($_ -notmatch "Chocolatey") {
                $packageName = $_.Split(' ')[0]
                try {
                    choco uninstall $packageName --yes *>&1 | Out-String
                } catch {
                    $result = @{
                        error = "Error uninstalling package: $packageName"
                        exception = $_.Exception.Message
                        exception_full = $_.ToString()
                    }
                    $result | ConvertTo-Json
                    exit $ERROR_UNINSTALLING_CHOCOLATEY
                }
            }
        }
    }

    # Uninstall Chocolatey
    try {
        choco uninstall chocolatey --yes *>&1 | Out-String
        $result = @{
            success = "Chocolatey has been uninstalled successfully."
        }
        $result | ConvertTo-Json
    } catch {
        $result = @{
            error = "Error uninstalling Chocolatey."
            exception = $_.Exception.Message
            exception_full = $_.ToString()
        }
        $result | ConvertTo-Json
        exit $ERROR_UNINSTALLING_CHOCOLATEY
    }

    # Clean up environment variables
    try {
        [System.Environment]::SetEnvironmentVariable("ChocolateyInstall", $null, [System.EnvironmentVariableTarget]::Machine)
        [System.Environment]::SetEnvironmentVariable("ChocolateyHome", $null, [System.EnvironmentVariableTarget]::Machine)
    } catch {
        $result = @{
            error = "Error cleaning up environment variables."
            exception = $_.Exception.Message
            exception_full = $_.ToString()
        }
        $result | ConvertTo-Json
        exit $ERROR_UNINSTALLING_CHOCOLATEY
    }

    exit $SUCCESS

} catch {
    $result = @{
        error = "An unexpected error occurred."
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_UNINSTALLING_CHOCOLATEY
}
