Set oWS = WScript.CreateObject("WScript.Shell")
sStartup = oWS.SpecialFolders("Startup")
sLinkFile = sStartup & "\Discord Auto-Responder.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "wscript.exe"
oLink.Arguments = """C:\Users\storm\AppData\Local\Programs\antigravity-discord-autoresponder\run_silent.vbs"""
oLink.WorkingDirectory = "C:\Users\storm\AppData\Local\Programs\antigravity-discord-autoresponder"
oLink.Save

sDeskFile = "C:\Users\storm\Desktop\Discord Auto-Responder.lnk"
Set oDesk = oWS.CreateShortcut(sDeskFile)
oDesk.TargetPath = "wscript.exe"
oDesk.Arguments = """C:\Users\storm\AppData\Local\Programs\antigravity-discord-autoresponder\run_silent.vbs"""
oDesk.WorkingDirectory = "C:\Users\storm\AppData\Local\Programs\antigravity-discord-autoresponder"
oDesk.Save
