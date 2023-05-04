#!/bin/bash

docker pull python:3.8
docker pull mysql:5.7
docker pull mongo:5.0.0
docker pull openjdk:8
docker image tag python:3.8 python:3
docker image tag mysql:5.7 mysql:latest
docker image tag mongo:5.0.0 mongo:latest
docker image tag openjdk:8 java:8-jre
bash setup.sh
python3 mod.py
