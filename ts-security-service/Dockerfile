FROM java:8-jre

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

ADD ./opentelemetry-javaagent.jar /app/
ADD ./target/ts-security-service-1.0.jar /app/
CMD ["java", "-javaagent:/app/opentelemetry-javaagent.jar", "-Dotel.service.name=ts-security-service", "-Dotel.exporter.otlp.endpoint=http://collector:4317", "-Xmx200m",  "-jar", "/app/ts-security-service-1.0.jar"]

EXPOSE 11188