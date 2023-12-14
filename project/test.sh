#!/bin/sh

# Set the working directory to the script's directory
# shellcheck disable=SC2164
cd "$(dirname "$0")"

# Inform the user about the installation of dependencies
echo "Installing project dependencies..."
pip install -r ../requirements.txt
echo "Dependencies installed successfully."

# Run the Python script from the "data" directory
python ./data/pipeline.py

