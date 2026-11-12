@echo off
chcp 65001 >nul
title 停止判题服务

echo 正在查找占用 127.0.0.1:8765 的服务进程...
set "FOUND="
for /f "tokens=5" %%a in ('netstat -ano ^| findstr /C:"127.0.0.1:8765" ^| findstr /I "LISTENING"') do (
  set "FOUND=1"
  echo 结束进程 PID=%%a
  taskkill /PID %%a /F >nul 2>nul
)

if not defined FOUND (
  echo 当前没有正在运行的判题服务。
) else (
  echo 判题服务已停止。下次需要判题时双击「打开题库（自动判题）.vbs」即可。
)
echo.
pause
