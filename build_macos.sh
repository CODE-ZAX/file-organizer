#!/bin/bash

echo "Building TidyDesk for macOS..."

# Install dependencies
pip3 install -r requirements.txt

# Build application bundle
pyinstaller --onefile --windowed --name=TidyDesk --icon=file_organizer/icons/app.icns --add-data="file_organizer/themes:themes" --add-data="file_organizer/icons:icons" --hidden-import=tkinter --hidden-import=PIL --hidden-import=schedule --hidden-import=psutil --hidden-import=file_organizer.core --hidden-import=file_organizer.gui --hidden-import=file_organizer.utils --osx-bundle-identifier=com.tiddesk.app file_organizer/main.py

# Create installer directory
mkdir -p installers

# Copy app bundle
cp -r dist/TidyDesk.app installers/

# Create DMG
hdiutil create -volname "TidyDesk" -srcfolder dist/TidyDesk.app -ov -format UDZO installers/TidyDesk-macOS.dmg

echo "Build complete! App: installers/TidyDesk.app, DMG: installers/TidyDesk-macOS.dmg"
