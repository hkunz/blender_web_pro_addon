param (
    [string]$DirectoryPath
)

. "$PSScriptRoot\exit-codes.ps1"
. "$PSScriptRoot\constants.ps1"

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

try {
    # throw "Simulate Exception Test"
    $nodeVersion = & node --version
    $npmVersion = & npm --version
} catch {
    $result = @{
        error = "No Node.js installed. You need to install it first!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_NODE_JS_INSTALLATION_REQUIRED
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
    # npm install --save-dev vite | Tee-Object -Variable commandOutput | Out-Null
    $commandOutput = @()
    $output = & { npm install --save-dev vite *>&1 | Out-String }
    $commandOutput += $output + $LINE_END
    $exit_code = $LASTEXITCODE
    $nodeVersion = & node --version
    $commandOutput += "Using node.js version $nodeVersion $LINE_END"
    $npmVersion = & npm --version
    $commandOutput += "Using npm version $npmVersion $LINE_END"
    if ($exit_code -eq 0) {
        $commandOutput += "Installed Vite dependency into directory $DirectoryPath $LINE_END"
        $commandOutput += "Successfully installed Vite dependency!$LINE_END"
    } else {
        $result = @{
            error = "Error installing Vite dependency."
            exception = "Installation failed with exit code: $exit_code."
            exception_full = $commandOutput + $LINE_END + "Vite dependency failed to install into directory $DirectoryPath $LINE_END"
        }
        $result | ConvertTo-Json
        exit $ERROR_INSTALLING_VITE_DEPENDENCY
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
        error = "Error installing Vite dependency!"
        exception = $_.Exception.Message
        exception_full = $_.ToString() + $LINE_END + "Vite dependency failed to install into directory $DirectoryPath $LINE_END"
    }
    $result | ConvertTo-Json
    exit $ERROR_INSTALLING_VITE_DEPENDENCY
}

exit $SUCCESS
