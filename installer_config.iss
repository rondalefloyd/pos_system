[Setup]
AppName=POS System
AppVersion=1.0
DefaultDirName={pf}\POS System
DefaultGroupName=POS System
UninstallDisplayIcon={app}\POS.exe
OutputDir=C:\Users\mimoy\Documents\GitHub\pos_system\v_1_0\dist
OutputBaseFilename=Setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\mimoy\Documents\GitHub\pos_system\v_1_0\dist\POS.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\POS System"; Filename: "{app}\POS.exe"
Name: "{commondesktop}\POS System"; Filename: "{app}\POS.exe"; Tasks: desktopicon

[Run]
Filename: "https://dl.google.com/drive-file-stream/GoogleDriveSetup.exe"; Description: "Download Google Drive for Desktop"; Flags: postinstall shellexec skipifsilent
