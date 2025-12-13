# 🔭 Astro-GUI Docker 🐳

[Back to README](README.md) • [Data preparation](DATA_PREPARATION.md)

This guide explains how to run the **Asteroid-Detection** GUI in Docker using **noVNC** (GUI in your browser). This approach avoids host-specific X11 setup and works consistently across Linux, macOS, and Windows hosts (Docker Desktop).

---

## 🚀 Quickstart

### 1) Build the image

From the project root (where the `Dockerfile` is):

```bash
docker build -t gui_app .
```

### 2) Prepare a data folder (recommended)

Create a local folder to persist downloaded/generated files:

```bash
mkdir -p data
```

### 3) Run the container

Mount your local `data/` to the container’s expected path (adjust if your app uses a different location):

```bash
docker run --rm -p 6080:6080 \
  -v "$PWD/data:/app/data" \
  gui_app
```

Then open:

- `http://localhost:6080/vnc.html`

> If you open `http://localhost:6080/` you may see a 404 depending on your noVNC package version; `vnc.html` is the safe entry point.

---

## 🔑 Astrometry.net API key

The application uses `ASTROMETRY_API_KEY` for online plate solving.

Choose one of the following:

### Option A: pass as an environment variable

```bash
docker run --rm -p 6080:6080 \
  -e ASTROMETRY_API_KEY="YOUR_KEY_HERE" \
  -v "$PWD/data:/app/data" \
  gui_app
```

### Option B: mount a `.env` file (recommended for non-interactive use)

Create a `.env` file next to your Dockerfile:

```env
ASTROMETRY_API_KEY=YOUR_KEY_HERE
```

Run:

```bash
docker run --rm -p 6080:6080 \
  -v "$PWD/data:/app/data" \
  -v "$PWD/.env:/app/.env:ro" \
  gui_app
```

---

## 🧰 Notes

- **Data files**: some tools require catalogue files (e.g. MPCORB and ASTORB). See [DATA_PREPARATION.md](DATA_PREPARATION.md).
- **Fullscreen**: open the noVNC side menu and use **Fullscreen**, and enable **Scaling**. If the virtual desktop is too small, increase the Xvfb resolution in `entrypoint.sh` (e.g. `1920x1080x24`).
- **Fedora host**: no special X11/Wayland steps are required with noVNC.

---

## ⚠️ Disclaimer

This Docker setup is experimental. Please report issues via the upstream repository’s issue tracker, or contact the docker developer directly.

*Docker Developer* [@mchadolias](https://github.com/mchadolias)
