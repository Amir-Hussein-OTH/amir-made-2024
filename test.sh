#!/bin/sh

# Set the working directory
cd testing

# Inform the user about the installation of dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt
echo "Dependencies installed successfully."

# Execute the pipeline
echo "Executing the data pipeline..."
python data/pipeline_script.py
echo "Data pipeline execution completed."

# Provide a friendly farewell message
echo "Pipeline script execution finished."
