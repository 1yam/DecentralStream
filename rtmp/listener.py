import subprocess

import asyncio
import os

import ipfs
import api_call
import config


async def convert_to_hls(input_video: str, hash: str):
    output_folder = config.Config.HLS_OUTPUT_DIR

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_name_without_ext = os.path.splitext(os.path.basename(input_video))[0]

    output_playlist = os.path.join(output_folder, f'{file_name_without_ext}.m3u8')

    hls_remote_base_url = f"{config.Config.API_URL}/video/{hash}/"

    command = [
        'ffmpeg',
        '-i', input_video,
        '-f', 'hls',
        '-hls_time', '5',
        '-hls_playlist_type', 'event',
        '-hls_base_url', hls_remote_base_url,
        '-method', 'append',
        output_playlist
    ]

    subprocess.run(command)

    return {"file_name": f'{file_name_without_ext}.m3u8', "file_path": output_playlist}


async def wait_for_file_creation(file_path: str):
    size = 0
    unchanged_count = 0

    while True:
        if os.path.exists(file_path):
            current_size = os.path.getsize(file_path)
            if current_size == size:
                unchanged_count += 1
                if unchanged_count >= 3:
                    return True
            else:
                size = current_size
                unchanged_count = 0
        await asyncio.sleep(1)


async def search_and_upload_loop():
    count = 0

    while True:
        input_video_path = f'outputs/{count:03d}.ts'

        await wait_for_file_creation(input_video_path)

        with open(input_video_path, 'rb') as file:
            chunk = file.read()
        try:
            result = await ipfs.upload_video_to_ipfs(chunk)

            hls_file = await convert_to_hls(input_video_path, result['hash'])

            await api_call.store_segment(hls_file['file_path'], hls_file['file_name'])

            print(f"File '{input_video_path}' uploaded to IPFS. IPFS Hash: {result['hash']}")
        except Exception as e:
            print(f"Error uploading '{input_video_path}' to IPFS: {e}")
        count += 1


async def main():
    await api_call.verify_stream_key()

    await search_and_upload_loop()


if __name__ == "__main__":
    asyncio.run(main())
