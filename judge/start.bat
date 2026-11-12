@echo off
chcp 65001 >nul
cd /d "%~dp0"
title C++ 题库 · 本地判题服务

set "PYEXE="
where python >nul 2>nul && set "PYEXE=python"
if not defined PYEXE ( where py >nul 2>nul && set "PYEXE=py" )
if not defined PYEXE (
  if exist "D:\Program Files\Tencent\Marvis\MarvisAgent\1.60.3300.765\runtime\python311\python.exe" (
    set "PYEXE=D:\Program Files\Tencent\Marvis\MarvisAgent\1.60.3300.765\runtime\python311\python.exe"
  )
)

if not defined PYEXE (
  echo.
  echo [错误] 未找到 Python 运行环境，无法启动判题服务。
  echo 你可以：1) 安装 Python 后重试；2) 直接双击 index.html 使用（仅无自动判题功能）。
  echo.
  pause
  exit /b 1
)

echo 正在启动本地判题服务，浏览器将自动打开...
echo 使用完毕后请关闭本窗口以停止服务。
echo.
"%PYEXE%" server.py %*
pause
