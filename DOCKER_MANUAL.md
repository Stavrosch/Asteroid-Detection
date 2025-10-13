# 🔭 Astro-GUI Docker

This Docker image bundles Python + Astropy + GUI support for running astronomy apps with `customtkinter`, `matplotlib`, `photutils`, and more.

The image is built from the [Asteroid-Detection](https://github.com/Stavrosch/Asteroid-Detection) repository.

## 🚀 Quickstart

### 🛠️ Build the image

```bash
docker build \
  --build-arg UID=$(id -u) \
  --build-arg GID=$(id -g) \
  -t astro-gui .
```

### 🏁 Run the image

```bash
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd):/home/docker/app \
  astro-gui
```

### 📦 Inside the container

```bash
./startup.sh
```

The image is based on [Python 3.11](https://hub.docker.com/_/python).

Disclaimer: This method is experimental and may not work as expected. Please report any issues to [GitHub](https://github.com/Stavrosch/Asteroid-Detection/issues) if you encounter any problems or have suggestions for improvement. Alternatively, you can contact me directly at [mchadolias](https://github.com/mchadolias).
