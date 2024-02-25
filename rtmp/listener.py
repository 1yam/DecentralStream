import json
import subprocess

import aiohttp
import asyncio
import time
import os

def load_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config


config = load_config()


async def upload_video(chunk):
    async with aiohttp.ClientSession() as session:
        timestamp = int(time.time())  # Current timestamp
        filename = f'{timestamp}.mp4'  # Unique filename with timestamp
        data = aiohttp.FormData()
        data.add_field('file', chunk)

        async with session.post('https://api2.aleph.im/api/v0/ipfs/add_file', data=data) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(status=response.status, message=response.reason)

            return await response.json()


async def wait_for_file_creation(filename):
    size = 0
    unchanged_count = 0
    while True:
        if os.path.exists(filename):
            current_size = os.path.getsize(filename)
            if current_size == size:
                unchanged_count += 1
                if unchanged_count >= 3:  # Nombre de vérifications successives sans changement
                    return True
            else:
                size = current_size
                unchanged_count = 0
        await asyncio.sleep(1)  # Attendre une seconde avant de vérifier à nouveau


async def convert_to_hls(input_video, hash):
    # Créer le dossier de sortie s'il n'existe pas
    output_folder = 'hls-outputs'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Récupérer le nom du fichier sans extension
    file_name = os.path.splitext(os.path.basename(input_video))[0]

    # Chemin de sortie pour la playlist m3u8
    output_playlist = os.path.join(output_folder, f'{file_name}.m3u8')

    # URL de base pour les segments HLS
    base_url = f"{config['api_url']}/video/{hash}/"

    command = [
        'ffmpeg',
        '-i', input_video,  # Chemin vers la vidéo d'entrée
        # '-c:a', 'aac', '-b:a', '128k',  # Paramètres audio
        # '-ar', '44100',  # Taux d'échantillonnage audio
        '-f', 'hls',  # Format de sortie HLS
        '-hls_time', '5',  # Durée des segments HLS (5 secondes)
        '-hls_playlist_type', 'event',  # Type de playlist HLS (optionnel)
        '-hls_base_url', base_url,  # URL de base pour les segments HLS
        '-method', 'append',  # Ajoutez cette option pour ajouter les nouveaux segments à la playlist existante
        output_playlist  # Chemin de sortie de la playlist m3u8
    ]

    # Exécuter la commande FFmpeg
    subprocess.run(command)

    return { "file_name": f'{file_name}.m3u8', "file_path": output_playlist }


async def search_and_upload():
    count = 0
    while True:
        filename = f'outputs/{count:03d}.ts'  # Format filename with leading zeros
        await wait_for_file_creation(filename)  # Attendre que le fichier soit créé
        with open(filename, 'rb') as file:
            chunk = file.read()
        try:
            result = await upload_video(chunk)

            hls_file = await convert_to_hls(filename, result['hash'])

            # if count == 0:
            #     hls.initialize_playlist(hls.get_target_duration(hls_file))
            #
            # hls.add_segment_to_playlist(hls_file)
            data = aiohttp.FormData()
            with open(hls_file['file_path'], 'rb') as f:
                data.add_field('segment', f, filename=hls_file['file_name'])
                async with aiohttp.ClientSession() as session:
                    async with session.post(f"{config['api_url']}/hls/store-segment?stream_key={config['stream_key']}",
                                            data=data) as resp:
                        await resp.release()

            # name = "StreamTest"
            # async with aiohttp.ClientSession() as session:
            #     async with session.post(f"http://localhost:5000/store_cid/{name}?key={result['hash']}") as resp:
            #         await resp.release()

            print(f"File '{filename}' uploaded to IPFS. IPFS Hash: {result['hash']}")
        except Exception as e:
            print(f"Error uploading '{filename}' to IPFS: {e}")
        count += 1


async def main():
    stream_key = json.loads(open('config.json').read())['stream_key']
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{config['api_url']}/accounts/verfify-stream-key?stream_key={config['stream_key']}") as resp:
            await resp.release()
            if resp.status != 200:
                raise Exception('Bad stream_key. Exiting...')


    await search_and_upload()


if __name__ == "__main__":
    asyncio.run(main())
