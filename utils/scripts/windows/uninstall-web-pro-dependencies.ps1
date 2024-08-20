. "$PSScriptRoot\common\exit-codes.ps1"
. "$PSScriptRoot\common\utils.ps1"

$install_name = "Chocolatey"
$version = ""
$infos = @()
$no_choco_installed=$False # assume chocolatey is installed

Write-Host ""
Write-Host "$PSCommandPath" -ForegroundColor Blue
Write-Host "Preparing for uninstallation of $install_name and related packages ..." -ForegroundColor White

Init-Log "$PSScriptRoot\..\..\..\logs\uninstall-web-pro-dependencies.log" | Out-Null

$CHOCO_UNINSTALLED_TEST = 0
$TEST_FAKE_UNINSTALL = 0


# Set Execution Policy
Write-Host "Setting execution policy: Set-ExecutionPolicy Bypass -Scope Process -Force"
try {
    Set-ExecutionPolicy Bypass -Scope Process -Force
} catch {
    $err = "Error setting execution policy!"
    Write-Error $_.ToString()
    Write-Error "$err"
    $result = @{
        error = $err
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_SETTING_EXECUTION_POLICY
}

# Set security protocol
Write-Host "Setting security protocol -bor 3072"
try {
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
} catch {
    $err = "Error setting security protocol!"
    Write-Error $_.ToString()
    Write-Error "$err"
    $result = @{
        error = $err
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_SETTING_SECURITY_PROTOCOL
}

# Check if Chocolatey is already installed
Write-Host "Checking for existing $install_name installation ..."
if (-not (Get-Command choco -ErrorAction SilentlyContinue) -or $CHOCO_UNINSTALLED_TEST) {
    $infos += "Chocolatey is not installed."
    $result = @{
        no_choco_installed = $True
        infos = $infos
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $SUCCESS
}

# Uninstall chocolatey packages
Write-Host "Uninstalling $install_name packages ..."
try {
    $version = choco --version
    if (!$TEST_FAKE_UNINSTALL) {
        $output = & { choco uninstall all -y }
    }
} catch {
    $err = "Error uninstalling Chocolatey packages"
    Write-Error $_.ToString()
    $result = @{
        error = $err
        exception = $_.Exception.Message
        exception_full = $_.ToString()
        errors = @($err)
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_UNINSTALLING_CHOCOLATEY_PACKAGES
}

Write-Host "Uninstalling $install_name $version ..."
$choco_path = "C:\ProgramData\chocolatey"
try {
    if (!$TEST_FAKE_UNINSTALL) {
        $output = & { Remove-Item -Recurse -Force $choco_path }
    }
} catch {
    Write-Error $_.ToString()
    $err = "Error removing Chocolatey $version"
    $result = @{
        error = $err
        exception = $_.Exception.Message
        exception_full = $_.ToString()
        errors = @("${err}: ${choco_path}")
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_UNINSTALLING_CHOCOLATEY_REMOVE_DIR
}

# Try removing any other folders related to Chocolatey but just output warnings when failed
Write-Host "Removing directories related to $install_name $version ..."
try {
    if (!$TEST_FAKE_UNINSTALL) {
        $output = & { Remove-Item -Recurse -Force C:\ProgramData\ChocolateyHttpCache }
    }
    $infos += "Removed directories related to chocolatey $version."
} catch {
    # Do nothing
}

# Clean up environment variables
Write-Host "Cleaning up environment variables related to $install_name $version ..."
try {
    if (!$TEST_FAKE_UNINSTALL) {
        [System.Environment]::SetEnvironmentVariable("ChocolateyInstall", $null, [System.EnvironmentVariableTarget]::Machine)
        [System.Environment]::SetEnvironmentVariable("ChocolateyHome", $null, [System.EnvironmentVariableTarget]::Machine)
    }
    $infos += "Removed environment variables related to Chocolatey $version"
} catch {
    Write-Error $_.ToString()
    $err = "Error cleaning $install_name $version environment variables"
    $result = @{
        error = $err
        exception = $_.Exception.Message
        exception_full = $_.ToString()
        errors = @($err)
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_UNINSTALLING_CHOCOLATEY
}

$infos += "Successfully uninstalled $install_name $version!"
$result = @{
    no_choco_installed = $False
    infos = $infos
}
Log-Progress -message ($result | ConvertTo-Json)
exit $SUCCESS
