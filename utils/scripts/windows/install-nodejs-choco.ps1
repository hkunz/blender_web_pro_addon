try {
    Set-ExecutionPolicy Bypass -Scope Process -Force
} catch {
    Write-Output "0" # failure
    Write-Output "Error setting execution policy!"
    Write-Output "$_"
    return
}

# Check if Chocolatey is installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Output "0" # failure
    Write-Output "Chocolatey is not installed!"
    Write-Output "Please install it first!"
    return
}

try {
    $nodeVersion = & node --version
    Write-Output "1" # success
    Write-Output "$nodeVersion"
    Write-Output "1" # indicate already installed
    return
} catch {
}

# When you install Node.js via Chocolatey,
# it includes both the Node.js runtime and npm, which is the default package manager for Node.js.
# So after installing Node.js with this command, you should have npm available for managing Node.js packages.
try {
    choco install -y nodejs-lts
    $nodeVersion = node --version
    Write-Output "1" # success
    Write-Output $nodeVersion
    Write-Output "0" # indicates not previously installed yet
} catch {
    Write-Output "0" # failure
    Write-Output "Error installing Node.js!"
    Write-Output "$_"
}
