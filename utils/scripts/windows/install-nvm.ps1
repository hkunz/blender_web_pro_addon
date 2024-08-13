. "$PSScriptRoot\common\exit-codes.ps1"
. "$PSScriptRoot\common\constants.ps1"
. "$PSScriptRoot\common\utils.ps1"

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

try {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    # throw "Simulate Exception Test"
} catch {
    $result = @{
        error = "Error setting execution policy!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_SETTING_EXECUTION_POLICY
}

try {
    # throw "Simulate Exception Test"
    $npmVersion = & npm --version
} catch {
    $result = @{
        error = "No Node.js installed. You need to install it first!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_NODE_JS_INSTALLATION_REQUIRED
}

# Check if NVM is already installed
try {
    # throw "Simulate Exception Test"
    $nvmVersion = & nvm version
    $result.nvmVersion = $nvmVersion
    $result.alreadyInstalled = $true
    $result.commandOutput += "Node Version Manager (nvm) is already installed.$LINE_END"
    $result | ConvertTo-Json
    exit $SUCCESS
} catch {
    $result.commandOutput += "NVM not installed, proceeding with installation.$LINE_END"
}

# Download nvm-setup.zip
try {
    $result.commandOutput += "Downloading nvm-windows installer...$LINE_END"
    Invoke-WebRequest -Uri $nvmUrl -OutFile $zipPath
} catch {
    $result.error = "Failed to download nvm-windows installer: $_"
    $result.exception = $_.Exception.Message
    $result.exception_full = $_.ToString()
    $result | ConvertTo-Json
    exit $ERROR_DOWNLOADING_NVM_INSTALLER
}

# Extract the installer
try {
    $result.commandOutput += "Extracting nvm-windows installer...$LINE_END"
    Expand-Archive -Path $zipPath -DestinationPath $installPath -Force
} catch {
    $result.error = "Failed to extract nvm-windows installer: $_"
    $result.exception = $_.Exception.Message
    $result.exception_full = $_.ToString()
    $result | ConvertTo-Json
    exit $ERROR_EXTRACTING_NVM_INSTALLER
}

$output = $null
$exit_code = 0
# Run the installer
try {
    $result.commandOutput += "Running the nvm-windows installer...$LINE_END"
    $output = Start-Process -FilePath $installerPath -Wait | Tee-Object -Variable installOutput | Out-Null
    $result.commandOutput += $installOutput.StandardOutput + $LINE_END
    $result.alreadyInstalled = $false
    $result.commandOutput += $output + $LINE_END
} catch {
    $result.error = "Failed to run nvm-windows installer"
    $result.exception = $_.Exception.Message
    $result.exception_full = $_.ToString()
    $result | ConvertTo-Json
    exit $ERROR_RUNNING_NVM_INSTALLER
}

# Clean up
try {
    $result.commandOutput += "Cleaning up...$LINE_END"
    #Remove-Item -Path $zipPath -Force
} catch {
    $result.commandOutput += "Failed to clean up: $_ $LINE_END"
}

try {
    $nvmVersion = & nvm version
    $result.nvmVersion = $nvmVersion
    $result.alreadyInstalled = $False
    $result.commandOutput += "Node Version Manager (nvm) is installed.$LINE_END"
    $result | ConvertTo-Json
    exit $SUCCESS
} catch {
    $result = @{
        error = "Error installing NVM!"
        exception = "Installation failed or was interrupted..."
        exception_full = $result.commandOutput
    }
    $result | ConvertTo-Json
    exit $ERROR_NVM_INSTALLATION_ERROR
}

$result.commandOutput += "Successfully installed NVM (Node Version Manager)$LINE_END"

$result | ConvertTo-Json
exit $SUCCESS
