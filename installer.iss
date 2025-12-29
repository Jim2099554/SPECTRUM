; Script de Inno Setup para SENTINELA
; Sistema de Inteligencia Penitenciaria

#define MyAppName "SENTINELA"
#define MyAppVersion "1.0"
#define MyAppPublisher "Sistema de Inteligencia Penitenciaria"
#define MyAppURL "https://sentinela.com"
#define MyAppExeName "SENTINELA.exe"

[Setup]
; Información de la aplicación
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputDir=installer_output
OutputBaseFilename=SENTINELA_Setup_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

; Icono del instalador
SetupIconFile=assets\sentinela_icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Backend ejecutable y dependencias
Source: "dist\SENTINELA_Backend\*"; DestDir: "{app}\backend"; Flags: ignoreversion recursesubdirs createallsubdirs
; Base de datos y configuraciones
Source: "backend\transcripts.db"; DestDir: "{app}\backend"; Flags: ignoreversion
Source: "backend\config\*"; DestDir: "{app}\backend\config"; Flags: ignoreversion recursesubdirs
Source: "backend\data\*"; DestDir: "{app}\backend\data"; Flags: ignoreversion recursesubdirs
; Directorios de trabajo
Source: "backend\photos\*"; DestDir: "{app}\backend\photos"; Flags: ignoreversion recursesubdirs
Source: "backend\transcripts\*"; DestDir: "{app}\backend\transcripts"; Flags: ignoreversion recursesubdirs
Source: "backend\audios\*"; DestDir: "{app}\backend\audios"; Flags: ignoreversion recursesubdirs
; Documentación
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "SISTEMA_LICENCIAS.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "ARQUITECTURA_BASES_DE_DATOS.md"; DestDir: "{app}"; Flags: ignoreversion
; Script de inicio
Source: "start_sentinela.bat"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\start_sentinela.bat"; IconFilename: "{app}\assets\sentinela_icon.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\start_sentinela.bat"; IconFilename: "{app}\assets\sentinela_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\start_sentinela.bat"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
var
  LicensePage: TInputFileWizardPage;
  DatabasePage: TInputQueryWizardPage;

procedure InitializeWizard;
begin
  { Página de licencia USB }
  LicensePage := CreateInputFilePage(wpSelectDir,
    'Licencia USB', 'Seleccione el archivo de licencia',
    'Por favor, conecte el USB con la licencia y seleccione el archivo sentinela.lic');
  LicensePage.Add('Archivo de licencia (sentinela.lic):', 
    'Archivos de licencia|sentinela.lic|Todos los archivos|*.*', '.lic');

  { Página de configuración de base de datos }
  DatabasePage := CreateInputQueryPage(wpSelectDir,
    'Configuración de Base de Datos PPL', 
    'Configure la conexión a la base de datos de PPL',
    'Esta base de datos es obligatoria y debe contener el PIN como clave principal.');
  
  DatabasePage.Add('Tipo de BD (mysql/postgresql/mssql/sqlite):', False);
  DatabasePage.Add('Host/Servidor:', False);
  DatabasePage.Add('Puerto:', False);
  DatabasePage.Add('Nombre de BD:', False);
  DatabasePage.Add('Usuario:', False);
  DatabasePage.Add('Contraseña:', True);
  
  { Valores por defecto }
  DatabasePage.Values[0] := 'mysql';
  DatabasePage.Values[1] := 'localhost';
  DatabasePage.Values[2] := '3306';
  DatabasePage.Values[3] := 'ppl_database';
  DatabasePage.Values[4] := 'root';
  DatabasePage.Values[5] := '';
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  LicenseFile: String;
begin
  Result := True;
  
  if CurPageID = LicensePage.ID then
  begin
    LicenseFile := LicensePage.Values[0];
    if LicenseFile = '' then
    begin
      MsgBox('Por favor seleccione el archivo de licencia USB.', mbError, MB_OK);
      Result := False;
    end
    else if not FileExists(LicenseFile) then
    begin
      MsgBox('El archivo de licencia no existe.', mbError, MB_OK);
      Result := False;
    end;
  end;
  
  if CurPageID = DatabasePage.ID then
  begin
    if (DatabasePage.Values[0] = '') or (DatabasePage.Values[3] = '') then
    begin
      MsgBox('Por favor complete todos los campos obligatorios.', mbError, MB_OK);
      Result := False;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigFile: String;
  ConfigContent: TStringList;
  LicenseFile: String;
  DestLicenseDir: String;
begin
  if CurStep = ssPostInstall then
  begin
    { Copiar licencia al directorio de instalación }
    LicenseFile := LicensePage.Values[0];
    if FileExists(LicenseFile) then
    begin
      DestLicenseDir := ExpandConstant('{app}\backend\config');
      FileCopy(LicenseFile, DestLicenseDir + '\sentinela.lic', False);
    end;
    
    { Crear archivo de configuración de base de datos }
    ConfigFile := ExpandConstant('{app}\backend\config\database_config.json');
    ConfigContent := TStringList.Create;
    try
      ConfigContent.Add('{');
      ConfigContent.Add('  "databases": {');
      ConfigContent.Add('    "ppl": {');
      ConfigContent.Add('      "type": "' + DatabasePage.Values[0] + '",');
      ConfigContent.Add('      "host": "' + DatabasePage.Values[1] + '",');
      ConfigContent.Add('      "port": ' + DatabasePage.Values[2] + ',');
      ConfigContent.Add('      "database": "' + DatabasePage.Values[3] + '",');
      ConfigContent.Add('      "user": "' + DatabasePage.Values[4] + '",');
      ConfigContent.Add('      "password": "' + DatabasePage.Values[5] + '",');
      ConfigContent.Add('      "required": true,');
      ConfigContent.Add('      "pin_field": "pin",');
      ConfigContent.Add('      "name_field": "nombre"');
      ConfigContent.Add('    }');
      ConfigContent.Add('  }');
      ConfigContent.Add('}');
      ConfigContent.SaveToFile(ConfigFile);
    finally
      ConfigContent.Free;
    end;
  end;
end;
