from flask import Flask, request, jsonify
from datetime import datetime
import json

###
### This API is not secure.
### This is the show possibility of feature using chat
### To Do: authentifcations with wallet
###

app = Flask(__name__)

# Load existing data from file if available
try:
    with open("chat_data.json", "r") as file:
        channels = json.load(file)
except FileNotFoundError:
    channels = {}

# Function to save data to file
def save_data():
    with open("chat_data.json", "w") as file:
        json.dump(channels, file)

# Function to add message to a channel
def add_message(channel, username, message):
    if channel not in channels:
        channels[channel] = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    channels[channel].append({"timestamp": timestamp, "username": username, "message": message})
    save_data()

# Route to post a message to a specific channel using JSON body
@app.route('/post_message', methods=['POST'])
def post_message():
    data = request.json
    if 'channel' in data and 'username' in data and 'message' in data:
        channel = data['channel']
        username = data['username']
        message = data['message']
        add_message(channel, username, message)
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Missing channel, username, or message"}), 400

# Route to get messages from a specific channel
@app.route('/get_messages/<channel>', methods=['GET'])
def get_messages(channel):
    if channel in channels:
        return jsonify(channels[channel])
    else:
        return jsonify({"error": "Channel not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
