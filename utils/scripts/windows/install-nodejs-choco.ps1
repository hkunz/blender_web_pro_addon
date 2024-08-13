. "$PSScriptRoot\common\exit-codes.ps1"
. "$PSScriptRoot\common\constants.ps1"
. "$PSScriptRoot\common\utils.ps1"

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
        error = "Error setting execution policy!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_SETTING_EXECUTION_POLICY
}

# Check if Chocolatey is installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    $result = @{
        error = "Chocolatey is required to be installed first!"
    }
    $result | ConvertTo-Json
    exit $ERROR_CHOCOLATEY_INSTALLATION_REQUIRED
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
        nodeVersion = "$nodeVersion"
        npmVersion = "$npmVersion"
        npxVersion = "$npxVersion"
        alreadyInstalled = $true
        commandOutput = @("Node.js is already installed!$LINE_END")
    }
    $result | ConvertTo-Json
    exit $SUCCESS
} catch {
    # Proceed with installation if Node.js is not installed yet
}

try {
    #throw "Simulate Exception Test"
    # choco install -y nodejs-lts | Tee-Object -Variable commandOutput | Out-Null
    $commandOutput = @()
    $output = & { choco install -y nodejs-lts *>&1 | Out-String }
    $commandOutput += $output + $LINE_END
    $exit_code = $LASTEXITCODE
    if ($exit_code -eq 0) {
        $commandOutput += "Successfully installed Node.js$LINE_END"
    } else {
        $result = @{
            error = "Error installing Node.js!"
            exception = "Installation failed with exit code: $exit_code."
            exception_full = $commandOutput
        }
        $result | ConvertTo-Json
        exit $ERROR_INSTALLING_NODE_JS
    }
    $nodeVersion = & node --version
    $npmVersion = & npm --version
    $npxVersion = & npx --version
    $result = @{
        nodeVersion = $nodeVersion
        npmVersion = $npmVersion
        npxVersion = $npxVersion
        alreadyInstalled = $false
        commandOutput = $commandOutput
    }
    $result | ConvertTo-Json
    exit $SUCCESS
} catch {
    $result = @{
        error = "Error installing Node.js!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_INSTALLING_NODE_JS
}

exit $SUCCESS
