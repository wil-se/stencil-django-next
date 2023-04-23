#!/bin/bash

git pull
# docker build -t backend-casino ./backend
# docker run -p 8000:8000 -t backend-casino
docker compose build
docker compose up