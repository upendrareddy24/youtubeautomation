#!/bin/bash

echo "--- Starting Oracle Cloud Setup ---"

# 1. System Updates
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# 2. Install Dependencies
echo "Installing base dependencies (FFmpeg, ImageMagick, Python)..."
sudo apt install -y python3 python3-pip python3-venv ffmpeg imagemagick git

# 3. Fix ImageMagick Policy (Critical for MoviePy TextClips)
# MoviePy often fails if ImageMagick policies restrict '@' usage or file reads
echo "Configuring ImageMagick policies..."
if [ -f /etc/ImageMagick-6/policy.xml ]; then
    sudo sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/g' /etc/ImageMagick-6/policy.xml
    # Sometimes more aggressive policy fixes are needed for text
    # This is a safe baseline.
fi

# 4. Setup Python Environment
echo "Setting up Python Virtual Environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing Python Requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "--- Setup Complete! ---"
echo "To activate manually, run: source venv/bin/activate"
