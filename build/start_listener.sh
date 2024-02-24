#/bin/sh

# Change to the listener loop directory
cd ./rtmp

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
. venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Run the listener loop
python3 listener.py