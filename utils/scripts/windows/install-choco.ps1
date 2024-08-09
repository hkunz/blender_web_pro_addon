try {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    # throw "This is a test exception!"
} catch {
    Write-Output "0" # failure
    Write-Output "Error setting execution policy!"
    Write-Output "$_"
    return
}

try {
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
} catch {
    Write-Output "0" # failure
    Write-Output "Error setting security protocol!"
    Write-Output "$_"
    return
}

$source = "https://community.chocolatey.org/install.ps1"

# Check if Chocolatey is already installed
if (Get-Command choco -ErrorAction SilentlyContinue) {
    $version = choco --version
    $chocoPath = (Get-Command choco).Source
    Write-Output "1" # success
    Write-Output "$version"
    Write-Output "1" # indicate already installed
    Write-Output $chocoPath
    Write-Output $source
    return
}

try {
    $scriptContent = (New-Object System.Net.WebClient).DownloadString($source)
    iex $scriptContent
} catch {
    Write-Output "0" # failure
    Write-Output "Error downloading/executing installation script!"
    Write-Output "$_"
    return
}

$version = choco --version
$chocoPath = (Get-Command choco).Source

try {
    choco upgrade chocolatey
    Write-Output "1" # success
    Write-Output "$version"
    Write-Output "0" # indicate not already installed
    Write-Output $chocoPath
    Write-Output $source
} catch {
    Write-Output "0" # failure
    Write-Output "Error upgrading Chocolatey!"
    Write-Output "$_"
}