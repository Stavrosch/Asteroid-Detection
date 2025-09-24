FROM python:3.11-slim-bullseye

ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOME=/home/docker \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PATH=/home/docker/.local/bin:/usr/local/bin:$PATH

# -----------------------------
# System dependencies
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc gfortran git wget curl ca-certificates pkg-config \
    libblas-dev liblapack-dev libatlas-base-dev \
    libfreetype6-dev libpng-dev \
    libx11-6 libxext6 libxrender1 libsm6 \
    python3-tk tk tcl \
    x11-utils xauth xvfb \
    procps \
    gzip \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Non-root user
# -----------------------------
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID docker && \
    useradd -m -u $UID -g $GID -s /bin/bash docker && \
    chown -R docker:docker /home/docker

# -----------------------------
# Python dependencies
# -----------------------------
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# -----------------------------
# App code
# -----------------------------
WORKDIR /home/docker/app
COPY --chown=docker:docker . /home/docker/app

# -----------------------------
# Download public data during build
# -----------------------------
RUN mkdir -p GUIs/Utilities && \
    wget -q -O GUIs/Utilities/MPCORB.DAT.gz http://minorplanetcenter.net/iau/MPCORB/MPCORB.DAT.gz && \
    gunzip -f GUIs/Utilities/MPCORB.DAT.gz && \
    wget -q -O GUIs/Utilities/astorb.dat.gz https://ftp.lowell.edu/pub/elgb/astorb.dat.gz && \
    gunzip -f GUIs/Utilities/astorb.dat.gz && \
    # Preprocess with pickler.py
    python GUIs/Utilities/pickler.py


# -----------------------------
# Entrypoint + scripts
# -----------------------------
COPY entrypoint.sh /home/docker/entrypoint.sh
COPY startup.sh /home/docker/startup.sh
RUN chmod +x /home/docker/entrypoint.sh /home/docker/startup.sh \
    && chown docker:docker /home/docker/entrypoint.sh /home/docker/startup.sh

# -----------------------------
# Switch to non-root
# -----------------------------
USER docker
WORKDIR /home/docker/app

# -----------------------------
# Entrypoint + default CMD
# -----------------------------
ENTRYPOINT ["/home/docker/entrypoint.sh"]
CMD ["./startup.sh"]
