#!/usr/bin/env bash
set -euo pipefail

ENV_FILE=".env"

# -----------------------------
# Step 1: Check API key
# -----------------------------
if [ -n "${ASTROMETRY_API_KEY-}" ]; then
    echo "✅ ASTROMETRY_API_KEY found in environment."
    # Optionally write to .env if you want it persisted in container
    if [ ! -f "$ENV_FILE" ]; then
        echo "ASTROMETRY_API_KEY=$ASTROMETRY_API_KEY" > "$ENV_FILE"
    fi
elif [ -f "$ENV_FILE" ] && grep -q "ASTROMETRY_API_KEY" "$ENV_FILE"; then
    echo "✅ ASTROMETRY_API_KEY found in .env"
else
    echo "⚠️ ASTROMETRY_API_KEY not set!"
    echo "Please provide it via -e ASTROMETRY_API_KEY or mount a .env file."
    echo "The GUI may not work without a valid API key."
fi

# -----------------------------
# Step 2: Run the GUI
# -----------------------------
exec python GUIs/GUI_main.py
