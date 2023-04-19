import asyncio
import websockets
import argparse
import sys
import time
from threading import Thread
import json

testarray = ['c,travel.service.TravelServiceImpl,query,io.opentelemetry.api.trace.Span.current().addEvent(\"[LUMOS] HELLO!!!!!!!!\");,158']

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
        self.id = 0
        return
    def gettps(self, arr):
        tps = "tps: ["
        for tp in arr:
            strs = tp.split(",")
            if(strs[0] == "c"):
                tp = self.codetp(strs[1], strs[2], strs[3], strs[4])
                tps += "{" + tp + "},"
        tps += "]"
        msg = "{type:add, " + tps + "}"
        return msg
    def codetp(self, cname, method, code, line):
        newid = self.id
        self.id += 1
        return f"id:'{newid}', cname:{cname}, method:{method}, tptype:code, line:{line}, code:'{code}'"
    def spantp(self, cname, method):
        newid = self.id
        self.id += 1
        return f"id:'{newid}', cname:{cname}, method:{method}, tptype:span"

    async def test(self, name):
        conn = self.connections[name]
        seconds = 20
        try:
            for i in range(seconds):
                print(seconds - i)
                await asyncio.sleep(1)

            msg = self.gettps(testarray)
            await conn.send(msg)
            print(f"> {msg}")
        except websockets.ConnectionClosedOK:
            pass


    async def handler(self, conn):
        name = await conn.recv()
        self.connections[name] = conn
        print(f"< {name}")
        #asyncio.create_task(self.test(name))
        
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
