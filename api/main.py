import io
import os.path

import json
import uvicorn
from aleph.sdk import AuthenticatedAlephHttpClient
from aleph.sdk.chains.common import get_fallback_private_key
from aleph.sdk.chains.ethereum import ETHAccount
from aleph.sdk.conf import settings
from aleph_client.synchronous import fetch_aggregate

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response, StreamingResponse

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

video_path = "video.mp4"


async def download_video(hash):
    pkey = get_fallback_private_key()

    account = ETHAccount(private_key=pkey)

    async with AuthenticatedAlephHttpClient(account=account, api_server=settings.API_HOST) as session:
        file_content = await session.download_file(hash)
        print(file_content)
        file_path = f"{hash}.mp4"  # Naming the file with the hash
        with open(file_path, "wb") as f:
            f.write(file_content)


@app.get("/files/{file}")
async def get_hls(file: str):
    path = os.path.join("../outputs", file)

    with open(path, "r") as f:
        content = f.read()

        return Response(content, media_type="application/vnd.apple.mpegurl")


@app.get("/video/{hash}/{video}")
async def get_video(hash: str, video: str):
    pkey = get_fallback_private_key()

    account = ETHAccount(private_key=pkey)

    async with AuthenticatedAlephHttpClient(account=account, api_server=settings.API_HOST) as session:
        file_content = await session.download_file(hash)

    file_object = io.BytesIO(file_content)

    return StreamingResponse(file_object, media_type="video/MP2T")


def load_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config

config = load_config()
account = ETHAccount(private_key=bytes.fromhex(config["private_key"]))

@app.get("/streamStatusOn/{owner}") 
def start_stream(self, owner: str):
    streamer_status = {owner: True}
    send_aggregate_aleph(account, "Streamer",{owner:True}, 'Streamer' )

@app.get("/streamStatusOff/{owner}")
def stop_stream(self, owner: str):
    streamer_status = {owner: False}
    send_aggregate_aleph(account, "Streamer",{owner:True}, 'Streamer')


@app.get("/steams")
async def get_active_stream():
    all_streamer=fetch_aggregate(account,"Streamer")
    online_streamer = []
    for key, value in all_streamer.items():
        if value == True:
            online_streamer.append(key)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
