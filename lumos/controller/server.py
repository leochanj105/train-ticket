import asyncio
import websockets
import argparse
import sys
import time

class Server:
    # async def hello(websocket, path):
    #     name = await websocket.recv()
    #     print(f"< {name}")

    #     greeting = f"Hello {name}!"
    #     await websocket.send(greeting)
    #     print(f"> {greeting}")

    def __init__(self):
        self.conn = None
        return

    async def handler(self, conn):
        self.conn = conn
        name = await self.conn.recv()
        print(f"< {name}")

        greeting = f"Hello {name}!"
        while True:
            await self.conn.send(greeting)
            print(f"> {greeting}")
            time.sleep(1)

    async def run(self):
        async with websockets.serve(self.handler, "0.0.0.0", 8765):
            await asyncio.Future()  # run forever


# if __name__ == '__main__':
#     # parser = argparse.ArgumentParser()
#     # parser.add_argument('-v','--views', type=int, nargs='+', help='Views', required=True)
#     # options = parser.parse_args()

#     sender = Sender()
#     asyncio.run(sender.run())
