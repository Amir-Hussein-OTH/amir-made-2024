#!/bin/sh

# Set the working directory
# shellcheck disable=SC2164
cd testing

# Inform the user about the installation of dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt
echo "Dependencies installed successfully."


