' 打开题库并确保判题服务在运行（无黑窗口、无弹窗）
' 若服务未启动则在后台静默拉起，然后打开 http://127.0.0.1:8765/
Option Explicit
Dim sh, fso, dir, rc
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)

' 检测 8765 端口是否已在监听
rc = sh.Run("cmd /c netstat -an | findstr /C:""127.0.0.1:8765"" | findstr /I ""LISTENING"" >nul 2>nul", 0, True)
If rc <> 0 Then
    ' 未运行：隐藏窗口启动服务（server.py 启动 1 秒后会自动打开浏览器）
    sh.Run "cmd /c """ & dir & "\start.bat""", 0, False
    WScript.Sleep 1800
Else
    ' 已在运行：直接用默认浏览器打开题库
    sh.Run "http://127.0.0.1:8765/", 1, False
End If
