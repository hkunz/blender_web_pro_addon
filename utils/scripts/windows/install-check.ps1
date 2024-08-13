. "$PSScriptRoot\common\constants.ps1"
. "$PSScriptRoot\common\exit-codes.ps1"
. "$PSScriptRoot\common\utils.ps1"


Write-Host ""
Write-Host "$PSCommandPath" -ForegroundColor Green
Write-Host "Checking installation prerequisites ..." -ForegroundColor Yellow

# These constant values -0,1,2 are used in property_group_installation_properties.py
$NOT_INSTALLED = 0
$INSTALLED = 1
$INSTALLATION_ERROR = 2

$TEST_INSTALL_CHOC = 0
$TEST_INSTALL_NODE = 0
$TEST_INSTALL_NPX = 0
$TEST_INSTALL_NPM = 0
$TEST_INSTALL_NVM = 0

$TEST_INSTALL_CHOC_EXCEPT = 0
$TEST_INSTALL_NODE_EXCEPT = 0
$TEST_INSTALL_NPX_EXCEPT = 0
$TEST_INSTALL_NPM_EXCEPT = 0
$TEST_INSTALL_NVM_EXCEPT = 0

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

Init-Log "$PSScriptRoot\..\..\..\logs\install-check.log"

# Check Chocolatey:
$install_name = "Chocolatey"
$version = ""
Write-Host "Checking if $install_name is already installed ..."
if ((Get-Command choco -ErrorAction SilentlyContinue) -and !$TEST_INSTALL_CHOC) {
    try {
        if ($TEST_INSTALL_CHOC_EXCEPT) {throw "Test Exception"}
        $version = & choco --version
        $result.choco = $INSTALLED # Choco installed successfully
        $result.choco_version = $version
        $msg = "$install_name $version is installed!"
        $result.commandOutput += $msg + $LINE_END
        Write-Host "$msg" -ForegroundColor Yellow
    } catch {
        $result.choco = $INSTALLATION_ERROR
        $msg = "$install_name $version is installed but error in execution!"
        $result.commandOutput += $msg + $LINE_END
        Write-Error "$msg"
    }
} else {
    $msg = "$install_name is not yet installed. You can either install it manually or with a click of a button within the addon."
    $result.commandOutput += $msg + $LINE_END
    Write-Host "$msg" -ForegroundColor Yellow
}

$nodejs_installed = $False

# Check if Node.js:
$install_name = "Node.js"
$node_js_name = $install_name
$version = ""
Write-Host "Checking if $install_name is already installed ..."
if ((Get-Command node -ErrorAction SilentlyContinue) -and !$TEST_INSTALL_NODE) {
    try {
        if ($TEST_INSTALL_NODE_EXCEPT) {throw "Test Exception"}
        $version = & node --version
        $result.node = $INSTALLED
        $result.node_version = $version
        $nodejs_installed = $True
        $msg = "$install_name $version is installed!"
        $result.commandOutput += $msg + $LINE_END
        Write-Host "$msg" -ForegroundColor Yellow
    } catch {
        $result.node = $INSTALLATION_ERROR
        $msg = "$install_name $version is installed but there was an error trying to run it!"
        $result.commandOutput += $msg + $LINE_END
        Write-Error "$msg"
    }
} else {
    $msg = "$install_name is not yet installed. You can either install it manually or with a click of a button within the addon."
    $result.commandOutput += $msg + $LINE_END
    Write-Host "$msg" -ForegroundColor Yellow
}

# Check if NPM:
$install_name = "Node Package Manager (NPM)"
$version = ""
Write-Host "Checking if $install_name is already installed ..."
if ((Get-Command npm -ErrorAction SilentlyContinue) -and !$TEST_INSTALL_NPM) {
    try {
        if ($TEST_INSTALL_NPM_EXCEPT) {throw "Test Exception"}
        $version = & npm --version
        $result.npm = $INSTALLED
        $result.npm_version = $version
        $msg = "$install_name $version is installed!"
        $result.commandOutput += $msg + $LINE_END
        Write-Host "$msg" -ForegroundColor Yellow
    } catch {
        $result.npm = $INSTALLATION_ERROR
        $msg = "$install_name $version is installed but there was an error trying to run it!"
        $result.commandOutput += $msg + $LINE_END
        Write-Error "$msg"
    }
} else {
     if (-not $nodejs_installed) {
        $msg = "ERROR: $install_name should have been available with the installation of '$node_js_name'! Try to re-install '$node_js_name' manually."
        $result.commandOutput += $msg + $LINE_END
        Write-Error $msg
    } else {
        $msg = "$install_name is not yet installed. NPM becomes available when installing '$node_js_name'. You can either install '$node_js_name' manually or with a click of a button within the addon."
        $result.commandOutput += $msg + $LINE_END
        Write-Host "$msg" -ForegroundColor Yellow
    }
}

# Check NPX:
$install_name = "Node Package eXecute (NPX)"
$version = ""
Write-Host "Checking if $install_name is already installed ..."
if ((Get-Command npx -ErrorAction SilentlyContinue) -and !$TEST_INSTALL_NPX) {
    try {
        if ($TEST_INSTALL_NPX_EXCEPT) {throw "Test Exception"}
        $version = & npx --version
        $result.npx = $INSTALLED
        $result.npx_version = $version
        $msg = "$install_name $version is installed!"
        $result.commandOutput += $msg + $LINE_END
        Write-Host "$msg" -ForegroundColor Yellow
    } catch {
        $result.npx = $INSTALLATION_ERROR
        $msg = "$install_name $version is installed but there was an error trying to run it!"
        $result.commandOutput += $msg + $LINE_END
        Write-Error "$msg"
    }
} else {
    if (-not $nodejs_installed) {
        $msg = "ERROR: $install_name should have been available with the installation of '$node_js_name'! Try to re-install '$node_js_name' manually."
        $result.commandOutput += $msg + $LINE_END
        Write-Error $msg
    } else {
        $msg = "$install_name is not yet installed. It becomes available when installing '$node_js_name'. You can either install '$node_js_name' manually or with a click of a button within the addon."
        $result.commandOutput += $msg + $LINE_END
        Write-Host "$msg" -ForegroundColor Yellow
    }
}

# Check NVM:
$install_name = "Node Version Manager (NVM)"
$version = ""
Write-Host "Checking if $install_name is already installed ..."
if ((Get-Command nvm -ErrorAction SilentlyContinue) -and !$TEST_INSTALL_NVM) {
    try {
        if ($TEST_INSTALL_NVM_EXCEPT) {throw "Test Exception"}
        $version = & nvm version
        $result.nvm = $INSTALLED
        $result.nvm_version = $version
        $msg = "$install_name $version is installed!"
        $result.commandOutput += $msg + $LINE_END
        Write-Host "$msg" -ForegroundColor Yellow
    } catch {
        $result.nvm = $INSTALLATION_ERROR
        $msg = "$install_name $version is installed but there was an error trying to run it!"
        $result.commandOutput += $msg + $LINE_END
        Write-Error "$msg"
    }
} else {
    $msg = "$install_name is not yet installed. You can either install it manually or with a click of a button within the addon."
    $result.commandOutput += $msg + $LINE_END
    Write-Host "$msg" -ForegroundColor Yellow
}

$result.commandOutput += "Blender Web Pro Installation check complete!"

Log-Progress -message ($result | ConvertTo-Json)

exit $SUCCESS
