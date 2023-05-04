FROM python:3.8

ADD ./controller /app/lumos/
ADD ./preprocessor /app/lumos/

RUN pip3 install websockets numpy pandas requests
RUN apt update
RUN apt install -y vim htop

CMD ["python3", "-u", "/app/lumos/controller.py"]

EXPOSE 8765