#/bin/sh

# Change to the api server directory
cd ./api

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
. venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Run the api server
uvicorn main:app --reload