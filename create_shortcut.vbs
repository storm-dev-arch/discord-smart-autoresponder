Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "C:\Users\storm\Desktop\Discord Auto-Responder.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "C:\Users\storm\AppData\Local\Programs\antigravity-discord-autoresponder\start.bat"
oLink.WorkingDirectory = "C:\Users\storm\AppData\Local\Programs\antigravity-discord-autoresponder"
oLink.Save
