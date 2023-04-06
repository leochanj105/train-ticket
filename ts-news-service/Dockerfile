FROM mrrm/web.go


RUN mkdir -p /app
WORKDIR /app

ADD ./opentelemetry-javaagent.jar /app/
ADD ./src/main/main.go /app/
RUN go build
CMD [ "./app" ]

EXPOSE 12862