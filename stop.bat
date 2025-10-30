@echo off
echo Stopping Subtitle Overlay Application...
echo.

REM Find and kill Python processes running main.py
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /I "PID"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /I "main.py" >nul
    if not errorlevel 1 (
        echo Stopping process %%a...
        taskkill /F /PID %%a >nul 2>&1
    )
)

REM Also check for pythonw.exe (windowless Python)
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq pythonw.exe" /FO LIST ^| findstr /I "PID"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /I "main.py" >nul
    if not errorlevel 1 (
        echo Stopping process %%a...
        taskkill /F /PID %%a >nul 2>&1
    )
)

echo.
echo All instances stopped.
timeout /t 2 >nul



