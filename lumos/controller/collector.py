#!/usr/bin/env python

import os
import json
import requests
import asyncio

JAEGER_ADDR = "c220g1-030623.wisc.cloudlab.us"

JAEGER_TRACES_ENDPOINT = f"http://{JAEGER_ADDR}:16686/api/traces?limit=20000&"
JAEGER_TRACES_PARAMS = "service="
JAEGER_SERVICES_ENDPOINT = f"http://{JAEGER_ADDR}:16686/api/services"

class Collector:
    def __init__(self):
        return



    def get_traces(self, service):
        """
        Returns list of all traces for a service
        """
        url = JAEGER_TRACES_ENDPOINT + JAEGER_TRACES_PARAMS + service
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err

        # json_string = ""
        # for chunk in response.iter_content(chunk_size=1024):
        #     if chunk:
        #         try:
        #             json_string += chunk.decode()
        #         except UnicodeDecodeError as e:
        #             # Log the error and continue processing the response
        #             print(f"Error decoding chunk: {e}")
        # traces = json.loads(json_string)["data"]

        response = json.loads(response.text)
        traces = response["data"]

        return traces

    def get_services(self):
        """
        Returns list of all services
        """
        try:
            response = requests.get(JAEGER_SERVICES_ENDPOINT)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err
            
        response = json.loads(response.text)
        services = response["data"]
        return services

    def write_traces(self, directory, traces):
        """
        Write traces locally to files
        """
        print("write traces")
        for trace in traces:
            # traceID, spans, processes, warnings
            if len(trace["spans"]) < 20:
                pass
            traceid = trace["traceID"]
            
            path = directory + "/" + traceid + ".json"
            with open(path, 'w') as fd:
                fd.write(json.dumps(trace))
        
    async def run(self):
        print("run collector")
        while True:
            try:
                services = self.get_services()

                for service in services:
                    if service != "ts-seat-service":
                        continue
                    data_path = "/app/lumos/"+service
                    if not os.path.exists(data_path):
                        os.makedirs(data_path)
                    traces = self.get_traces(service)
                    self.write_traces(data_path, traces)
                    await asyncio.sleep(10)
            except:
                print("collection failed, waiting")
                await asyncio.sleep(10)




# if __name__ == '__main__':
#     c = Collector()
#     asyncio.run(c.run())
