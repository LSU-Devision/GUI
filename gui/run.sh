#!/bin/bash
IMAGE_NAME=gui

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

if ! command_exists docker; then
    echo "Installing docker, please wait..."

    # Install Docker
    curl -fsSL https://get.docker.com | sudo bash
    sudo usermod -aG docker $USER

    echo "Docker installed..."
fi

if ! pgrep -x "dockerd" > /dev/null; then
    echo "Initializing docker..."
    sudo systemctl start docker
fi


if docker inspect --type=image $IMAGE_NAME > /dev/null 2>&1; then
    #Image exists
    echo "Running Program"
else
    #Image doesn't exist
    echo "Installing docker image, please wait"
    docker load -i vm.tar
    echo "Running Program"
fi

xhost +local:docker
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix  -v "$(pwd)/excel":/app/excel -v "$(pwd)/config":/app/config -v "$(pwd)/images":/app/images -v "$(pwd)/annotations":/app/annotations/ gui