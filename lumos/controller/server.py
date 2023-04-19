import asyncio
import websockets
import argparse
import sys
import time
from threading import Thread

class Server:
    # async def hello(websocket, path):
    #     name = await websocket.recv()
    #     print(f"< {name}")

    #     greeting = f"Hello {name}!"
    #     await websocket.send(greeting)
    #     print(f"> {greeting}")

    def __init__(self):
        #self.conn = None
        self.connections = dict()
        return
    
    async def test(self, name):
        conn = self.connections[name]
        seconds = 120
        for i in range(seconds):
            print(seconds - i)
            time.sleep(1)
            if i%5 == 0:
                await conn.send("keepalive")

        msg = 'travel.service.TravelServiceImpl,query,io.opentelemetry.api.trace.Span.current().addEvent(\"[LUMOS] HELLO!!!!!!!!\");,158'
        await conn.send(msg)
        print(f"> {msg}")

    async def handler(self, conn):
        name = await conn.recv()
        self.connections[name] = conn
        print(f"< {name}")
        #await conn.send("Hi")

        if "ts-travel-service" in name:
            await self.test(name)

    async def run(self):
        async with websockets.serve(self.handler, "0.0.0.0", 8765):
            await asyncio.Future()  # run forever


# if __name__ == '__main__':
#     # parser = argparse.ArgumentParser()
#     # parser.add_argument('-v','--views', type=int, nargs='+', help='Views', required=True)
#     # options = parser.parse_args()

#     sender = Sender()
#     asyncio.run(sender.run())
