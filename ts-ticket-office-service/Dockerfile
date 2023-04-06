FROM node

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

RUN mkdir -p /app
WORKDIR /app

ADD ./opentelemetry-javaagent.jar /app/
ADD ./node_modules /app/node_modules
ADD ./opentelemetry-javaagent.jar /app/
ADD ./package.json /app/
ADD ./opentelemetry-javaagent.jar /app/
ADD ./public /app/public
# RUN npm install

ADD ./opentelemetry-javaagent.jar /app/
ADD ./bin /app/bin
ADD ./opentelemetry-javaagent.jar /app/
ADD ./app.js /app/
CMD [ "npm", "start" ]

EXPOSE 16108