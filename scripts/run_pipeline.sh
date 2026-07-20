#!/bin/bash

# -----------------------------
# Bash + Python Data Pipeline
# -----------------------------

echo "=================================="
echo "Starting Data Processing Pipeline"
echo "=================================="

# Move to project root
cd "$(dirname "$0")/.."

# Create required folders
mkdir -p logs output

# Check Python
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed."
    exit 1
fi

# Check curl
if ! command -v curl &> /dev/null
then
    echo "curl is not installed."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "Virtual environment activated."

# Check if dataset exists
if [ ! -f data/iris.csv ]; then
    echo "Dataset not found."

    # Download dataset (replace with your URL if required)
    curl -L \
https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv \
-o data/iris.csv

    if [ $? -ne 0 ]; then
        echo "Download failed."
        exit 1
    fi
fi

echo "Dataset ready."

echo "Running Python script..."

python3 scripts/process_data.py

if [ $? -eq 0 ]
then
    echo "Pipeline completed successfully."
else
    echo "Pipeline failed."
fi