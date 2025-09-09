#!/bin/bash

echo "Building TidyDesk for Linux..."

# Install dependencies
pip3 install -r requirements.txt

# Build executable
pyinstaller --onefile --windowed --name=tiddesk --icon=file_organizer/icons/icon_256x256.png --add-data="file_organizer/themes:themes" --add-data="file_organizer/icons:icons" --hidden-import=tkinter --hidden-import=PIL --hidden-import=schedule --hidden-import=psutil --hidden-import=file_organizer.core --hidden-import=file_organizer.gui --hidden-import=file_organizer.utils file_organizer/main.py

# Create installer directory
mkdir -p installers

# Copy executable
cp dist/tiddesk installers/tiddesk-linux
chmod +x installers/tiddesk-linux

echo "Build complete! Executable: installers/tiddesk-linux"
