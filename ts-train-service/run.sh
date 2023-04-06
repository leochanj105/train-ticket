#!/bin/bash

python3 -u /app/agent.py &
java -javaagent:/app/opentelemetry-javaagent.jar -Dotel.service.name=ts-train-service -Dotel.exporter.otlp.endpoint=http://collector:4317 -Xmx200m -jar /app/ts-train-service-1.0.jar