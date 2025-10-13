FROM python:3.11-slim-bullseye

ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOME=/home/docker \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PATH=/home/docker/.local/bin:/usr/local/bin:$PATH

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc gfortran git wget curl ca-certificates pkg-config \
    libblas-dev liblapack-dev libatlas-base-dev \
    libfreetype6-dev libpng-dev \
    libx11-6 libxrender1 libxext6 libsm6 libgl1-mesa-glx libgl1-mesa-dri \
    libxrandr2 libxss1 libxcursor1 libxinerama1 libglib2.0-0 \
    tk tcl python3-tk \
    x11-utils xvfb xauth procps \
    && rm -rf /var/lib/apt/lists/*

# 🔑 Add UID/GID mapping here
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID docker && \
    useradd -m -u $UID -g $GID -s /bin/bash docker && \
    chown -R docker:docker /home/docker

# Copy requirements and install
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy app
WORKDIR /home/docker/app
COPY --chown=docker:docker . /home/docker/app

# Entrypoint scripts
COPY entrypoint.sh /home/docker/entrypoint.sh
COPY startup.sh /home/docker/startup.sh
RUN chmod +x /home/docker/entrypoint.sh /home/docker/startup.sh \
    && chown docker:docker /home/docker/entrypoint.sh /home/docker/startup.sh

# Switch to non-root user
USER docker
WORKDIR /home/docker/app

ENTRYPOINT ["/home/docker/entrypoint.sh"]
