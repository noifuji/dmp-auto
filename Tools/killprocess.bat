setlocal enabledelayedexpansion
cd %~dp0

set PIDFile=..\data\pid.txt

if exist "%PIDFile%" (
    set /p targetPID=<%PIDFile%

    tasklist /fi "PID eq !targetPID!" | find "cmd.exe" > nul
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