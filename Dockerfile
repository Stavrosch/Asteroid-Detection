FROM python:3.11-slim-bullseye

ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    DATA_DIR=/data

# -----------------------------
# System + GUI (noVNC) dependencies
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    # build tools (keep if you compile wheels)
    build-essential gcc gfortran pkg-config \
    # common runtime utils
    ca-certificates curl wget git procps \
    # GUI stack
    xvfb x11vnc fluxbox novnc websockify \
    # X11 libs often needed by GUI toolkits
    libx11-6 libxext6 libxrender1 libsm6 libice6 \
    libgl1 \
    # optional: Tkinter support (safe even if unused)
    python3-tk tk tcl \
    # fonts
    fonts-dejavu-core \
    # Windows CRLF fixer
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Python deps
# -----------------------------
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# -----------------------------
# App code + scripts
# -----------------------------
COPY *.md /app/
COPY GUIs/ /app/GUI/
COPY demo-fits/ /app/demo-fits/
COPY entrypoint.sh /app/entrypoint.sh
COPY startup.sh /app/startup.sh

# Ensure scripts are runnable on Linux (even if edited on Windows)
RUN dos2unix /app/entrypoint.sh /app/startup.sh \
    && chmod +x /app/entrypoint.sh /app/startup.sh

# Mounted runtime data directory (host bind mount recommended)
VOLUME ["/data"]

# noVNC web port
EXPOSE 6080

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["/app/startup.sh"]
