$nvmUrl = "https://github.com/coreybutler/nvm-windows/releases/download/1.1.9/nvm-setup.zip"
$zipPath = "nvm-setup.zip"
$installPath = "$env:USERPROFILE\nvm"
$installerPath = "$installPath\nvm-setup.exe"

$result = @{
    success = $true
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
    return
}
#>

# Check if NVM is already installed
try {
    # throw "Simulate Exception Test"
    $nvmVersion = & nvm version
    $result.nvmVersion = $nvmVersion
    $result.alreadyInstalled = $true
    $result.commandOutput += "Node Version Manager (nvm) is already installed."
    $result | ConvertTo-Json
    return
} catch {
    $result.commandOutput += "NVM not installed, proceeding with installation."
}

# Download nvm-setup.zip
try {
    $result.commandOutput += "Downloading nvm-windows installer..."
    Invoke-WebRequest -Uri $nvmUrl -OutFile $zipPath
} catch {
    $result.success = $false
    $result.error = "Failed to download nvm-windows installer: $_"
    $result.exception = $_.Exception.Message
    $result.exception_full = $_.ToString()
    $result | ConvertTo-Json
    return
}

# Extract the installer
try {
    $result.commandOutput += "Extracting nvm-windows installer..."
    Expand-Archive -Path $zipPath -DestinationPath $installPath -Force
} catch {
    $result.success = $false
    $result.error = "Failed to extract nvm-windows installer: $_"
    $result.exception = $_.Exception.Message
    $result.exception_full = $_.ToString()
    $result | ConvertTo-Json
    return
}

# Run the installer
try {
    $result.commandOutput += "Running the nvm-windows installer..."
    $installOutput = Start-Process -FilePath $installerPath -Wait -PassThru | Tee-Object -Variable installOutput | Out-Null
    $result.commandOutput += $installOutput.StandardOutput
    $result.alreadyInstalled = $false
} catch {
    $result.success = $false
    $result.error = "Failed to run nvm-windows installer"
    $result.exception = $_.Exception.Message
    $result.exception_full = $_.ToString()
    $result | ConvertTo-Json
    return
}

# Clean up
try {
    $result.commandOutput += "Cleaning up..."
    Remove-Item -Path $zipPath -Force
} catch {
    $result.commandOutput += "Failed to clean up: $_"
}

# Final success message
if ($result.success) {
    $result.commandOutput += "nvm-windows installation completed."
}

$result | ConvertTo-Json
