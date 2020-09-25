@echo off
setlocal enabledelayedexpansion
cd %~dp0/..

set PIDFile=./data/pid.txt

powershell "Get-WmiObject win32_process -filter processid=$pid | ForEach-Object{$_.parentprocessid;}" > %PIDFile%

set /P USR_INPUT_STR="Enter ref No.: "

java -jar sikulixide-2.0.4.jar -r ./scripts/CardCount.sikuli -- %USR_INPUT_STR%

pause