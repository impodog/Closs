Name "Closs Installer"
OutFile "ClossSetup.exe"
RequestExecutionLevel user
Unicode True
InstallDir C:\Games\Closs
RequestExecutionLevel admin
Page directory
Page instfiles
Section "Install"
  SetOutPath $INSTDIR
  File /r "package\*.*" 
SectionEnd