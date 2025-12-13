#!/bin/sh
set -e

# -----------------------------
# Configuration
# -----------------------------
DATA_DIR="${DATA_DIR:-data/}"
ENV_FILE=".env"

echo "🚀 Starting application..."
echo "📁 Using data directory: $DATA_DIR"

# -----------------------------
# Step 1: Check mounted data directory
# -----------------------------
if [ ! -d "$DATA_DIR" ]; then
    echo "⚠️ Data directory $DATA_DIR does not exist."
    echo "   Did you forget to mount it? (-v <host_dir>:/data)"
else
    echo "✅ Data directory mounted."
fi

# Ensure it exists (for first run)
mkdir -p "$DATA_DIR"

# -----------------------------
# Step 2: Check API key
# -----------------------------
if [ -n "${ASTROMETRY_API_KEY-}" ]; then
    echo "✅ ASTROMETRY_API_KEY found in environment."
    if [ ! -f "$ENV_FILE" ]; then
        echo "ASTROMETRY_API_KEY=$ASTROMETRY_API_KEY" > "$ENV_FILE"
    fi
elif [ -f "$ENV_FILE" ] && grep -q "ASTROMETRY_API_KEY" "$ENV_FILE"; then
    echo "✅ ASTROMETRY_API_KEY found in .env"
else
    echo "⚠️ ASTROMETRY_API_KEY not set!"
    echo "   Provide it via -e ASTROMETRY_API_KEY or mount a .env file."
    echo "   The GUI may not work without a valid API key."
fi

# -----------------------------
# Step 3: Launch the GUI
# -----------------------------
echo " 🖥️ Launching GUI..."
exec python GUI/GUI_main.py
