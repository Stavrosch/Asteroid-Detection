#!/bin/bash
set -e

# Step 1: Environment setup
cat <<'EOF'
This script will install all dependencies and prepare the environment.

Steps:
1. Create a Python virtual environment or conda environment.
2. Install required dependencies.
3. Download and process data files.

Please enter your choice of environment:
- venv
- conda
EOF

read -p "Environment: " env_choice
echo "You chose: $env_choice"

if [ "$env_choice" = "venv" ]; then
    python3 -m venv .venv 
    source .venv/bin/activate
    pip install -r requirements.txt
elif [ "$env_choice" = "conda" ]; then
    # Ensure conda is available
    if ! command -v conda &> /dev/null; then
        echo "conda not found. Please install Anaconda or Miniconda first."
        exit 1
    fi
    conda create -y -n astro-detection python=3.12
z
    conda activate astro-detection
    pip install -r requirements.txt
else
    echo "Please choose either venv or conda"
    exit 1
fi

echo "Environment setup complete."

# Step 2nd: Set up API key for Astrometry.net
ENV_FILE=".env"
URL="http://nova.astrometry.net/api_help"

echo "Opening Astrometry.net profile page in your browser..."
xdg-open "$URL" >/dev/null 2>&1 &

echo "------------------------------------------------------"
echo "Please log in and copy your API key from the website."
echo "Paste your API key here and press Enter:"
read -r API_KEY

if [ -z "$API_KEY" ]; then
    echo "❌ No API key entered. Aborting."
    exit 1
fi

echo "Saving API key to $ENV_FILE..."

echo "✅ Done. Your .env file now contains the API key."
echo "   You can load it in Python with dotenv"

# Step 3rd: Download and process data files
echo " Downloading data files..."
echo "  1. MPCORB.DAT"
echo "  2. astorb.dat"

# Download MPCORB.DAT
wget http://minorplanetcenter.net/iau/MPCORB/MPCORB.DAT

# Download astorb.dat
wget http://minorplanetcenter.net/iau/MPCORB/astorb.dat

mv MPCORB.DAT GUIs/Utilities/
mv astorb.dat GUIs/Utilities/

echo " Processing data files..."
python GUIs/Utilities/pickler.py