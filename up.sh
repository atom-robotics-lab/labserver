#!/bin/bash
# docker compose build  &
xhost +si:localuser:$USER &
xhost +local:docker &
export DISPLAY=$DISPLAY &
docker-compose up  &
exec bash
