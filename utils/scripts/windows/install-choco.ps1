. "$PSScriptRoot\common\exit-codes.ps1"
. "$PSScriptRoot\common\constants.ps1"
. "$PSScriptRoot\common\utils.ps1"

Write-Host ""
Write-Host "$PSCommandPath" -ForegroundColor Green
Write-Host "Preparing installation for Chocolatey ..." -ForegroundColor Yellow

Init-Log "$PSScriptRoot\..\..\..\logs\install-choco.log"

$TEST_FORCE_INSTALL = 1

try {
    Write-Host "Setting execution policy: Set-ExecutionPolicy Bypass -Scope Process -Force"
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
            $msg = "$install_name $version is installed, but an error occurred during execution."
            error = $msg
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
    #$commandOutput += $output + $LINE_END
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

try {
    $output = & { choco upgrade chocolatey 2>&1 | Out-String }
    $commandOutput += $output + $LINE_END
    $exit_code = $LASTEXITCODE
    if ($exit_code -eq 0) {
        $commandOutput += "Successfully installed Chocolatey$LINE_END"
    } else {
        $result = @{
            error = "Error installing Chocolatey!"
            exception = "Installation failed with exit code: $exit_code."
            exception_full = $commandOutput
        }
        Log-Progress -message ($result | ConvertTo-Json)
        exit $ERROR_UPGRADING_CHOCOLATEY
    }
    $result = @{
        version = $version
        alreadyInstalled = $false
        chocoPath = $chocoPath
        source = $source
        commandOutput = $commandOutput
    }
    Log-Progress -message ($result | ConvertTo-Json)
} catch {
    $result = @{
        error = "Error upgrading Chocolatey!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_UPGRADING_CHOCOLATEY
}

exit $SUCCESS
