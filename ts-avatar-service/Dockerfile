FROM python:3.8

RUN /bin/ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

RUN apt update -y
RUN apt install -y cmake
RUN apt install -y libgl1-mesa-glx

ENV PYTHONUNBUFFERED=TRUE

RUN mkdir -p /app
ADD . /app/
WORKDIR /app
# RUN ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install --upgrade numpy
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:17001", "app:app"]

EXPOSE 17001