@echo off
chcp 65001 >nul
title 取消开机自启（题库判题服务）

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$lnk = Join-Path ([Environment]::GetFolderPath('Startup')) '题库判题服务.lnk';" ^
  "if (Test-Path $lnk) { Remove-Item $lnk -Force; Write-Host '已删除开机自启快捷方式。' } else { Write-Host '未找到开机自启快捷方式，无需取消。' }"

echo.
pause
