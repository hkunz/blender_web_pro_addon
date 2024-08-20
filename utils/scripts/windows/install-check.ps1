. "$PSScriptRoot\common\exit-codes.ps1"
. "$PSScriptRoot\common\utils.ps1"


Write-Host ""
Write-Host "$PSCommandPath" -ForegroundColor Blue
Write-Host "Checking installation prerequisites ..." -ForegroundColor White

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

    infos = @() # list of info outputs displayed in Blender's Info Panel
    errors = @() # list of error outputs displayed in Blender's Info Panel
}

Init-Log "$PSScriptRoot\..\..\..\logs\install-check.log" | Out-Null

# Check Chocolatey:
$install_name = "Chocolatey"
$version = ""
Write-Host "Checking if $install_name is already installed ..."
if ((Get-Command choco -ErrorAction SilentlyContinue) -and !$TEST_INSTALL_CHOC) {
    try {
        if ($TEST_INSTALL_CHOC_EXCEPT) {throw "Test Exception"}
        $version = & choco --version
        $msg = "$install_name $version is already installed!"
        $result.choco = $INSTALLED
        $result.choco_version = $version
        $result.infos += $msg
        Write-Host "$msg" -ForegroundColor Yellow
    } catch {
        $msg = "$install_name $version is installed but error in execution!"
        $result.choco = $INSTALLATION_ERROR
        $result.errors += $msg
        Write-Error "$msg"
    }
} else {
    $msg = "$install_name is not yet installed. You can either install it manually or with a click of a button within the addon."
    $result.infos += $msg
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
        $msg = "$install_name $version is already installed!"
        $nodejs_installed = $True
        $result.node = $INSTALLED
        $result.node_version = $version
        $result.infos += $msg
        Write-Host "$msg" -ForegroundColor Yellow
    } catch {
        $msg = "$install_name $version is installed, but an error occurred during execution."
        $result.node = $INSTALLATION_ERROR
        $result.errors += $msg
        Write-Error "$msg"
    }
} else {
    $msg = "$install_name is not yet installed. You can either install it manually or with a click of a button within the addon."
    $result.infos += $msg
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
        $msg = "$install_name $version is already installed!"
        $result.npm = $INSTALLED
        $result.npm_version = $version
        $result.infos += $msg
        Write-Host "$msg" -ForegroundColor Yellow
    } catch {
        $msg = "$install_name $version is installed, but an error occurred during execution."
        $result.node = $INSTALLATION_ERROR
        $result.npm = $INSTALLATION_ERROR
        $result.errors += $msg
        Write-Error "$msg"
    }
} else {
     if ($nodejs_installed) {
        $msg = "ERROR: $install_name should have been available with the installation of '$node_js_name'! Try to re-install '$node_js_name' manually."
        $result.node = $INSTALLATION_ERROR
        $result.npm = $INSTALLATION_ERROR
        $result.errors += $msg
        Write-Error $msg
    } else {
        $msg = "$install_name is not yet installed. NPM becomes available when installing '$node_js_name'. You can either install '$node_js_name' manually or with a click of a button within the addon."
        $result.infos += $msg
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
        $msg = "$install_name $version is already installed!"
        $result.npx = $INSTALLED
        $result.npx_version = $version
        $result.infos += $msg
        Write-Host "$msg" -ForegroundColor Yellow
    } catch {
        $msg = "$install_name $version is installed, but an error occurred during execution."
        $result.node = $INSTALLATION_ERROR
        $result.npx = $INSTALLATION_ERROR
        $result.errors += $msg
        Write-Error "$msg"
    }
} else {
    if ($nodejs_installed) {
        $msg = "ERROR: $install_name should have been available with the installation of '$node_js_name'! Try to re-install '$node_js_name' manually."
        $result.node = $INSTALLATION_ERROR
        $result.npx = $INSTALLATION_ERROR
        $result.errors += $msg
        Write-Error $msg
    } else {
        $msg = "$install_name is not yet installed. It becomes available when installing '$node_js_name'. You can either install '$node_js_name' manually or with a click of a button within the addon."
        $result.infos += $msg
        Write-Host "$msg" -ForegroundColor Yellow
    }
}


# Check NVM: (This should happen before Node.js installation because you need NVM to manage multiple Node.js installations)
<#
$install_name = "Node Version Manager (NVM)"
$version = ""
Write-Host "Checking if $install_name is already installed ..."
if ((Get-Command nvm -ErrorAction SilentlyContinue) -and !$TEST_INSTALL_NVM) {
    try {
        if ($TEST_INSTALL_NVM_EXCEPT) {throw "Test Exception"}
        $version = & nvm version
        $msg = "$install_name $version is already installed!"
        $result.nvm = $INSTALLED
        $result.nvm_version = $version
        $result.infos += $msg
        Write-Host "$msg" -ForegroundColor Yellow
    } catch {
        $msg = "$install_name $version is installed, but an error occurred during execution."
        $result.nvm = $INSTALLATION_ERROR
        $result.errors += $msg
        Write-Error "$msg"
    }
} else {
    $msg = "$install_name is not yet installed. You can either install it manually or with a click of a button within the addon."
    $result.infos += $msg
    Write-Host "$msg" -ForegroundColor Yellow
}
#>

$result.infos += "Blender Web Pro Installation check complete!"

Log-Progress -message ($result | ConvertTo-Json)

exit $SUCCESS
