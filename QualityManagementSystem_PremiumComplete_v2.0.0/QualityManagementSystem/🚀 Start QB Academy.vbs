Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory of this script
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
objShell.CurrentDirectory = strScriptPath

' Create a nice console window
objShell.Run "cmd /c title QB Academy Quality Management System v2.0 && color 0A && echo ===================================================== && echo    QB Academy Quality Management System v2.0 && echo    Premium Arabic Enhancement Edition && echo ===================================================== && echo. && echo 🚀 Starting application... && python qb.py && pause", 1, False
