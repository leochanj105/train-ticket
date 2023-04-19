
# Train Ticket：A Benchmark Microservice System

The project is a train ticket booking system based on microservice architecture which contains 41 microservices. The programming languages and frameworks it used are as below.
- Java - Spring Boot, Spring Cloud
- Node.js - Express
- Python - Django
- Go - Webgo
- DB - Mongo、MySQL

You can get more details at [Wiki Pages](https://github.com/FudanSELab/train-ticket/wiki).

## Service Architecture Graph
![architecture](./image/2.png)

## Quick Start

#### Presequisite
* Docker
* Docker Compose

#### 1. Clone the Repository
```bash
git clone https://github.com/leochanj105/train-ticket
cd train-ticket/
git checkout old
git pull
```

#### 2. Install docker and docker compose 
(for Ubuntu 18.04, skip if you know how/already installed)
```bash
sudo apt-get update
sudo apt install docker.io
sudo apt install docker-compose
sudo apt install maven
sudo apt-get install openjdk-8-jdk
```
In case your system previously have other versions of java, run the following and choose java-8
```bash
sudo update-alternatives --config java
```
Optional: you may want to reconfigure the path where you docker images are saved:
create a JSON file /etc/docker/daemon.json with the content pointing to the new storage location:
```
{
"data-root": "/mnt/newlocation"
}
```
Then restart Docker:
```bash
sudo systemctl restart docker
```

#### 3. Build service jars (original)
```bash
sudo mvn clean package -Dmaven.test.skip=true
```

#### 4. Pull certain Docker images
Since the original benchmark use older version of some dependency images, we need to pull and tag them manually
Do the following:
```bash
docker pull python:3.8
docker pull mysql:5.7
docker pull mongo:5.0.0
docker pull openjdk:8
docker image tag python:3.8 python:3
docker image tag mysql:5.7 mysql:latest
docker image tag mongo:5.0.0 mongo:latest
docker image tag openjdk:8 java:8-jre
```

#### 5a. Enable OTLP+LUMOS instrumentation
If you want don't want to include instrumentation, simply goes to the next step.
Note: this will modify many files, so you may want to create a new branch if you want to keep an original version.
Build LumosAgent and copy jars:
```bash
bash setup.sh
```

Modify Dockerfiles to run with the opentelemtry instrumentation (do not run this under `controller` branch):
```bash
python3 mod.py
```

#### 5b. Build images
Build images:
```bash
sudo make build-image
```

#### 5c. Build Lumos controller
```bash
cd lumos && docker build -t lumos .
```

### 5d, Run Preprocesser
```bash
apt install python3.8-dev
python3.8 -m pip install javalang
cd lumos/preprocesser && python3.8 train-ticket-parser.py
```
You need to change the train-ticket project dir in `train-ticket-parser.py`. This will generate `coarse_block.lms` and `fine_block.lms`, each contains pairs of tracepoints.

#### 6. Start the Application
If you setup for opentemetry, you need to also start a collector service and a jaeger service.
To do so, just uncomment the last two services under the name "jaeger-service" and "collecter".

Also, since you want to use your compiled version of images, set the following environments (do not run these exports under `controller` branch):

```bash
export IMG_REPO=test
export NAMESPACE=test
export IMG_TAG=latest
export TAG=latest
```

To start the application, just do:
```bash
docker-compose up -d
```


Once the application starts, you can visit the Train Ticket web page at [http://localhost:8080](http://localhost:8080).

The jaeger agent is at http://localhost:16686


