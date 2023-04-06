import asyncio
import websockets
import time

async def agent():
    async with websockets.connect('ws://lumos:8765') as websocket:
        await websocket.send("hello")
        while True:
            greeting = await websocket.recv()
            print(f"< {greeting}")

if __name__ == '__main__':
    while True:
        try:
            asyncio.run(agent())
        except:
            print("waiting for host")
            time.sleep(1)
            pass