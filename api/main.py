import io
import os.path
import re
from typing import Annotated

import json
import uvicorn
from aleph.sdk import AuthenticatedAlephHttpClient
from aleph.sdk.chains.common import get_fallback_private_key
from aleph.sdk.chains.ethereum import ETHAccount
from aleph.sdk.conf import settings
from aleph_client.synchronous import fetch_aggregate

from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import Response, StreamingResponse

import jwt

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


def initialize_playlist(playlist_path, target_duration):
    file = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-TARGETDURATION:{target_duration}
#EXT-X-DISCONTINUITY
    """

    if os.path.exists(playlist_path):
        os.remove(playlist_path)

    with open(playlist_path, 'w') as f:
        f.write(file)


def get_target_duration(segment_path):
    with open(segment_path, 'r') as f:
        segment = f.read()

        pattern = r'#EXT-X-TARGETDURATION:(\d+)'
        match = re.search(pattern, segment)
        if match:
            # Récupération de la valeur capturée
            target_duration = match.group(1)
            return target_duration


def add_segment_to_playlist(playlist_path, segment_path):
    with open(segment_path, 'r') as f:
        segment = f.read()

    # parse the playlist and get #EXTINF: and segment URI
    pattern_extinf = r'#EXTINF:(\d+\.\d+),'
    pattern_url = r'http\S+'

    match_extinf = re.search(pattern_extinf, segment)
    match_url = re.search(pattern_url, segment)

    if match_extinf and match_url:
        with open(playlist_path, 'a') as f:
            f.write(f"#EXTINF:{match_extinf.group(1)},\n")
            f.write(f"{match_url.group()}\n")


def generate_playlist(streams_path, segment_path):
    playlist_path = os.path.join(streams_path, "playlist.m3u8")

    if not os.path.exists(playlist_path):
        initialize_playlist(playlist_path, get_target_duration(segment_path))

    add_segment_to_playlist(playlist_path, segment_path)


@app.post("/hls/store-segment")
async def store_hls_segment(segment: UploadFile, stream_key: str):
    if not stream_key:
        return Response(status_code=400)

    try:
        data = jwt.decode(stream_key, "secret", algorithms=["HS256"])
    except Exception as e:
        return Response(status_code=400, content=str(e))

    account = data["account"]

    account_streams_dir = os.path.join("./streams", account)
    if not os.path.exists(account_streams_dir):
        os.makedirs(account_streams_dir)

    segment_path = os.path.join(account_streams_dir, segment.filename)
    segment_content = await segment.read()
    with open(segment_path, "wb") as f:
        f.write(segment_content)

    generate_playlist(account_streams_dir, segment_path)

    return {"status": "ok"}


@app.get("/hls/{account}/playlist.m3u8")
async def get_hls_playlist(account: str):
    playlist_path = os.path.join("./streams", account, "playlist.m3u8")

    if not os.path.exists(playlist_path):
        return Response(status_code=400)

    with open(playlist_path, "r") as f:
        content = f.read()

        return Response(content, media_type="application/vnd.apple.mpegurl")


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

@app.post("/accounts/{account}/generate-stream-key")
async def generate_stream_key(account: str):
    data = {
        "account": account,
    }

    stream_key = jwt.encode(data, "secret", algorithm="HS256")

    return Response(content=stream_key, media_type="application/json")


@app.get("/accounts/verfify-stream-key")
async def verify_stream_key(stream_key: str):
    try:
        jwt.decode(stream_key, "secret", algorithms=["HS256"])
    except Exception as e:
        return Response(status_code=400, content=str(e))

    return Response(content="ok", media_type="application/json")
