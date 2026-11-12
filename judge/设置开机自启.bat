@echo off
chcp 65001 >nul
cd /d "%~dp0"
title 设置开机自启（题库判题服务）

echo 本操作会在你的「启动」文件夹中创建一个快捷方式：
echo   目标：后台常驻（不弹窗）.vbs
echo   效果：开机后判题服务自动在后台运行，以后打开题库网页即可直接判题。
echo.
echo 该操作只写入当前用户的启动项，不修改系统注册表，可随时用「取消开机自启.bat」撤销。
echo.
set /p yes=确认设置？输入 Y 回车继续，其他键取消：
if /i not "%yes%"=="Y" (
  echo 已取消。
  pause
  exit /b 0
)

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ws = New-Object -ComObject WScript.Shell;" ^
  "$lnk = Join-Path ([Environment]::GetFolderPath('Startup')) '题库判题服务.lnk';" ^
  "$s = $ws.CreateShortcut($lnk);" ^
  "$s.TargetPath = 'wscript.exe';" ^
  "$s.Arguments = '\"' + (Join-Path '%~dp0' '后台常驻（不弹窗）.vbs') + '\"';" ^
  "$s.WorkingDirectory = '%~dp0';" ^
  "$s.WindowStyle = 7;" ^
  "$s.Description = 'C语言题库本地判题服务';" ^
  "$s.Save();" ^
  "Write-Host ('已创建：' + $lnk)"

echo.
echo 完成。下次开机后无需再手动启动服务。
pause
