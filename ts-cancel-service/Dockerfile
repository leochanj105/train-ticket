FROM amazoncorretto:8-alpine-jre

RUN /bin/ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

ADD ./target/ts-cancel-service-1.0.jar /app/
CMD ["java", "-Xmx200m",  "-jar", "/app/ts-cancel-service-1.0.jar"]

EXPOSE 18885