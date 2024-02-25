from fastapi import FastAPI, HTTPException, Request
from datetime import datetime
import json

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@app.post('/post_message')
async def post_message(request: Request):
    data = await request.json()
    if 'channel' in data and 'username' in data and 'message' in data:
        channel = data['channel']
        username = data['username']
        message = data['message']
        add_message(channel, username, message)
        return {"success": True}
    else:
        raise HTTPException(status_code=400, detail="Missing channel, username, or message")


# Route to get messages from a specific channel
@app.get('/get_messages/{channel}')
async def get_messages(channel: str):
    if channel in channels:
        return channels[channel]
    else:
        raise HTTPException(status_code=404, detail="Channel not found")
