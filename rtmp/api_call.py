import aiohttp
import config


async def verify_stream_key() -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{config.Config.API_URL}/accounts/verfify-stream-key?stream_key={config.Config.STREAM_KEY}") as resp:
            await resp.release()

            if resp.status != 200:
                raise Exception('An error are occured while stopping stream. Exiting...')


async def start_stream() -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{config.Config.API_URL}/start-stream?stream_key={config.Config.STREAM_KEY}") as resp:
            await resp.release()

            if resp.status != 200:
                raise Exception('An error are occured while starting stream. Exiting...')


async def stop_stream() -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{config.Config.API_URL}/stop-stream?stream_key={config.Config.STREAM_KEY}") as resp:
            await resp.release()

            if resp.status != 200:
                raise Exception('An error are occured while stopping stream. Exiting...')


async def store_segment(file_path: str, file_name: str) -> None:
    data = aiohttp.FormData()

    with open(file_path, 'rb') as f:
        data.add_field('segment', f, filename=file_name)
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{config.Config.API_URL}/hls/store-segment?stream_key={config.Config.STREAM_KEY}",
                                    data=data) as resp:
                await resp.release()
