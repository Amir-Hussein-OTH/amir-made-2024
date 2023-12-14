#!/bin/sh

# Set the working directory
cd testing || { echo "Unable to change directory. Exiting."; exit 1; }

# Inform the user about the installation of dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt || { echo "Dependency installation failed. Exiting."; exit 1; }
echo "Dependencies installed successfully."

python ./data/pipeline.py
