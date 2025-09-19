#!/usr/bin/env bash
set -euo pipefail

# TODO: Add support for X11 forwarding

# If DISPLAY is set and /tmp/.X11-unix exists, we assume host X forwarding is intended.
if [ -n "${DISPLAY-}" ] && [ -d /tmp/.X11-unix ]; then
  echo "Using host X11 display: ${DISPLAY}"
  # If XAUTHORITY not provided, try copying from /root or create .Xauthority for user
  if [ -z "${XAUTHORITY-}" ]; then
    # try to use host user's .Xauthority if mounted
    if [ -f /tmp/.docker_xauth ]; then
      export XAUTHORITY=/tmp/.docker_xauth
    else
      # no explicit xauth file — warn user (they may run xhost +local:docker on host)
      echo "Warning: no XAUTHORITY file found. If GUI apps fail, run on the host: xhost +local:docker"
    fi
  fi
else
  # Fallback to virtual framebuffer for headless use
  echo "No host X11 detected. Starting Xvfb on :99 (headless mode)."
  export DISPLAY=":99"
  # start Xvfb in background
  Xvfb :99 -screen 0 1280x800x24 >/dev/null 2>&1 &
fi

# Run the passed command (or default CMD)
if [ $# -eq 0 ]; then
  exec bash
else
  exec "$@"
fi
