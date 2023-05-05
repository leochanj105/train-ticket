FROM java:8-jre

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

ADD ./target/ts-preserve-service-1.0.jar /app/
ADD ./opentelemetry-javaagent.jar /app/
ADD ./LumosAgent-jar-with-dependencies.jar /app/
CMD ["java", "-javaagent:/app/opentelemetry-javaagent.jar", "-Dotel.service.name=ts-preserve-service", "-Dotel.exporter.otlp.endpoint=http://c220g1-030623.wisc.cloudlab.us:4317", "-Xmx200m",  "-jar", "/app/ts-preserve-service-1.0.jar"]

EXPOSE 14568