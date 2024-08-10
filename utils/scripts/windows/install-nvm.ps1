. "$PSScriptRoot\exit-codes.ps1"

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
    exit 1
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
    exit 10
}

# Check if NVM is already installed
try {
    # throw "Simulate Exception Test"
    $nvmVersion = & nvm version
    $result.nvmVersion = $nvmVersion
    $result.alreadyInstalled = $true
    $result.commandOutput += "Node Version Manager (nvm) is already installed."
    $result | ConvertTo-Json
    exit $SUCCESS
} catch {
    $result.commandOutput += "NVM not installed, proceeding with installation."
}

# Download nvm-setup.zip
try {
    $result.commandOutput += "Downloading nvm-windows installer..."
    Invoke-WebRequest -Uri $nvmUrl -OutFile $zipPath
} catch {
    $result.error = "Failed to download nvm-windows installer: $_"
    $result.exception = $_.Exception.Message
    $result.exception_full = $_.ToString()
    $result | ConvertTo-Json
    exit 18
}

# Extract the installer
try {
    $result.commandOutput += "Extracting nvm-windows installer..."
    Expand-Archive -Path $zipPath -DestinationPath $installPath -Force
} catch {
    $result.error = "Failed to extract nvm-windows installer: $_"
    $result.exception = $_.Exception.Message
    $result.exception_full = $_.ToString()
    $result | ConvertTo-Json
    exit 19
}

# Run the installer
try {
    $result.commandOutput += "Running the nvm-windows installer..."
    $installOutput = Start-Process -FilePath $installerPath -Wait -PassThru | Tee-Object -Variable installOutput | Out-Null
    $result.commandOutput += $installOutput.StandardOutput
    $result.alreadyInstalled = $false
} catch {
    $result.error = "Failed to run nvm-windows installer"
    $result.exception = $_.Exception.Message
    $result.exception_full = $_.ToString()
    $result | ConvertTo-Json
    exit 20
}

# Clean up
try {
    $result.commandOutput += "Cleaning up..."
    Remove-Item -Path $zipPath -Force
} catch {
    $result.commandOutput += "Failed to clean up: $_"
}

$result.commandOutput += "nvm-windows installation completed."

$result | ConvertTo-Json
exit $SUCCESS
