#!/bin/sh

# Set the working directory to the script's directory
# shellcheck disable=SC2164
cd "$(dirname "$0")"

# Inform the user about the installation of dependencies
echo "Installing project dependencies..."
pip install -r ./requirements.txt
echo "Dependencies installed successfully."

# Run the Python scripts
echo "Running pipeline.py..."
python ./data/pipeline.py

# Add the execution of pipeline_test.py with pytest
echo "Running pipeline_test.py with pytest..."
pytest ./data/pipeline_test.py

# Provide feedback
echo "Python scripts and pytest executed successfully."
