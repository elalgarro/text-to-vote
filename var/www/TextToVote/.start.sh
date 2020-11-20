#!/bin/bash
app="aalgard/text_to_vote"
docker build -t ${app} .
docker-compose  up