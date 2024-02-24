import io
import os.path
import json  # Add this import for reading JSON config file

from aleph.sdk import AuthenticatedAlephHttpClient
from aleph.sdk.chains.common import get_fallback_private_key
from aleph.sdk.chains.ethereum import ETHAccount
from aleph.sdk.conf import settings

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

# Load private key from config file
def load_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config

config = load_config()
private_key = config["private_key"]


async def download_video(hash):
    pkey = private_key  # Use the loaded private key

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
    pkey = private_key  # Use the loaded private key

    account = ETHAccount(private_key=pkey)

    async with AuthenticatedAlephHttpClient(account=account, api_server=settings.API_HOST) as session:
        file_content = await session.download_file(hash)

    file_object = io.BytesIO(file_content)

    return StreamingResponse(file_object, media_type="video/MP2T")
