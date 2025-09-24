# 🔭 Astro-GUI Docker 🐳

This Docker image provides a dedicated application for **asteroid detection**, developed in the context of a Master’s thesis by [@Stavrosch](https://github.com/Stavrosch). The application is written in **Python** and features a user-friendly GUI for its operation.  

The image is built from the [Asteroid-Detection](https://github.com/Stavrosch/Asteroid-Detection) repository.

---

## 🚀 Quickstart

### Image creation

#### Option 1: 🛠️ Build the image

You can build the image locally using the provided `Dockerfile`:

```bash
docker build \
  --build-arg UID=$(id -u) \
  --build-arg GID=$(id -g) \
  -t <your-image-name> .
```

#### Option 2: 📦 Pull the image

**ATTENTION**: Pre-built images are currently unavailable as this feature is under development.

When available, you will be able to pull them from GitHub or Docker Hub:

```bash
# 1st github option
docker pull ghcr.io/stavrosch/asteroid-detection:<tag>

# 2nd option Dockerhub
docker pull mchadolias/asteroid-detection
```

### 🏁 Run the image

The default entrypoint (`startup.sh`) checks for your API key and launches the GUI (`GUI_main.py`).

Basic run command:

```bash
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd):/home/docker/app \
  <name-your-own-image>
```

Alternatively, you can use the helper script:

```bash
./run_docker.sh
```

For more information check the `run_docker.sh` script. If you are wondering how it works.

---

## 🧰 Dependencies

- Base image [Python 3.11-slim-bullseye](https://hub.docker.com/_/python)
- Additional Python packages for astronomy and GUI development.

---

## ⚠️ Disclaimer

This Docker setup is experimental and may not work as expected in all environments. Please report any issues or suggestions to [GitHub](https://github.com/Stavrosch/Asteroid-Detection/issues), or contact the docker developer directly at [@mchadolias](https://github.com/mchadolias) or the main developer [@Stavrosch](https://github.com/Stavrosch).
