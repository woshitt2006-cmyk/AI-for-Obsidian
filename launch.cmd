@echo off
chcp 65001 >nul
setlocal
powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File "%~dp0import_gui.ps1"
if errorlevel 1 pause
