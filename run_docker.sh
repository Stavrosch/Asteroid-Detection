#!/bin/bash

APP_NAME="gui_app"
PORT=6080

echo "🌍 Access the GUI in your browser at: http://localhost:$PORT"

docker run -it \
    --rm \
    -p 5901:5901 \
    -p ${PORT}:${PORT} \
    --name ${APP_NAME} \
    ${APP_NAME}
