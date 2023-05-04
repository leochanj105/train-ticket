import asyncio
import websockets
import argparse
import sys

import server
import collector
import analyzer


class LumosController:
    def __init__(self):
        # WebSocket server
        self.server = server.Server()

        # Trace collector
        self.collector = collector.Collector()

        # Trace parser
        self.analyzer = analyzer.Analyzer()

    async def run(self):
        s = asyncio.create_task(self.server.run("/app/lumos/"))
        c = asyncio.create_task(self.collector.run())
        a = asyncio.create_task(self.analyzer.run())

        await s
        await c
        await a

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-s','--server', type=str, help='Lumos Controller Server Address', required=True)
    # options = parser.parse_args()
    # print(options.server)
    print("hello")

    controller = LumosController()
    asyncio.run(controller.run())