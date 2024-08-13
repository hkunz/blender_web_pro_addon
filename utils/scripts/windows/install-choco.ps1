. "$PSScriptRoot\common\exit-codes.ps1"
. "$PSScriptRoot\common\constants.ps1"
. "$PSScriptRoot\common\utils.ps1"

Write-Host ""
Write-Host "$PSCommandPath" -ForegroundColor Blue
Write-Host "Preparing installation for Chocolatey ..." -ForegroundColor White

Init-Log "$PSScriptRoot\..\..\..\logs\install-choco.log"

$TEST_FORCE_INSTALL = 0

# Set Execution Policy
Write-Host "Setting execution policy: Set-ExecutionPolicy Bypass -Scope Process -Force"
try {
    Set-ExecutionPolicy Bypass -Scope Process -Force
} catch {
    $err = "Error setting execution policy!"
    Write-Error "$err"
    $result = @{
        error = $err
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_SETTING_EXECUTION_POLICY
}

try {
    Write-Host "Setting security protocol -bor 3072"
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
} catch {
    $err = "Error setting security protocol!"
    Write-Error "$err"
    $result = @{
        error = $err
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_SETTING_SECURITY_PROTOCOL
}

$install_name = "Chocolatey"
$source = "https://community.chocolatey.org/install.ps1"
$version = "Unknown Version"
$chocoPath = "Unknown Chocolatey Path"

# Check if Chocolatey is already installed
Write-Host "Checking for existing $install_name installation ..."
$output = Get-Command choco -ErrorAction SilentlyContinue
if ((Get-Command choco -ErrorAction SilentlyContinue) -and !$TEST_FORCE_INSTALL) {
    try {
        $version = choco --version
        $chocoPath = (Get-Command choco).Source
        Write-Host "$install_name $version is already installed" -ForegroundColor Yellow
    } catch {
        Write-Error $_.ToString()
        $result = @{
            error = "$install_name $version is installed, but an error occurred during execution."
            exception = $_.Exception.Message
            exception_full = $_.ToString()
        }
        Log-Progress -message ($result | ConvertTo-Json)
        exit $ERROR_RUNNING_INSTALLED_CHOCOLATEY
    }
    $result = @{
        version = $version
        alreadyInstalled = $true
        chocoPath = $chocoPath
        source = $source
        commandOutput = @("$install_name $version is already installed!")
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $SUCCESS
}

Write-Host "Ready to install $install_name ..."
try {
    & "$PSScriptRoot\install-choco-community.ps1"
    #$scriptContent = (New-Object System.Net.WebClient).DownloadString($source)
    #$output = & { iex $scriptContent *>&1 | Out-String }
} catch {
    Write-Error "Error occurred while trying to install $PSScriptRoot\install-choco-community.ps1"
    $result = @{
        error = "Error executing Chocolatey installation!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_DOWNLOADING_CHOCOLATEY
}

Write-Host "$install_name installed. Testing choco --version command"

try {
    $version = choco --version
    $chocoPath = (Get-Command choco).Source
} catch {
    Write-Error "$install_name $version is installed, but an error occurred during execution."
    $result = @{
        error = "Error executing $install_name!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_RUNNING_CHOCOLATEY_AFTER_INSTALLATION
}

Write-Host "$install_name $version installation has been verified. Upgrading using 'choco upgrade chocolatey'"

try {
    $output = & { choco upgrade chocolatey}
    $exit_code = $LASTEXITCODE
    if ($exit_code -eq 0) {
        Write-Host "$install_name upgrade to $version complete"
    } else {
        Write-Error "$install_name upgrade error"
        $result = @{
            error = "Error installing Chocolatey!"
            exception = "Installation failed with exit code: $exit_code."
            exception_full = $output
        }
        Log-Progress -message ($result | ConvertTo-Json)
        exit $ERROR_UPGRADING_CHOCOLATEY
    }
} catch {
    Write-Error $_.ToString()
    $result = @{
        error = "$install_name upgrade error!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_UPGRADING_CHOCOLATEY
}

Write-Host "$install_name $version installation successful!" -ForegroundColor Green
$result = @{
    version = $version
    alreadyInstalled = $false
    chocoPath = $chocoPath
    source = $source
    commandOutput = @("$install_name $version installation successful!")
}
Log-Progress -message ($result | ConvertTo-Json)

exit $SUCCESS
