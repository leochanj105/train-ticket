import asyncio
import websockets
import argparse
import sys
import time
from threading import Thread
import json

#testarray = ['c,travel.service.TravelServiceImpl,query,io.opentelemetry.api.trace.Span.current().addEvent(\"[LUMOS] HELLO!!!!!!!!\");,158']
testarray = ['s, seat.service.SeatServiceImpl, distributeSeat']
timingarray = [("seat.service.SeatServiceImpl", "distributeSeat", 185,194)]
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
    def timingtps(self, arr):
        tps = "tps: ["
        for i, (cname, method, line1, line2) in enumerate(arr):
            timerstart = f"io.opentelemetry.api.trace.Span.current().addEvent(\"start\"+{self.id} + seat  +\": \"+ System.currentTimeMillis());"
            #timerstart = f"start{i} = System.currentTimeMillis();"
            #timerstop = f"long finish{i} = System.currentTimeMillis(); "
            timerstop = f"io.opentelemetry.api.trace.Span.current().addEvent(\"end\"+{self.id} +\": \"+ System.currentTimeMillis());"
            #tptiming = self.timingtp(cname, method, line1, line2)
            tpstart = self.codetp(cname, method, timerstart, line1)
            tpstop = self.codetp(cname, method, timerstop, line2)

            #tps += "{" + tpdec + "},"
            tps += "{" + tpstart + "},"
            tps += "{" + tpstop + "},"
        tps += "]"
        msg = "{type:add, " + tps + "}"
        return msg


    def gettps(self, arr):
        tps = "tps: ["
        for tp in arr:
            strs = tp.split(",")
            tp = ""
            if(strs[0] == "c"):
                tp = self.codetp(strs[1], strs[2], strs[3], strs[4])
            else:
                tp = self.spantp(strs[1], strs[2])
            tps += "{" + tp + "},"
        tps += "]"
        msg = "{type:add, " + tps + "}"
        return msg
    def timingtp(self, cname, method, line1, line2):
        newid = self.id
        self.id += 1
        return f"id:'{newid}', cname:{cname}, method:{method}, tptype:timing, line1:{line1}, line2:{line2}"
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
        seconds = 5
        try:
            for i in range(seconds):
                print(seconds - i)
                await asyncio.sleep(1)

            msg = self.gettps(testarray)
            await conn.send(msg)
            print(f"> {msg}")
            msg = self.timingtps(timingarray)
            await conn.send(msg)
            print(f"> {msg}")
        except websockets.ConnectionClosedOK:
            pass


    async def handler(self, conn):
        name = await conn.recv()
        self.connections[name] = conn
        print(f"< {name}")
        #asyncio.create_task(self.test(name))
        
        if "ts-seat-service" in name:
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
