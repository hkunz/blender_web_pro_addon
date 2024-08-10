<#
When you install Node.js via Chocolatey,
it includes npx, and both the Node.js runtime and npm, which is the default package manager for Node.js.
So after installing Node.js with this command, you should have npm available for managing Node.js packages.
#>

try {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    # throw "Simulate Exception Test"
} catch {
    $result = @{
        success = $false
        error = "Error setting execution policy!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    return
}

# Check if Chocolatey is installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    $result = @{
        success = $false
        error = "Chocolatey is not installed!"
        exception = "Chocolatey is required to be installed first!"
        exception_full = "Chocolatey is not installed. Chocolatey is required to be installed first."
    }
    $result | ConvertTo-Json
    return
}

$nodeVersion = "Unknown Node.js version"
$npmVersion = "Unknown npm version"
$npxVersion = "Unknown npx version"

try {
    #throw "Simulate Exception Test"
    $nodeVersion = & node --version
    $npmVersion = & npm --version
    $npxVersion = & npx --version
    $result = @{
        success = $true
        nodeVersion = "$nodeVersion"
        npmVersion = "$npmVersion"
        npxVersion = "$npxVersion"
        alreadyInstalled = $true
        commandOutput = @("Node.js is already installed!")
    }
    $result | ConvertTo-Json
    return
} catch {
    # Proceed with installation if Node.js is not installed yet
}

try {
    #throw "Simulate Exception Test"
    choco install -y nodejs-lts | Tee-Object -Variable commandOutput | Out-Null
    $nodeVersion = & node --version
    $npmVersion = & npm --version
    $npxVersion = & npx --version
    $result = @{
        success = $true
        nodeVersion = $nodeVersion
        npmVersion = $npmVersion
        npxVersion = $npxVersion
        alreadyInstalled = $false
        commandOutput = $commandOutput
    }
    $result | ConvertTo-Json
} catch {
    $result = @{
        success = $false
        error = "Error installing Node.js!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    return
}
