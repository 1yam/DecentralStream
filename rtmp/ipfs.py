import time

import aiohttp


async def upload_video_to_ipfs(chunk: bytes) -> dict:
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('file', chunk)

        async with session.post('https://api2.aleph.im/api/v0/ipfs/add_file', data=data) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(status=response.status, message=response.reason)

            return await response.json()