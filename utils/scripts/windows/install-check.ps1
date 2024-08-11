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

    commandOutput = @("Blender Web Pro Installation check complete!")
}

# Check if Chocolatey is already installed
if (Get-Command choco -ErrorAction SilentlyContinue) {
    try {
        $choco_version = & choco --version
        $result.choco = $INSTALLED # Choco installed successfully
        $result.choco_version = $choco_version
    } catch {
        $result.choco = $INSTALLATION_ERROR # Error running choco but is installed already!
    }
}

# Check if Node.js is already installed
try {
    $node_version = & node --version
    $result.node = $INSTALLED # Node.js installed successfully
    $result.node_version = $node_version
} catch {
    $result.node = $INSTALLATION_ERROR # Error running node but is installed already!
}

# Check if npm is already installed
try {
    $npm_version = & npm --version
    $result.npm = $INSTALLED # npm installed successfully
    $result.npm_version = $npm_version
} catch {
    $result.npm = $INSTALLATION_ERROR # Error running npm but is installed already!
}

# Check if npx is already installed
try {
    $npx_version = & npx --version
    $result.npx = $INSTALLED # npx installed successfully
    $result.npx_version = $npx_version
} catch {
    $result.npx = $INSTALLATION_ERROR # Error running npx but is installed already!
}

# Check if nvm is already installed
try {
    $nvm_version = & nvm version
    $result.nvm = $INSTALLED # nvm installed successfully
    $result.nvm_version = $nvm_version
} catch {
    $result.nvm = $INSTALLATION_ERROR # Error running npx but is installed already!
}

$result | ConvertTo-Json
exit 0
