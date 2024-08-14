. "$PSScriptRoot\common\exit-codes.ps1"
. "$PSScriptRoot\common\constants.ps1"
. "$PSScriptRoot\common\utils.ps1"

Write-Host ""
Write-Host "$PSCommandPath" -ForegroundColor Blue
Write-Host "Preparing installation for Node Version Manager (NVM) ..." -ForegroundColor White

Init-Log "$PSScriptRoot\..\..\..\logs\install-nvm.log"

$TEST_FORCE_INSTALL = 0
$TEST_SKIP_DOWNLOAD = 0
$TEST_SKIP_EXTRACTION = 0

$nvmUrl = "https://github.com/coreybutler/nvm-windows/releases/download/1.1.9/nvm-setup.zip"
$zipPath = "nvm-setup.zip"
$installPath = "$env:USERPROFILE\nvm"
$installerPath = "$installPath\nvm-setup.exe"

$result = @{
    commandOutput = @()
    error = $null
}

<#
try {
    throw "No internet connection."
    $response = Test-Connection -ComputerName 1.1.1.1 -Count 1 -Quiet
    if (-not $response) {
        throw "No internet connection."
    }
} catch {
    $result.error = "No connection. Please check internet connection"
    $result.exception = $_.Exception.Message
    $result.exception_full = $_.ToString()
    $result | ConvertTo-Json
    exit $ERROR_GENERIC
}
#>

# Set Execution Policy
Write-Host "Setting execution policy: Set-ExecutionPolicy Bypass -Scope Process -Force"
try {
    Set-ExecutionPolicy Bypass -Scope Process -Force
} catch {
    Write-Error $_.ToString()
    $result = @{
        error = "Error setting execution policy!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_SETTING_EXECUTION_POLICY
}

# Check if Node.js is already installed
Write-Host "Checking for existing Node.js installation ..."
try {
    $node_version = & node --version
    Write-Host "Node.js $node_version is already installed" -ForegroundColor Yellow
} catch {
    Write-Error $_.ToString()
    $result = @{
        error = "Node.js is required to be installed first!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_NODE_JS_INSTALLATION_REQUIRED
}

# Check if NVM is already installed
Write-Host "Checking for existing Node Version Manager (NVM) installation ..."
try {
    if ($TEST_FORCE_INSTALL) {
        throw "Simulate NVM not installed"
    }
    $nvmVersion = & nvm version
    $result.nvmVersion = $nvmVersion
    $result.alreadyInstalled = $true
    $result.commandOutput = @("Node Version Manager (NVM) is already installed.")
    Log-Progress -message ($result | ConvertTo-Json)
    exit $SUCCESS
} catch {
    Write-Host "Node Version Manager (NVM) not installed, proceeding with installation."
}

# Download nvm-setup.zip
Write-Host "Downloading nvm-windows installer ..."
try {
    if (!$TEST_SKIP_DOWNLOAD) {
        Invoke-WebRequest -Uri $nvmUrl -OutFile $zipPath
    }
} catch {
    Write-Error $_.ToString()
    $result.error = "Failed to download nvm-windows installer: $_"
    $result.exception = $_.Exception.Message
    $result.exception_full = $_.ToString()
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_DOWNLOADING_NVM_INSTALLER
}

# Extract the installer
Write-Host "Extracting nvm-windows installer ..."
try {
    if (!$TEST_SKIP_EXTRACTION) {
        Expand-Archive -Path $zipPath -DestinationPath $installPath -Force
    }
} catch {
    Write-Error $_.ToString()
    $result.error = "Failed to extract nvm-windows installer: $_"
    $result.exception = $_.Exception.Message
    $result.exception_full = $_.ToString()
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_EXTRACTING_NVM_INSTALLER
}

$output = $null
$exit_code = 0
# Run the installer
# Extract the installer
Write-Host "Installing Node Version Manager (NVM) ..."
try {
    # FIXME: There is no way to know if the installation was exited or not.. So for now it will always say successful installation
    Start-Process -FilePath $installerPath -Wait
    $result.alreadyInstalled = $false
} catch {
    Write-Error $_.ToString()
    $result.error = "Failed to run nvm-windows installer"
    $result.exception = $_.Exception.Message
    $result.exception_full = $_.ToString()
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_RUNNING_NVM_INSTALLER
}

# Clean up
Write-Host "Cleaning installation files ..."
try {
    #Remove-Item -Path $zipPath -Force
} catch {
    Write-Error $_.ToString()
    $result.commandOutput += "Failed to clean up: $_ $LINE_END"
}

Write-Host "Testing installation with nvm version"
try {
    $nvmVersion = & nvm version
    $result.nvmVersion = $nvmVersion
    $result.alreadyInstalled = $False
} catch {
    Write-Error $_.ToString()
    $result = @{
        error = "Error installing Node Version Manager (NVM)!"
        exception = "Installation failed or was interrupted..."
        exception_full = $result.commandOutput
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_NVM_INSTALLATION_ERROR
}

Write-Host "Successfully installed Node Version Manager (NVM)" -ForegroundColor Green
Log-Progress -message ($result | ConvertTo-Json)
exit $SUCCESS
