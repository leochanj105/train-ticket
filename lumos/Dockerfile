FROM python:3.8

ADD ./controller /app/lumos/
RUN pip3 install websockets

CMD ["python3", "-u", "/app/lumos/controller.py"]

EXPOSE 8765