#!/bin/sh
set -e

echo "🚀 Starting Xvfb + noVNC..."

export DISPLAY=:1

# Virtual display
Xvfb :1 -screen 0 1280x800x16 &
sleep 1

# Window manager
fluxbox &
sleep 1

# VNC server
x11vnc -display :1 -forever -nopw -shared -listen 0.0.0.0 &
sleep 1

# noVNC frontend
websockify --web=/usr/share/novnc/ 6080 0.0.0.0:5900 &

echo "✅ noVNC ready at http://localhost:6080"

# Execute CMD (startup.sh)
exec "$@"
