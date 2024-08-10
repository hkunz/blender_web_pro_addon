. "$PSScriptRoot\exit-codes.ps1"

param (
    [string]$DirectoryPath,
    [string]$AnotherArg
)

try {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    throw "Simulate Exception Test"
} catch {
    $result = @{
        error = "Error setting execution policy!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit 10
}

# Check if the directory path is provided
if (-not $DirectoryPath) {
    Write-Error "No directory path provided. Usage: .\script.ps1 -DirectoryPath 'C:\Path\To\Directory'"
    exit 1
}

# Check if the provided path is a valid directory
if (-not (Test-Path -Path $DirectoryPath -PathType Container)) {
    Write-Error "The provided path is not a valid directory: $DirectoryPath"
    exit 1
}

# Change to the desired directory
Set-Location -Path $DirectoryPath

try {
    #throw "Simulate Exception Test"
    npm install --save three | Tee-Object -Variable commandOutput | Out-Null
    $npmVersion = & node --version
    $result = @{
        npmVersion = $npmVersion
        alreadyInstalled = $false
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
    return
}

exit $SUCCESS
