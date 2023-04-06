FROM java:8-jre

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

ADD ./opentelemetry-javaagent.jar /app/
ADD ./target/ts-train-service-1.0.jar /app/
ADD ./agent.py /app/
ADD ./run.sh /app/

RUN apt update
RUN apt install -y python3-pip
RUN pip3 install websockets

CMD ["bash", "/app/run.sh"]
# CMD ["java", "-javaagent:/app/opentelemetry-javaagent.jar", "-Dotel.service.name=ts-train-service", "-Dotel.exporter.otlp.endpoint=http://collector:4317", "-Xmx200m",  "-jar", "/app/ts-train-service-1.0.jar"]

EXPOSE 14567