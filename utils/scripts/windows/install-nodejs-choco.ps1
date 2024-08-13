. "$PSScriptRoot\common\exit-codes.ps1"
. "$PSScriptRoot\common\constants.ps1"
. "$PSScriptRoot\common\utils.ps1"

$install_name = "Node.js"

Write-Host ""
Write-Host "$PSCommandPath" -ForegroundColor Blue
Write-Host "Preparing installation for $install_name ..." -ForegroundColor White

Init-Log "$PSScriptRoot\..\..\..\logs\install-nodejs-choco.log"

$TEST_FORCE_INSTALL = 1

<#
When you install Node.js via Chocolatey,
it includes npx, and both the Node.js runtime and npm, which is the default package manager for Node.js.
So after installing Node.js with this command, you should have npm available for managing Node.js packages.
#>

try {
    Write-Host "Setting execution policy: Set-ExecutionPolicy Bypass -Scope Process -Force"
    Set-ExecutionPolicy Bypass -Scope Process -Force
} catch {
    $result = @{
        error = "Error setting execution policy!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_SETTING_EXECUTION_POLICY
}

Write-Host "Checking for existing Chocolatey installation ..."
# Check if Chocolatey is installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    $result = @{
        error = "Chocolatey is required to be installed first!"
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_CHOCOLATEY_INSTALLATION_REQUIRED
} else {
    $choco_version = ""
    try {
        $choco_version = choco --version
    } catch {
        Write-Error $_.ToString()
        $result = @{
            error = "Chocolatey $choco_version is installed, but an error occurred during execution."
            exception = $_.Exception.Message
            exception_full = $_.ToString()
        }
        Log-Progress -message ($result | ConvertTo-Json)
        exit $ERROR_RUNNING_INSTALLED_CHOCOLATEY
    }
    Write-Host "Chocolatey $choco_version is already installed" -ForegroundColor Yellow
}

$nodeVersion = "Unknown Node.js version"
$npmVersion = "Unknown npm version"
$npxVersion = "Unknown npx version"

# Check if Node.js is already installed
Write-Host "Checking for existing $install_name installation ..."
try {
    if ($TEST_FORCE_INSTALL) {
        throw "Simulate Node.js not installed"
    }
    $nodeVersion = & node --version
    $npmVersion = & npm --version
    $npxVersion = & npx --version
    $result = @{
        nodeVersion = "$nodeVersion"
        npmVersion = "$npmVersion"
        npxVersion = "$npxVersion"
        alreadyInstalled = $true
        commandOutput = @("Node.js is already installed!")
    }
    Write-Host "$install_name $nodeVersion is already installed" -ForegroundColor Yellow
    Log-Progress -message ($result | ConvertTo-Json)
    exit $SUCCESS
} catch {
    # Proceed with installation if Node.js is not installed yet
}

# Start Node.js installation
Write-Host "Installing $install_name ..."
try {
    & { choco install -y nodejs-lts }
    $exit_code = $LASTEXITCODE
    if ($exit_code -ne 0) {
        Write-Error "Error installing $install_name with exit code $exit_code!"
        $result = @{
            error = "Error installing $install_name!"
            exception = "Installation failed with exit code: $exit_code."
        }
        Log-Progress -message ($result | ConvertTo-Json)
        exit $ERROR_INSTALLING_NODE_JS
    }
} catch {
    Write-Error $_.ToString()
    $result = @{
        error = "Error installing $install_name!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_INSTALLING_NODE_JS
}

# Testing installed Node.js
Write-Host "$install_name installed. Testing node --version command"
try {
    $nodeVersion = & node --version
    $npmVersion = & npm --version
    $npxVersion = & npx --version
    $result = @{
        nodeVersion = $nodeVersion
        npmVersion = $npmVersion
        npxVersion = $npxVersion
        alreadyInstalled = $false
        commandOutput = @("$install_name $nodeVersion installation successful!")
    }
} catch {
    Write-Error $_.ToString()
    $result = @{
        error = "Error executing $install_name!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_RUNNING_NODEJS_AFTER_INSTALLATION
}

Log-Progress -message ($result | ConvertTo-Json)
Write-Host "$install_name $nodeVersion installation successful!" -ForegroundColor Green
exit $SUCCESS
