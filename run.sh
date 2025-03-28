#!/bin/bash
xhost +local:docker
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix gui -v "$(pwd)/output":/app/output -v "$(pwd)/config":/app/config