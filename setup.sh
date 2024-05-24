#!/bin/bash

# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the project dependencies
pip install -r requirements.txt