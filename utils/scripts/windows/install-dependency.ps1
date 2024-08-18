param (
    [string]$DirectoryPath,
    [string]$install_name, # e.g., "Three.js" or "Vite dependency"
    [string]$logfile,     # e.g., "install-threejs.log" or "install-vite-dependency.log"
    [string]$command       # e.g., "& { npm install --save three }" or "& { npm install --save-dev vite }"
)


. "$PSScriptRoot\common\exit-codes.ps1"
. "$PSScriptRoot\common\constants.ps1"
. "$PSScriptRoot\common\utils.ps1"

Write-Host ""
Write-Host "$PSCommandPath" -ForegroundColor Blue
Write-Host "Preparing installation for $install_name ..." -ForegroundColor White

Init-Log "$PSScriptRoot\..\..\..\logs\$logfile" | Out-Null

# Set Execution Policy
Write-Host "Setting execution policy: Set-ExecutionPolicy Bypass -Scope Process -Force"
try {
    Set-ExecutionPolicy Bypass -Scope Process -Force
} catch {
    Write-Error $_.ToString()
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
    $msg = "Node.js is required to be installed first!"
    Write-Error $msg
    $result = @{
        error = $msg
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
if (-not $DirectoryPath -or -not (Test-Path -Path $DirectoryPath -PathType Container)) {
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

Write-Host "Entering directory: $DirectoryPath"
# Change to the desired directory
try {
    Set-Location -Path $DirectoryPath
}
catch {
    Write-Error $_.ToString()
    $result = @{
        error = "Failed to access directory:"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_ACCESSING_DIRECTORY
}

$infos = @()
#Preparing to initialize your Node.js project by creating a default package.json file.
#This file will include basic information about your project and is essential for managing your project's dependencies and scripts.
Write-Host "Initializing project directory: $DirectoryPath"

try {
    $package_json = Join-Path -Path $DirectoryPath -ChildPath "package.json"
    if (-not Test-Path $package_json) {
        npm init -y
        $info += "The package.json file has been successfully created with default settings."
        Write-Host $info
        Write-Host "You can now start adding dependencies and configuring scripts for your project."
        $infos += $info
    } else {
        Write-Host "The package.json file was found: $package_json"
    }
} catch {
    Write-Error $_.ToString()
    $err = "Error initializing project directory"
    $errors = @("$err $DirectoryPath using NPM $npmVersion")
    $result = @{
        error = "${err}!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
        errors = $errors
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_INITIALIZING_NODEJS_PROJECT_DIRECTORY
}

Write-Host "Installing $install_name into directory: $DirectoryPath"
try {
    Invoke-Expression $command
    $exit_code = $LASTEXITCODE
    $nodeVersion = & node --version
    $infos += "Using node.js version $nodeVersion"
    $npmVersion = & npm --version
    $infos += "Using npm version $npmVersion"
    if ($exit_code -eq 0) {
        $infos += "Successfully installed $install_name into directory $DirectoryPath"
    } else {
        $errors = @("$install_name failed to install into directory $DirectoryPath using NPM $npmVersion")
        $result = @{
            error = "Error installing $install_name into directory!"
            exception = "Installation failed with exit code: $exit_code."
            errors = $errors
        }
        Log-Progress -message ($result | ConvertTo-Json)
        exit $ERROR_INSTALLING_DEPENDENCY_IN_DIRECTORY
    }
    $result = @{
        nodeVersion = $nodeVersion
        npmVersion = $npmVersion
        alreadyInstalled = $false
        directoryPath = $DirectoryPath
        infos = $infos
    }
    Log-Progress -message ($result | ConvertTo-Json)
} catch {
    Write-Error $_.ToString()
    $errors = @("$install_name failed to install into directory $DirectoryPath using NPM $npmVersion")
    $result = @{
        error = "Error installing $install_name into directory!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
        errors = $errors
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_INSTALLING_DEPENDENCY_IN_DIRECTORY
}

Write-Host "$install_name installation successful!" -ForegroundColor Green
exit $SUCCESS
