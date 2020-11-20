#!/bin/bash
app="docker.test"
docker build -t ${app} .
docker-compose  up