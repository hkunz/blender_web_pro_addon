$nvmUrl = "https://github.com/coreybutler/nvm-windows/releases/download/1.1.9/nvm-setup.zip"
$zipPath = "nvm-setup.zip"
$installPath = "$env:USERPROFILE\nvm"
$installerPath = "$installPath\nvm-setup.exe"

# Download nvm-setup.zip
Write-Output "Downloading nvm-windows installer..."
Invoke-WebRequest -Uri $nvmUrl -OutFile $zipPath

# Extract the installer
Write-Output "Extracting nvm-windows installer..."
Expand-Archive -Path $zipPath -DestinationPath $installPath -Force

# Run the installer
Write-Output "Running the nvm-windows installer..."
Start-Process -FilePath $installerPath -Wait

# Clean up
Write-Output "Cleaning up..."
Remove-Item -Path $zipPath -Force
Write-Output "nvm-windows installation completed."
