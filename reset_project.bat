@echo off
cd /d %~dp0
powershell -NoProfile -ExecutionPolicy Bypass -Command "Remove-Item -Recurse -Force -ErrorAction SilentlyContinue '.\app\static\uploads'; Get-ChildItem -Recurse -Force -Filter '*.db' -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue; Get-ChildItem -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"
pause