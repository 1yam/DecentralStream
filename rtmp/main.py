from __future__ import annotations

import asyncio
import json
import logging
import os
from asyncio import StreamReader

import aiohttp
from pyrtmp import StreamClosedException
from pyrtmp.flv import FLVMediaType, FLVWriter
from pyrtmp.rtmp import RTMPProtocol, SimpleRTMPController, SimpleRTMPServer
from pyrtmp.session_manager import SessionManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RTMP2SocketController(SimpleRTMPController):
    def __init__(self, output_directory: str):
        self.output_directory = output_directory
        super().__init__()

    async def on_ns_publish(self, session, message) -> None:
        publishing_name = message.publishing_name
        prefix = os.path.join(self.output_directory, f"{publishing_name}")
        session.state = RemoteProcessFLVWriter()
        logger.debug(f"outputs to {prefix}.mp4")
        await session.state.initialize(
            command=f"ffmpeg -y -i pipe:0 -c:v copy -c:a copy -f segment -segment_time 5  -segment_format mpegts {prefix}%03d.ts",
            stdout_log=f"{prefix}.stdout.log",
            stderr_log=f"{prefix}.stderr.log",
        )
        session.state.write_header()
        await super().on_ns_publish(session, message)

    async def on_metadata(self, session, message) -> None:
        session.state.write(0, message.to_raw_meta(), FLVMediaType.OBJECT)
        await super().on_metadata(session, message)

    async def on_video_message(self, session, message) -> None:
        session.state.write(message.timestamp, message.payload, FLVMediaType.VIDEO)
        await super().on_video_message(session, message)

    async def on_audio_message(self, session, message) -> None:
        session.state.write(message.timestamp, message.payload, FLVMediaType.AUDIO)
        await super().on_audio_message(session, message)

    async def on_stream_closed(self, session: SessionManager, exception: StreamClosedException) -> None:
        await session.state.close()
        await super().on_stream_closed(session, exception)


class RemoteProcessFLVWriter:
    def __init__(self):
        self.stream_key = json.loads(open('config.json').read())['stream_key']

        self.proc = None
        self.stdout = None
        self.stderr = None
        self.writer = FLVWriter()

    async def initialize(self, command: str, stdout_log: str, stderr_log: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"http://localhost:8000/start-stream?stream_key={self.stream_key}") as resp:
                await resp.release()
                if resp.status != 200:
                    raise Exception('An error are occured while starting stream. Exiting...')

        self.proc = await asyncio.create_subprocess_shell(
            command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        self.stdout = asyncio.create_task(self._read_to_file(stdout_log, self.proc.stdout))
        self.stderr = asyncio.create_task(self._read_to_file(stderr_log, self.proc.stderr))

    async def _read_to_file(self, filename: str, stream: StreamReader):
        fp = open(filename, "w")
        while not stream.at_eof():
            data = await stream.readline()
            fp.write(data.decode())
            fp.flush()

        fp.close()

    def write_header(self):
        buffer = self.writer.write_header()
        self.proc.stdin.write(buffer)

    def write(self, timestamp: int, payload: bytes, media_type: FLVMediaType):
        buffer = self.writer.write(timestamp, payload, media_type)
        self.proc.stdin.write(buffer)

    async def close(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"http://localhost:8000/stop-stream?stream_key={self.stream_key}") as resp:
                await resp.release()
                if resp.status != 200:
                    raise Exception('An error are occured while stopping stream. Exiting...')

        await self.proc.stdin.drain()
        self.proc.stdin.close()
        await self.proc.wait()


class SimpleServer(SimpleRTMPServer):
    def __init__(self, output_directory: str):
        self.output_directory = output_directory
        super().__init__()

    async def create(self, host: str, port: int):
        loop = asyncio.get_event_loop()
        self.server = await loop.create_server(
            lambda: RTMPProtocol(controller=RTMP2SocketController(self.output_directory)),
            host=host,
            port=port,
        )


async def main():
    stream_key = json.loads(open('config.json').read())['stream_key']
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"http://localhost:8000/accounts/verfify-stream-key?stream_key={stream_key}") as resp:
            await resp.release()
            if resp.status != 200:
                raise Exception('Bad stream_key. Exiting...')

    current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
    server = SimpleServer(output_directory=current_dir)
    await server.create(host="0.0.0.0", port=1234)
    await server.start()
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
