#!/usr/bin/env python

import os
import json
import requests

JAEGER_TRACES_ENDPOINT = "http://localhost:16686/api/traces?limit=20000&"
JAEGER_TRACES_PARAMS = "service="

def get_traces(service):
    """
    Returns list of all traces for a service
    """
    url = JAEGER_TRACES_ENDPOINT + JAEGER_TRACES_PARAMS + service
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise err

    response = json.loads(response.text)
    traces = response["data"]
    return traces

JAEGER_SERVICES_ENDPOINT = "http://localhost:16686/api/services"

def get_services():
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

def write_traces(directory, traces):
    """
    Write traces locally to files
    """
    for trace in traces:
        # traceID, spans, processes, warnings
        if len(trace["spans"]) < 20:
            pass
        traceid = trace["traceID"]
        print(traceid)
        
        for span in trace["spans"]:
            for item in span:
                try:
                    print(item, len(span[item]))
                    print(span[item][0])
                except:
                    pass
            break

        # traceID,spanID,operationName,references,startTime,duration,tags,logs,processID,warnings
        # print(len(trace["spans"][0]))

        # print(trace["processes"])
        
        # path = directory + "/" + traceid + ".json"
        # with open(path, 'w') as fd:
        #     fd.write(json.dumps(trace))
        
        break




if __name__ == '__main__':
    services = get_services()
    # Pull traces for all the services & store locally as json files
    for service in services:
        #print(service)
        if service != "ts-travel-service":
            continue
        if not os.path.exists(service):
            os.makedirs(service)
        traces = get_traces(service)
        write_traces(service, traces)