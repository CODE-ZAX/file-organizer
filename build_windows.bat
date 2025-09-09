@echo off
echo Building TidyDesk for Windows...

REM Install dependencies
pip install -r requirements.txt

REM Build executable
pyinstaller --onefile --windowed --name=TidyDesk --icon=file_organizer/icons/app.ico --add-data="file_organizer/themes;themes" --add-data="file_organizer/icons;icons" --hidden-import=tkinter --hidden-import=PIL --hidden-import=schedule --hidden-import=psutil --hidden-import=file_organizer.core --hidden-import=file_organizer.gui --hidden-import=file_organizer.utils file_organizer/main.py

REM Create installer directory
mkdir installers 2>nul

REM Copy executable
copy dist\TidyDesk.exe installers\TidyDesk-Windows.exe

echo Build complete! Executable: installers\TidyDesk-Windows.exe
pause
