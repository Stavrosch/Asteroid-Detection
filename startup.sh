#!/usr/bin/env bash
set -e

# -----------------------------
# Step 1: Set up API key for Astrometry.net
# -----------------------------
ENV_FILE=".env"
URL="http://nova.astrometry.net/api_help"

echo "------------------------------------------------------"
echo "Please log in and copy your API key from the website."
echo "Checking if API key is set..."

if [ -f "$ENV_FILE" ] && grep -q "ASTROMETRY_API_KEY" "$ENV_FILE"; then
    echo "✅ Your .env file already contains the API key."
elif [ -n "$ASTROMETRY_API_KEY" ]; then
    echo "✅ The API key is already set as an environment variable."
    if [ -f "$ENV_FILE" ]; then
        if grep -q "ASTROMETRY_API_KEY" "$ENV_FILE"; then
            sed -i "s/^ASTROMETRY_API_KEY=.*/ASTROMETRY_API_KEY=$ASTROMETRY_API_KEY/" "$ENV_FILE"
        else
            echo "ASTROMETRY_API_KEY=$ASTROMETRY_API_KEY" >> "$ENV_FILE"
        fi
    fi
else
    echo "❌ The API key is not set."
    echo "Please visit: $URL to get your API key"
    
    if [ -t 0 ]; then
        echo "Paste your API key here and press Enter:"
        read -r API_KEY

        if [ -z "$API_KEY" ]; then
            echo "❌ No API key entered. Aborting."
            exit 1
        fi

        echo "ASTROMETRY_API_KEY=$API_KEY" >> "$ENV_FILE"
        echo -e "✅ Done - Your .env file now contains the API key.\n"
    else
        echo "❌ Running in non-interactive mode without API key. Aborting."
        exit 1
    fi
fi  

# -----------------------------
# Step 2: Download and process data files
# -----------------------------
DATA_DIR="GUIs/Utilities"
mkdir -p "$DATA_DIR"

MAX_ATTEMPTS=4
ATTEMPT=0

download_file () {
    url=$1
    filename=$2
    if command -v wget &>/dev/null; then
        wget -O "$filename" "$url"
    elif command -v curl &>/dev/null; then
        curl -L -o "$filename" "$url"
    else
        echo "❌ Neither wget nor curl found."
        exit 1
    fi
}

if [ -f "$DATA_DIR/MPCORB.DAT" ] && [ -f "$DATA_DIR/astorb.dat" ]; then
    echo "✅ Data files already exist. Skipping download."
else
    while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
        echo "------------------------------------------------------"
        echo " Downloading data files (attempt $((ATTEMPT+1))/$MAX_ATTEMPTS)..."

        download_file "http://minorplanetcenter.net/iau/MPCORB/MPCORB.DAT.gz" "MPCORB.DAT.gz"
        download_file "https://ftp.lowell.edu/pub/elgb/astorb.dat.gz" "astorb.dat.gz"

        if [ -f "MPCORB.DAT.gz" ] && [ -f "astorb.dat.gz" ]; then
            echo " Decompressing data files..."
            gunzip -f MPCORB.DAT.gz
            gunzip -f astorb.dat.gz

            mv MPCORB.DAT "$DATA_DIR/"
            mv astorb.dat "$DATA_DIR/"

            echo "✅ The data files have been downloaded successfully."
            break
        else 
            ATTEMPT=$((ATTEMPT + 1))
            if [ $ATTEMPT -lt $MAX_ATTEMPTS ]; then
                echo "❌ Download failed. Retrying in 5 seconds..."
                sleep 5
            else
                echo "❌ Download failed $MAX_ATTEMPTS times."
                if [ -t 0 ]; then
                    echo "Please download manually into $DATA_DIR"
                    read -p "Press Enter to continue..." dummy
                else
                    exit 1
                fi
            fi
        fi
    done
fi

if [ -f "$DATA_DIR/MPCORB.DAT" ] && [ -f "$DATA_DIR/astorb.dat" ]; then
    echo " Processing data files..."
    python GUIs/Utilities/pickler.py
else
    echo "❌ Required data files missing."
    exit 1
fi

echo "✅ Setup complete."

# -----------------------------
# Step 3: Run the app
# -----------------------------
exec python GUIs/GUI_main.py
