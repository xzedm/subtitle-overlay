@echo off
echo Starting Subtitle Overlay Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if another instance is running and stop it
echo Checking for running instances...
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST 2^>nul ^| findstr /I "PID"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /I "subtitle.*main.py" >nul
    if not errorlevel 1 (
        echo Stopping previous instance...
        taskkill /F /PID %%a >nul 2>&1
        timeout /t 1 >nul
    )
)

echo Checking dependencies...
python -c "import PyQt6; import websockets" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting application...
echo The app will minimize to the system tray.
echo Look for the icon in your system tray (bottom-right corner).
echo.

python app\main.py

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)

