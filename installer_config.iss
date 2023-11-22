[Setup]
AppName=POS
AppVersion=1.0
DefaultDirName={userappdata}\POS System
DisableDirPage=yes
DefaultGroupName=POS
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
Source: "C:\Users\mimoy\Documents\GitHub\pos_system\v_1_0\dist\POS\POS.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\mimoy\Documents\GitHub\pos_system\v_1_0\dist\POS\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs uninsneveruninstall hidden

[Icons]
Name: "{group}\POS System"; Filename: "{app}\POS.exe"
Name: "{commondesktop}\POS System"; Filename: "{app}\POS.exe"; Tasks: desktopicon

[Run]
Filename: "https://dl.google.com/drive-file-stream/GoogleDriveSetup.exe"; Description: "Download Google Drive for Desktop"; Flags: postinstall shellexec skipifsilent
