@echo off
chcp 65001 >nul
setlocal EnableExtensions
cd /d "%~dp0"

set PORT=8000

echo SyncView launcher
echo Папка проекта: %CD%
echo.

REM 
where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python не найден в PATH.
  echo Установи Python с python.org и поставь галочку "Add Python to PATH".
  echo Потом открой новый PowerShell/консоль и попробуй снова.
  echo.
  pause
  exit /b 1
)

REM 
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /c:"IPv4-адрес" /c:"IPv4 Address"') do (
  for /f "tokens=* delims= " %%B in ("%%A") do set LANIP=%%B
)
if not defined LANIP set LANIP=127.0.0.1

echo Для этого ПК:   http://127.0.0.1:%PORT%
echo Для других:     http://%LANIP%:%PORT%
echo.

REM 
if not exist "venv\Scripts\python.exe" (
  echo [INFO] Creating venv...
  python -m venv venv
  if errorlevel 1 (
    echo [ERROR] Не удалось создать venv.
    echo.
    pause
    exit /b 1
  )
)

echo [INFO] Python in venv:
venv\Scripts\python.exe -c "import sys; print(sys.executable)"
echo.

echo [INFO] Updating pip...
venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 (
  echo [ERROR] pip upgrade failed.
  echo.
  pause
  exit /b 1
)

REM 
if exist "requirements.txt" (
  echo [INFO] Installing from requirements.txt...
  venv\Scripts\python.exe -m pip install -r requirements.txt
) else (
  echo [WARN] requirements.txt not found - installing minimal deps...
  venv\Scripts\python.exe -m pip install flask flask_sqlalchemy flask_login flask_wtf flask_socketio
)

echo.
echo [INFO] Starting server...
echo ------------------------------------------
venv\Scripts\python.exe run.py
echo ------------------------------------------
echo [INFO] Server exited.
echo.

pause
