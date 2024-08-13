. "$PSScriptRoot\common\exit-codes.ps1"
. "$PSScriptRoot\common\constants.ps1"
. "$PSScriptRoot\common\utils.ps1"

Write-Host ""
Write-Host "$PSCommandPath" -ForegroundColor Green
Write-Host "Preparing installation for Chocolatey ..." -ForegroundColor Yellow

Init-Log "$PSScriptRoot\..\..\..\logs\install-choco.log"

try {
    Write-Host "Setting execution policy: Set-ExecutionPolicy Bypass -Scope Process -Force"
    Set-ExecutionPolicy Bypass -Scope Process -Force
    throw "ERROR ---"
} catch {
    msg = "Error setting execution policy!"
    Write-Error "$msg"
    $result = @{
        error = "$msg"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    Log-Progress -message ($result | ConvertTo-Json)
    exit $ERROR_SETTING_EXECUTION_POLICY
}

try {
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
} catch {
    $result = @{
        error = "Error setting security protocol!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_SETTING_SECURITY_PROTOCOL
}

$source = "https://community.chocolatey.org/install.ps1"
$version = "Unknown Version"
$chocoPath = "Unknown Chocolatey Path"
$commandOutput = @()

# Check if Chocolatey is already installed
if (Get-Command choco -ErrorAction SilentlyContinue) {
    try {
        $version = choco --version
        $chocoPath = (Get-Command choco).Source
    } catch {
        $result = @{
            error = "Error running choco but is installed already!"
            exception = $_.Exception.Message
            exception_full = $_.ToString()
        }
        $result | ConvertTo-Json
        exit $ERROR_RUNNING_INSTALLED_CHOCOLATEY
    }
    $result = @{
        version = $version
        alreadyInstalled = $true
        chocoPath = $chocoPath
        source = $source
        commandOutput = @("Chocolatey is already installed!$LINE_END")
    }
    $result | ConvertTo-Json
    exit $SUCCESS
}

try {
    #$output = & { iex (Get-Content "install-choco-community.ps1" -Raw) *>&1 | Out-String }
    $output = & "$PSScriptRoot\install-choco-community.ps1" *>&1 | Out-String
    $commandOutput += $output + $LINE_END
    #$scriptContent = (New-Object System.Net.WebClient).DownloadString($source)
    #$output = & { iex $scriptContent *>&1 | Out-String }
    #$commandOutput += $output + $LINE_END
} catch {
    $result = @{
        error = "Error downloading/executing installation script!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_DOWNLOADING_CHOCOLATEY
}

$chocoPath = "Undefined"
$version = "Undefined"
$result = $null

try {
    $version = choco --version
    $chocoPath = (Get-Command choco).Source
} catch {
    $result = @{
        error = "Error running choco after installation!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
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
        $result | ConvertTo-Json
        exit $ERROR_UPGRADING_CHOCOLATEY
    }
    $result = @{
        version = $version
        alreadyInstalled = $false
        chocoPath = $chocoPath
        source = $source
        commandOutput = $commandOutput
    }
    $result | ConvertTo-Json
} catch {
    $result = @{
        error = "Error upgrading Chocolatey!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_UPGRADING_CHOCOLATEY
}

exit $SUCCESS
