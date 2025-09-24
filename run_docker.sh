#!/usr/bin/env bash
set -e

# ================================
# Configurable variables
# ================================
## TODO: Image to be changed after testing to the original developer of the project stavrosch
DOCKER_IMAGE=${DOCKER_IMAGE:-mchadolias/astro-gui:test} 
WORKDIR=/home/docker/app


echo -e "
############# Astro-GUI Docker  ############ 
Starting Docker container 🚀
Docker image: $DOCKER_IMAGE 
Working directory: $WORKDIR 
############################################

To access the container, run:\n \

docker run -it --rm 
    -e DISPLAY=$DISPLAY 
    -v /tmp/.X11-unix:/tmp/.X11-unix 
    -v $(pwd):$WORKDIR 
    $DOCKER_IMAGE

This command will start with the startup.sh script in the container, which will check for an API key and run the GUI.

Otherwise, you can run the container in bash mode:

docker run -it --rm 
    -e DISPLAY=$DISPLAY 
    -v /tmp/.X11-unix:/tmp/.X11-unix 
    -v $(pwd):$WORKDIR 
    $DOCKER_IMAGE bash

You can also mount a .env file to persist the API key by adding the following option:

    -v $(pwd)/.env:$WORKDIR/.env  
    --env-file .env

To quit the container, press Ctrl+C.

You can find more information about the program in the README.md file inside the container or the GitHub repository.
Regarding the Docker image, you can check the DOCKER_MANUAL.md file.
For more information, visit https://github.com/stavrosch/Asteroid-Detection
Please report any issues at https://github.com/stavrosch/Asteroid-Detection/issues

Have fun! 🚀 🔭•🪐•☄️   
"


# Allow local docker containers to use your X server
xhost +local:docker

# ================================
# Run the container
# ================================

docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -e ASTROMETRY_API_KEY="test" \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$(pwd)/.env:$WORKDIR/.env" \
    --env-file .env \
    $DOCKER_IMAGE "$@"

# ================================
# Cleanup
# ================================
xhost -local:docker