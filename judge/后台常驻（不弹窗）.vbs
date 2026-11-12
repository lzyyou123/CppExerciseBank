' 后台常驻判题服务（不开浏览器、不显窗口），供开机自启使用
Option Explicit
Dim sh, fso, dir, rc
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)

rc = sh.Run("cmd /c netstat -an | findstr /C:""127.0.0.1:8765"" | findstr /I ""LISTENING"" >nul 2>nul", 0, True)
If rc <> 0 Then
    sh.Run "cmd /c """ & dir & "\start.bat"" --no-browser", 0, False
End If
