. "$PSScriptRoot\exit-codes.ps1"

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
        commandOutput = @("Chocolatey is already installed!")
    }
    $result | ConvertTo-Json
    exit $SUCCESS
}

try {
    $scriptContent = (New-Object System.Net.WebClient).DownloadString($source)
    iex $scriptContent
} catch {
    $result = @{
        error = "Error downloading/executing installation script!"
        exception = $_.Exception.Message
        exception_full = $_.ToString()
    }
    $result | ConvertTo-Json
    exit $ERROR_DOWNLOADING_CHOCOLATEY
}

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
    choco upgrade chocolatey
    $result = @{
        version = $version
        alreadyInstalled = $false
        chocoPath = $chocoPath
        source = $source
        commandOutput = @("Successfully installed Chocolatey!")
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
