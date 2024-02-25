import json


def load_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config


config = load_config()


class Config:
    OUTPUT_DIR: str = 'outputs'
    HLS_OUTPUT_DIR: str = 'hls-outputs'

    API_URL: str = config['api_url']
    STREAM_KEY: str = config['stream_key']
