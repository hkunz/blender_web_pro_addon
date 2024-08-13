. "$PSScriptRoot\common\utils.ps1"

$NOT_INSTALLED = 0
$INSTALLED = 1
$INSTALLATION_ERROR = 2

$result = @{
    choco = $NOT_INSTALLED
    node = $NOT_INSTALLED
    npm = $NOT_INSTALLED
    npx = $NOT_INSTALLED
    nvm = $NOT_INSTALLED

    choco_version = ""
    node_version = ""
    npm_version = ""
    npx_version = ""
    nvm_version = ""

    commandOutput = @()
}

Init-Log

# Check if Chocolatey is already installed
if (Get-Command choco -ErrorAction SilentlyContinue) {
    try {
        $choco_version = & choco --version
        $result.choco = $INSTALLED # Choco installed successfully
        $result.choco_version = $choco_version
        $result.commandOutput += "Chocolatey $choco_version is installed!"
    } catch {
        $result.choco = $INSTALLATION_ERROR # Error running choco but is installed already!
        $result.commandOutput += "Chocolatey is installed but error in execution!"
    }
} else {
    $result.commandOutput += "Chocolatey is not installed"
}

# Check if Node.js is already installed
if (Get-Command node -ErrorAction SilentlyContinue) {
    try {
        $node_version = & node --version
        $result.node = $INSTALLED # Node.js installed successfully
        $result.node_version = $node_version
        #$result.npm = $NOT_INSTALLED # testing
        $result.commandOutput += "Node.js $node_version is installed!"
    } catch {
        $result.node = $INSTALLATION_ERROR # Error running node but is installed already!
        $result.commandOutput += "Node.js is installed but error in execution!"
    }
} else {
    $result.commandOutput += "Node.js is not installed"
}

# Check if npm is already installed
if (Get-Command npm -ErrorAction SilentlyContinue) {
    try {
        $npm_version = & npm --version
        $result.npm = $INSTALLED # npm installed successfully
        $result.npm_version = $npm_version
        $result.commandOutput += "NPM $npm_version is installed!"
    } catch {
        $result.npm = $INSTALLATION_ERROR # Error running npm but is installed already!
        $result.commandOutput += "NPM is installed but error in execution!"
    }
} else {
    $result.commandOutput += "NPM is not installed!"
}

# Check if npx is already installed
if (Get-Command npx -ErrorAction SilentlyContinue) {
    try {
        $npx_version = & npx --version
        $result.npx = $INSTALLED # npx installed successfully
        $result.npx_version = $npx_version
        $result.commandOutput += "NPX $npx_version is installed!"
    } catch {
        $result.npx = $INSTALLATION_ERROR # Error running npx but is installed already!
        $result.commandOutput += "NPX is installed but error in execution!"
    }
} else {
    $result.commandOutput += "NPX is not installed!"
}

if ($result.node -eq $INSTALLED) {
    if ($result.npm -ne $INSTALLED) {
        $result.node = $INSTALLATION_ERROR
        $result.commandOutput += "Node.js is installed but there is a problem with NPM!"
    }
    if ($result.npx -ne $INSTALLED) {
        $result.node = $INSTALLATION_ERROR
        $result.commandOutput += "Node.js is installed but there is a problem with NPX!"
    }
}

# Check if nvm is already installed
if (Get-Command nvm -ErrorAction SilentlyContinue) {
    try {
        $nvm_version = & nvm version
        $result.nvm = $INSTALLED # nvm installed successfully
        $result.nvm_version = $nvm_version
        $result.commandOutput += "NVM $nvm_version is installed!"
    } catch {
        $result.nvm = $INSTALLATION_ERROR # Error running nvm but is installed already!
        $result.commandOutput += "NVM is installed but error in execution!"
    }
} else {
    $result.commandOutput += "NVM is not installed!"
}

$result.commandOutput += "Blender Web Pro Installation check complete!"

$result | ConvertTo-Json
exit 0
