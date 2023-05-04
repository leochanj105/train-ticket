import os
import json
import numpy as np
import pandas as pd
import asyncio

class Analyzer():
    def __init__(self):
        self.raw_data = None
        self.trace_data = pd.DataFrame()     
        self.outlier_function = []

    def LoadRawData(self, dir):
        f = open(dir)
        self.raw_data = json.load(f)
        f.close()

    def GetTraceID(self):
        return self.raw_data["traceID"]
    
    def GetSpans(self):
        return self.raw_data["spans"]

    def GetProcesses(self):
        return self.raw_data["processes"]
    
    def GetWarnings(self):
        return self.raw_data["warnings"]

    def ParseSpans(self):
        spans = self.raw_data["spans"]
        # traceID
        # spanID
        # operationName
        # references
        # startTime
        # duration
        # tags
        # logs
        # processID
        # warnings

        entry = ""
        entry_dur = 0

        ops = ["TraceID"]
        durs = [self.GetTraceID()]
        for span in spans:
            dur = span["duration"]
            op = span["operationName"]
            logs = span["logs"]
            if logs != []:
                print(op, len(logs))
            if op not in ops:
                ops.append(op)
                durs.append(dur)
            if dur > entry_dur:
                entry = op
                entry_dur = dur

        ops.append("Entry")
        durs.append(entry)
        ops.append("Latency")
        durs.append(entry_dur)

        temp = pd.DataFrame([durs], columns = ops)
        if self.raw_data['traceID'] not in self.trace_data:
            self.trace_data = pd.concat([self.trace_data, temp], ignore_index = True)

        return

    def Analyze(self):
        self.outlier_function = []
        grouped_data = self.trace_data.groupby('Entry')
        for group in grouped_data:
            entry = group[0]
            data = group[1]

            # Find out slow requests
            latency = data['Latency']
            mean, stdev = np.mean(latency), np.std(latency)

            # 95% confidence interval
            outliers = np.abs(latency[:]-mean > 1.96 * stdev)
            baseline = data[outliers]["TraceID"].to_string(index=False)

            # For each ops, find outliers
            meta_columns = ["Entry", "Latency", "TraceID"]
            for c in data.columns:
                if c in meta_columns:
                    continue
                c_data = data[c]
                c_mean, c_stdev = np.mean(c_data), np.std(c_data)

                c_outliers = np.abs(c_data[:]-c_mean > 1.96 * c_stdev)

                # if the function identifies same outlier requests as slow requests, the function is considered as problematic
                if baseline == data[c_outliers]["TraceID"].to_string(index=False):
                    if "." in c:
                        self.outlier_function.append(c)
    
    async def run(self):
        print("run analyzer")
        while True:
            try:
                service = "ts-seat-service"
                traces = os.listdir("/app/lumos/" + service)

                for trace in traces:
                    self.LoadRawData("/app/lumos/" + service + "/" + trace)
                    self.ParseSpans()

                self.Analyze()
                print(self.outlier_function)
                await asyncio.sleep(10)
            
            except:
                print("analysis failed, waiting")
                await asyncio.sleep(10)
    


# if __name__ == '__main__':
#     a = Analyzer()
#     asyncio.run(a.run())