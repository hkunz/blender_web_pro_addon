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

$nodeVersion = "Unknown nodejs version"
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
