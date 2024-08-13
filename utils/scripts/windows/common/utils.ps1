function Log-Progress {
    param ([string]$message)
    Add-Content -Path $logFile -Value $message
}

function Init-Log {
    if (Test-Path $logFile) {
        Clear-Content -Path $logFile -Force
    } else {
        New-Item -Path $logFile -ItemType File -Force
    }
}
