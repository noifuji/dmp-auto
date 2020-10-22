@echo off
setlocal enabledelayedexpansion
cd %~dp0/..

set PIDFile=./data/pid.txt

powershell "Get-WmiObject win32_process -filter processid=$pid | ForEach-Object{$_.parentprocessid;}" > %PIDFile%

java -jar sikulixide-2.0.4.jar -r ./scripts/AllMainStories.sikuli -- reset
if %ERRORLEVEL%==50 (
 start .\Tools\auto_update.bat .\bat\%~n0%~x0
 exit
)

pause