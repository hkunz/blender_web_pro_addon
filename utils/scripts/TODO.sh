# GLTFLoader: https://threejs.org/docs/#examples/en/loaders/GLTFLoader
# Three JS Installation: https://threejs.org/docs/#manual/en/introduction/Installation

# LINUX ===============================================

# npm installation
sudo apt update # to refresh the package lists from the repositories. This will help in getting the latest package information
sudo apt-get update --fix-missing # to attempt to fix any missing dependencies.
sudo apt upgrade # to apply the updates
sudo apt install npm

# three js installation
npm install --save three
npm install --save-dev vite

# nvm installation:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
source ~/.bashrc
nvm --version

# installation of latest version node.js
nvm install --lts


npx vite


# WINDOWS ===================================================

# Refresh the package lists and apply updates
# Note: These commands are typically for Ubuntu. On Windows, package management is different.
# We will use Chocolatey for package management in Windows.
Set-ExecutionPolicy Bypass -Scope Process -Force; 
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; 
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

choco --version
choco upgrade chocolatey


# Install npm and nodejs using Chocolatey
choco install -y nodejs-lts

# Check if Chocolatey installed correctly


# Install npm packages: three and vite
# npm install --save three
# npm install --save-dev vite

# nvm installation:
# Download nvm-setup.zip from the official nvm-windows repository
Invoke-WebRequest -Uri "https://github.com/coreybutler/nvm-windows/releases/download/1.1.9/nvm-setup.zip" -OutFile "nvm-setup.zip"

# Extract the installer
Expand-Archive -Path "nvm-setup.zip" -DestinationPath "$env:USERPROFILE\nvm"

# Run the installer
Start-Process -FilePath "$env:USERPROFILE\nvm\nvm-setup.exe" -Wait


# choco install -y nvm # use manual way of installation since this one will not put it in PATH

# Verify nvm installation
nvm --version
nvm install lts
nvm use lts

# Verify Node.js and npm installation
node -v
npm -v

npm install --save three
npm install --save-dev vite

# Run Vite
npx vite




# CONFIGURE VITE:

touch vite.config.mjs and enter content:

import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    open: true  // Automatically open the browser
  }
});

# RUN

# Run Subprocess to Open Browser

import subprocess
import os
import bpy

bpy.ops.wm.console_toggle()

directory = r'C:\Users\harry\workspace\test'
command = 'npx vite'


# BETTER RUN SUBPROCESS

import subprocess
import os
import bpy

directory = r'C:\Users\harry\workspace\test'
#command = 'npx vite'
#subprocess.run(command, shell=True, cwd=directory, check=True)

#bpy.ops.wm.console_toggle()
server_script = os.path.join(directory, r'server.py')
subprocess.Popen(['python', server_script])



# Run the command in the specified directory
subprocess.run(command, shell=True, cwd=directory, check=True)



# PYTHON ===================================

import subprocess

# PowerShell script to be executed
powershell_script = """
# Refresh the package lists and apply updates
Set-ExecutionPolicy Bypass -Scope Process -Force;
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install npm and nodejs using Chocolatey
choco install -y nodejs-lts

# Check if Chocolatey installed correctly
choco --version

# Install npm packages: three and vite
npm install --save three
npm install --save-dev vite

# nvm installation:
# Download nvm-setup.zip from the official nvm-windows repository
Invoke-WebRequest -Uri "https://github.com/coreybutler/nvm-windows/releases/download/1.1.9/nvm-setup.zip" -OutFile "nvm-setup.zip"

# Extract the installer
Expand-Archive -Path "nvm-setup.zip" -DestinationPath "$env:USERPROFILE\nvm"

# Run the installer
Start-Process -FilePath "$env:USERPROFILE\nvm\nvm-setup.exe" -Wait

# Verify nvm installation
nvm --version

# Install the latest LTS version of Node.js using nvm
nvm install lts
nvm use lts

# Verify Node.js and npm installation
node -v
npm -v

# Run Vite
npx vite
"""

# Save the PowerShell script to a file
script_path = "setup.ps1"
with open(script_path, "w") as file:
    file.write(powershell_script)

# Execute the PowerShell script
subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_path], check=True)





Uninstall Node.js: 
Control Panel > Programs > Programs and Features > Uninstall Program > Search for Node.js > remove
Uninstall Choco:
Remove-Item -Recurse -Force C:\ProgramData\chocolatey


choco uninstall all -y
Remove-Item -Recurse -Force C:\ProgramData\chocolatey
choco --version # verify it's uninstalled
