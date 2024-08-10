param (
    [string]$DirectoryPath,
    [string]$AnotherArg
)

. "$PSScriptRoot\exit-codes.ps1"

try {
    Set-ExecutionPolicy Bypass -Scope Process -Force
} catch {
    $result = @{
        error = "Error setting execution policy!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_SETTING_EXECUTION_POLICY
}

# Check if the directory path is provided
if (-not $DirectoryPath) {
    $result = @{
        error = "No directory path provided!"
    }
    $result | ConvertTo-Json
    exit $ERROR_NO_DIRECTORY_PATH_PROVIDED
}

# Check if the provided path is a valid directory
if (-not (Test-Path -Path $DirectoryPath -PathType Container)) {
    $result = @{
        error = "The provided path is not a valid directory:"
        exception = "$DirectoryPath"
        exception_full = "The provided path is not a valid directory: $DirectoryPath"
    }
    $result | ConvertTo-Json
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
    npm install --save three | Tee-Object -Variable commandOutput | Out-Null
    $npmVersion = & node --version
    $result = @{
        npmVersion = $npmVersion
        alreadyInstalled = $false
        directoryPath = $DirectoryPath
        commandOutput = $commandOutput
    }
    $result | ConvertTo-Json
} catch {
    $result = @{
        error = "Error installing Three.js!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_INSTALLING_THREE_JS
}

exit $SUCCESS
