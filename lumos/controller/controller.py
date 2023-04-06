import asyncio
import websockets
import argparse
import sys

import server
import stat
import parser


class LumosController:
    def __init__(self):
        self.server = server.Server()
        asyncio.run(self.server.run())

        # WebSocket server

        # Trace parser

        # Trace stat examiner


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-s','--server', type=str, help='Lumos Controller Server Address', required=True)
    # options = parser.parse_args()
    # print(options.server)
    print("hello")

    controller = LumosController()