setlocal enabledelayedexpansion
cd %~dp0/..

set PIDFile=.\data\pid.txt

if exist "%PIDFile%" (
    set /p targetPID=<%PIDFile%

    tasklist /fi "PID eq !targetPID!" | find "cmd.exe" | find "Console" > nul
    if not ERRORLEVEL 1 (
        goto RUNNING
    ) else (
        del %PIDFile%
        goto NOT_RUNNING
    )

) else (
    goto NOT_RUNNING

)

:RUNNING
    echo kill process: !targetPID!
    taskkill /pid !targetPID!
    del !PIDFile!
    goto END

:NOT_RUNNING
    echo not running
    goto END

:END


set PIDFile=./data/pid.txt

powershell "Get-WmiObject win32_process -filter processid=$pid | ForEach-Object{$_.parentprocessid;}" > %PIDFile%

java -jar sikulixide-2.0.4.jar -r .\scripts\NoxDailyMission.sikuli
java -jar sikulixide-2.0.4.jar -r .\scripts\LegendBattleBasic.sikuli
java -jar sikulixide-2.0.4.jar -r .\scripts\AllMainStories.sikuli