param (
    [string]$DirectoryPath,
    [string]$AnotherArg
)

. "$PSScriptRoot\common\exit-codes.ps1"
. "$PSScriptRoot\common\constants.ps1"
. "$PSScriptRoot\common\utils.ps1"

$install_name = "Three.js"

Write-Host ""
Write-Host "$PSCommandPath" -ForegroundColor Blue
Write-Host "Preparing installation for $install_name ..." -ForegroundColor White

$log_file = Init-Log "$PSScriptRoot\..\..\..\logs\install-threejs.log"
Write-Host "Log file ===: $log_file"

# Set Execution Policy
Write-Host "Setting execution policy: Set-ExecutionPolicy Bypass -Scope Process -Force"
try {
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

# Check if Node.js is already installed
Write-Host "Checking for existing Node.js installation ..."
try {
    $node_version = & node --version
    Write-Host "Node.js $node_version is already installed" -ForegroundColor Yellow
} catch {
    Write-Error $_.ToString()
    $result = @{
        error = "Node.js is required to be installed first!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_NODE_JS_INSTALLATION_REQUIRED
}

# Check if the directory path is provided
Write-Host "Using directory: $DirectoryPath"
if (-not $DirectoryPath) {
    $msg = "No directory path provided!"
    Write-Error "$msg"
    $result = @{
        error = $msg
        errors = @($msg)
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_NO_DIRECTORY_PATH_PROVIDED
}

# Check if the provided path is a valid directory
Write-Host "Checking if directory is valid path: $DirectoryPath"
if (-not (Test-Path -Path $DirectoryPath -PathType Container)) {
    $msg = "The provided path is not a valid directory:"
    Write-Error "$msg"
    $result = @{
        error = $msg
        exception = "$DirectoryPath"
        exception_full = "${msg}: $DirectoryPath"
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_INVALID_DIRECTORY_PATH
}

# Change to the desired directory
try {
    Set-Location -Path $DirectoryPath
}
catch {
    $result = @{
        error = "Failed setting directory"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_ACCESSING_DIRECTORY
}


try {
    # throw "Simulate Exception Test"
    # npm install --save three | Tee-Object -Variable commandOutput | Out-Null
    # $commandOutput = npm install --save three 2>&1
    $commandOutput = @()
    $output = & { npm install --save three *>&1 | Out-String }
    $commandOutput += $output + $LINE_END
    $exit_code = $LASTEXITCODE
    $nodeVersion = & node --version
    $commandOutput += "Using node.js version $nodeVersion $LINE_END"
    $npmVersion = & npm --version
    $commandOutput += "Using npm version $npmVersion $LINE_END"
    if ($exit_code -eq 0) {
        $commandOutput += "Installed Three.js into directory $DirectoryPath $LINE_END"
        $commandOutput += "Successfully installed Three.js!$LINE_END"
    } else {
        $result = @{
            error = "Error installing Three.js."
            exception = "Installation failed with exit code: $exit_code."
            exception_full = $commandOutput + $LINE_END + "Three.js failed to install into directory $DirectoryPath $LINE_END"
        }
        $result | ConvertTo-Json
        exit $ERROR_INSTALLING_THREE_JS
    }
    $result = @{
        nodeVersion = $nodeVersion
        npmVersion = $npmVersion
        alreadyInstalled = $false
        directoryPath = $DirectoryPath
        commandOutput = $commandOutput
    }
    $result | ConvertTo-Json
} catch {
    $result = @{
        error = "Error installing Three.js into!"
        exception = $_.Exception.Message
        exception_full = $_.ToString() + $LINE_END + "Three.js failed to install into directory $DirectoryPath $LINE_END"
    }
    $result | ConvertTo-Json
    exit $ERROR_INSTALLING_THREE_JS
}

exit $SUCCESS
