try {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    # throw "Simulate Exception Test"
} catch {
    $result = @{
        success = $false
        error = "Error setting execution policy!"
        exception = $_.Exception.Message
    }
    $result | ConvertTo-Json
    return
}

try {
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
} catch {
    $result = @{
        success = $false
        error = "Error setting security protocol!"
        exception = $_.Exception.Message
    }
    $result | ConvertTo-Json
    return
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
            success = $false
            error = "Error running choco but is installed already!"
            exception = $_.Exception.Message
        }
        $result | ConvertTo-Json
        return
    }
    $result = @{
        success = $true
        version = $version
        alreadyInstalled = $true
        chocoPath = $chocoPath
        source = $source
    }
    $result | ConvertTo-Json
    return
}

try {
    $scriptContent = (New-Object System.Net.WebClient).DownloadString($source)
    iex $scriptContent
} catch {
    $result = @{
        success = $false
        error = "Error downloading/executing installation script!"
        exception = $_.Exception.Message
    }
    $result | ConvertTo-Json
    return
}

try {
    $version = choco --version
    $chocoPath = (Get-Command choco).Source
} catch {
    $result = @{
        success = $false
        error = "Error running choco after installation!"
        exception = $_.Exception.Message
    }
    $result | ConvertTo-Json
    return
}

try {
    choco upgrade chocolatey
    $result = @{
        success = $true
        version = $version
        alreadyInstalled = $false
        chocoPath = $chocoPath
        source = $source
    }
    $result | ConvertTo-Json
} catch {
    $result = @{
        success = $false
        error = "Error upgrading Chocolatey!"
        exception = $_.Exception.Message
    }
    $result | ConvertTo-Json
    return
}
