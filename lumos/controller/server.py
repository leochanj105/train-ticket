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

testfile = "seat.service.SeatServiceImpl"
testmethod = "distributeSeat"

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
        self.coarse_blocks = {}
        self.fine_blocks = {}
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
    def removetps(self, tpids):
        tps = ["{id: '" + tpid + "'}, " for tpid in tpids]
        tpstr = "["
        for tp in tps:
            tpstr += tp
        tpstr += "]"
        msg = "{type:remove, tps:" + tpstr + "}"
        return msg
    def parse_tps_file(self, data, tptype):
        service = ""
        fname = ""
        for line in data:
            if ".java" in line:
                temp = line.split("\n")[0].split("/")
                if "train-ticket" in temp:
                    service = temp[temp.index("train-ticket")+1]
                    fname = ""
                    for i in range(temp.index("java")+1, len(temp)-1):
                        fname += temp[i]
                        fname += "."
                    fname += temp[-1].split(".java")[0]
                if tptype == "c":
                    if service not in self.coarse_blocks:
                        self.coarse_blocks[service] = {}
                    self.coarse_blocks[service][fname] = {}
                elif tptype == "f":
                    if service not in self.fine_blocks:
                        self.fine_blocks[service] = {}
                    self.fine_blocks[service][fname] = {}

            else:
                temp = line.split("\n")[0].split(" ")
                method_name = temp[0]
                s = int(temp[1])
                e = int(temp[2])

                if tptype == "c":
                    if method_name not in self.coarse_blocks[service][fname]:
                        self.coarse_blocks[service][fname][method_name] = []
                    self.coarse_blocks[service][fname][method_name].append((s, e))
                elif tptype == "f":
                    if method_name not in self.fine_blocks[service][fname]:
                        self.fine_blocks[service][fname][method_name] = []
                    self.fine_blocks[service][fname][method_name].append((s, e))
        
        return

    def get_tps(self):
        for service in self.coarse_blocks:
            for fname in self.coarse_blocks[service]:
                if testfile == fname:
                    for method in self.coarse_blocks[service][fname]:
                        if testmethod == method.split("_")[0]:
                            return self.coarse_blocks[service][fname][method]

    def load_tps_file(self, tp_dir):
        coarse = open(tp_dir + "coarse_blocks.lms", "r")
        data = coarse.readlines()
        coarse.close()
        self.parse_tps_file(data, "c")

        fine = open(tp_dir + "fine_blocks.lms", "r")
        data = fine.readlines()
        fine.close()
        self.parse_tps_file(data, "f")

        return


    async def test(self, name):
        conn = self.connections[name]
        seconds = 5
        # try:
        #     for i in range(seconds):
        #         print(seconds - i)
        #         await asyncio.sleep(1)

        #     testarray = ['s,'+testfile+','+testmethod]
        #     msg = self.gettps(testarray)
        #     await conn.send(msg)
        #     print(f"> {msg}")
            
        #     tps = self.get_tps()
        #     for tp in tps:
        #         timingarray = [(testfile, testmethod, tp[0], tp[1])]
        #         msg = self.timingtps(timingarray)
        #         await conn.send(msg)
        #         print(f"> {msg}")

        # except websockets.ConnectionClosedOK:
        #     pass

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
                       
            for i in range(120):
                print(120 - i)
                await asyncio.sleep(1)
            msg = self.removetps(["0", "1", "2"])
            print(f"> {msg}")
            await conn.send(msg)
        except websockets.ConnectionClosedOK:
            pass


    async def handler(self, conn):
        name = await conn.recv()
        self.connections[name] = conn
        print(f"< {name}")
        #asyncio.create_task(self.test(name))
        
        if "ts-seat-service" in name:
            await self.test(name)

    async def run(self, tp_dir):
        print("run server")
        self.load_tps_file(tp_dir)
        async with websockets.serve(self.handler, "0.0.0.0", 8765):
            await asyncio.Future()  # run forever


# if __name__ == '__main__':
#     s = Server()
#     s.load_tps_file("../preprocessor/")

#     s.get_tps()

#     testarray = ['s,'+testfile+','+testmethod]
#     msg = s.gettps(testarray)
#     print(msg)

#     tps = s.get_tps()
#     for tp in tps:
#         print(tp[0], tp[1])
#     timingarray = [(testfile, testmethod, 1, 2)]
#     msg = s.timingtps(timingarray)
#     print(msg)
