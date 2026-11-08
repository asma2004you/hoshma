@echo off
cd /d "%~dp0"
echo ================================================
echo   Running: vacuum_agent.py
echo ================================================
python --version
if errorlevel 1 (
    echo.
    echo [ERROR] Python was not found.
    echo         Open a NEW terminal window and try again.
) else (
    echo.
    python vacuum_agent.py
)
echo.
pause
