@echo off
chcp 65001 >nul
title C++练习题 - 公网分享
cd /d "%~dp0"

echo ==========================================
echo   C++练习题 公网分享启动器
echo ==========================================
echo.

rem 1) 启动只读分享服务（public 目录，无线编译判题能力，端口 8766）
netstat -ano | findstr ":8766 " | findstr LISTENING >nul
if errorlevel 1 (
    echo [1/2] 正在启动分享服务 8766 ...
    start "" /b python -m http.server 8766 --bind 0.0.0.0 --directory "%~dp0public"
    timeout /t 2 >nul
) else (
    echo [1/2] 分享服务 8766 已在运行
)

rem 2) 建立公网隧道
echo [2/2] 正在连接公网隧道，请稍候 10-20 秒 ...
echo.
echo   下面出现的 https://xxxx.lhr.life 就是发给别人的公网网址
echo   保持本窗口开启，关闭窗口或关机则网址失效
echo ==========================================
echo.

ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL -o ServerAliveInterval=20 -o ExitOnForwardFailure=yes -R 80:127.0.0.1:8766 nokey@localhost.run

echo.
echo 隧道已断开。按任意键退出。
pause >nul
