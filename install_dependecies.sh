#!/bin/bash
set -e

# -----------------------------
# Detect Platform / WSL
# -----------------------------
OS="$(uname -s)"
if grep -qi microsoft /proc/version; then
    platform="wsl"
else
    case "$OS" in
        Linux*)     platform="linux";;
        Darwin*)    platform="mac";;
        *)          platform="unknown";;
    esac
fi
echo "Detected platform: $platform"

# -----------------------------
# Step 1: Environment setup
# -----------------------------
cat <<'EOF'
This script will install all dependencies and prepare the environment.

Steps:
1. Create a Python virtual environment or conda environment.
2. Install required dependencies.
3. Download and process data files.


------------------------------------------------------
Please enter your choice of environment:
- venv
- conda
EOF

read -p "Environment: " env_choice
echo "You chose: $env_choice"

if [ "$env_choice" = "venv" ]; then
    python3 -m venv .venv 
    if [ "$platform" = "wsl" ]; then
        source .venv/Scripts/activate
    else 
        source .venv/bin/activate
    fi
    pip install -r requirements.txt

elif [ "$env_choice" = "conda" ]; then
    read -p "Conda environment name: " conda_env_name
    echo "You chose: $conda_env_name"

    # Ensure conda is available
    if ! command -v conda &> /dev/null; then
        echo "conda not found. Please install Anaconda or Miniconda first (inside WSL if applicable)."
        exit 1
    fi

    # Fix conda activation in scripts
    eval "$(conda shell.bash hook)"

    conda create -y -n "$conda_env_name" python=3.12
    conda activate "$conda_env_name"
    pip install -r requirements.txt

else
    echo "Please choose either venv or conda"
    exit 1
fi

echo -e "✅ Environment setup complete. \n"

# -----------------------------
# Step 2: Set up API key for Astrometry.net
# -----------------------------
ENV_FILE=".env"
URL="http://nova.astrometry.net/api_help"

# Choose best browser opener
if [ "$platform" = "wsl" ] && command -v wslview &>/dev/null; then
    BROWSER="wslview"
elif [ "$platform" = "mac" ]; then
    BROWSER="open"
else
    BROWSER="xdg-open"
fi

echo "------------------------------------------------------"
echo "Please log in and copy your API key from the website."
echo "Checking if API key is set..."

if [ -f "$ENV_FILE" ] && grep -q "ASTROMETRY_API_KEY" "$ENV_FILE"; then
    echo "✅ Your .env file already contains the API key."
elif [ "$ASTROMETRY_API_KEY" ]; then
    echo "✅ The API key is already set as an environment variable."
else
    echo "❌ The API key is not set."
    echo "Opening Astrometry.net profile page in your browser..."
    $BROWSER "$URL" >/dev/null 2>&1 || echo "Open manually: $URL"

    echo "Paste your API key here and press Enter:"
    read -r API_KEY

    if [ -z "$API_KEY" ]; then
        echo "❌ No API key entered. Aborting."
        exit 1
    fi

    echo "ASTROMETRY_API_KEY=$API_KEY" >> "$ENV_FILE"

    echo -e "✅ Done   \
             Your .env file now contains the API key. \
             You can load it in Python with dotenv.\n"
fi  

# -----------------------------
# Step 3: Download and process data files
# -----------------------------
DATA_DIR="GUIs/Utilities"
mkdir -p "$DATA_DIR"

MAX_ATTEMPTS=4
ATTEMPT=0

download_file () {
    url=$1
    if command -v wget &>/dev/null; then
        wget "$url"
    elif command -v curl &>/dev/null; then
        curl -O "$url"
    else
        echo "❌ Neither wget nor curl found. Please install one (e.g. sudo apt install wget)."
        exit 1
    fi
}

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do

    echo "------------------------------------------------------"
    echo " Downloading data files..."
    echo "  1. MPCORB.DAT"
    echo "  2. astorb.dat"



    download_file http://minorplanetcenter.net/iau/MPCORB/MPCORB.DAT.gz
    download_file https://ftp.lowell.edu/pub/elgb/astorb.dat.gz

    if [ -f "MPCORB.DAT.gz" ] && [ -f "astorb.dat.gz" ]; then
        echo " Decompressing data files..."
        gunzip MPCORB.DAT.gz
        gunzip astorb.dat.gz

        mv MPCORB.DAT "$DATA_DIR/"
        mv astorb.dat "$DATA_DIR/"

        echo " Processing data files..."
        python GUIs/Utilities/pickler.py

        echo " The data files have been downloaded and processed successfully."
        break
    else 
        ATTEMPT=$((ATTEMPT + 1))
        if [ $ATTEMPT -lt $MAX_ATTEMPTS ]; then
            echo "❌ Download failed. Retrying... ($ATTEMPT/$MAX_ATTEMPTS) \n"
        else
            echo "❌ Download failed $MAX_ATTEMPTS times. Please download the files manually:"
            echo "  1. MPCORB.DAT: http://minorplanetcenter.net/iau/MPCORB/MPCORB.DAT.gz"
            echo "  2. astorb.dat: https://ftp.lowell.edu/pub/elgb/astorb.dat.gz"
            echo "Place them in the current directory and press Enter to continue..."
            read -p "Press Enter to continue..." dummy

            echo " Transfer data files to $DATA_DIR and process them manually..."
        fi
    fi
done
            
echo "✅ Setup complete."