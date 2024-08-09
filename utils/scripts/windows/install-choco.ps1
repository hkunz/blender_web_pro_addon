# Set execution policy and adjust security protocols
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072

# Check if Chocolatey is already installed
if (Get-Command choco -ErrorAction SilentlyContinue) {
    $version = choco --version
    $chocoPath = (Get-Command choco).Source
    Write-Output "1"           # Indicate success
    Write-Output "$version"    # Output the version
    Write-Output "1"           # Indicate already installed
    Write-Output $chocoPath
    return
}

# If Chocolatey is not installed, install it
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Get the version after installation
$version = choco --version
$chocoPath = (Get-Command choco).Source

# Upgrade Chocolatey to the latest version
choco upgrade chocolatey

# Output success and version
Write-Output "1"           # Indicate success
Write-Output "$version"    # Output the version
Write-Output "1"           # Indicate already installed
Write-Output $chocoPath