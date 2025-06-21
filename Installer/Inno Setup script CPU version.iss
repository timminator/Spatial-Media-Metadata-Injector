#define MyAppName "Spatial Media Metadata Injector"
#define MyAppVersion "2.3.0"
#define MyAppURL "https://github.com/timminator/Spatial-Media-Metadata-Injector"
#define MyAppExeName "Spatial Media Metadata Injector.exe"
#define MyInstallerVersion "1.0.0.0"
#define MyAppCopyright "timminator"

[Setup]
SignTool=signtool $f
AppId={{6EF74D42-F07C-4AAC-91B9-B18C3E4459F6}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
VersionInfoVersion={#MyInstallerVersion}
AppCopyright={#MyAppCopyright}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={commonpf64}\{#MyAppName}
DefaultGroupName={#MyAppName}
UsePreviousAppDir=yes
LicenseFile=..\LICENSE
DisableProgramGroupPage=yes
PrivilegesRequired=admin
OutputBaseFilename={#MyAppName}-GUI-v{#MyAppVersion}-setup-x64
SetupIconFile=..\Spatial Media Metadata Injector.ico
Compression=lzma2/ultra64
InternalCompressLevel=ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
LZMANumBlockThreads=6
WizardStyle=classic
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Dirs]
Name: "{app}"; Permissions: everyone-full

[Files]
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\_bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\_decimal.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\_elementtree.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\_lzma.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\_tkinter.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\_wmi.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\libcrypto-3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\libffi-8.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\python312.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\tcl86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\tk86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\vcruntime140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\vcruntime140_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\Spatial Media Metadata Injector.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\Spatial Media Metadata Injector.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\zlib1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\tcl\*"; DestDir: "{app}\tcl"; Flags: ignoreversion recursesubdirs
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\tcl8\*"; DestDir: "{app}\tcl8"; Flags: ignoreversion recursesubdirs
Source: "..\Windows\Spatial-Media-Metadata-Injector-GUI-v{#MyAppVersion}\tk\*"; DestDir: "{app}\tk"; Flags: ignoreversion recursesubdirs

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent