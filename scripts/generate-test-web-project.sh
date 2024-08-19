#!/bin/bash

# This script will create the directory specified in the .vscode/settings.json file under the property "liveServer.settings.root"
# This generated directory serves as the root for the web server configuration when running VSCode Live Server
# Populate this generated directory by installing Three.js & Vite dependency using the Blender Web Pro addon
# Test the website using the addon's test web page functionality


CONFIG_FILE=".vscode/settings.json"

# Extract the directory path using grep and sed
#DIR_PATH=$(grep '"liveServer.settings.root"' "$CONFIG_FILE" | sed 's/.*"liveServer.settings.root": "\(.*\)".*/\1/' | sed 's/^\/\?//')
DIR_PATH="test/test-project/"

# Check if the directory path was extracted successfully
if [ -z "$DIR_PATH" ]; then
  echo "Error: Directory path not found in the configuration file."
  exit 1
fi

# Create the directory
mkdir -p "$DIR_PATH"

# Check if the directory was created successfully
if [ $? -eq 0 ]; then
  echo "Directory '$DIR_PATH' created successfully."
else
  echo "Error: Failed to create directory '$DIR_PATH'."
  exit 1
fi
