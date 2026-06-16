@echo off
setlocal

cd /d "%~dp0"

if "%~1"=="--check" (
    where python >nul 2>nul
    if errorlevel 1 (
        echo Python was not found. Please install Python or update PATH.
        exit /b 1
    )
    if not exist "make_dict\web_ui.py" (
        echo make_dict\web_ui.py was not found. Run this batch file from the project root.
        exit /b 1
    )
    echo Web UI batch check passed.
    exit /b 0
)

set "PORT=8765"
if not "%~1"=="" set "PORT=%~1"

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Please install Python or update PATH.
    pause
    exit /b 1
)

if not exist "make_dict\web_ui.py" (
    echo make_dict\web_ui.py was not found. Run this batch file from the project root.
    pause
    exit /b 1
)

echo Starting glossary Web UI...
echo URL: http://127.0.0.1:%PORT%
start "" "http://127.0.0.1:%PORT%"
python make_dict\web_ui.py --port %PORT%

echo.
echo Web UI stopped.
pause
