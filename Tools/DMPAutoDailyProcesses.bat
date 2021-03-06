



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



@REM デイリーログイン
java -jar sikulixide-2.0.4.jar -r .\scripts\NoxDailyLogin.sikuli
if %ERRORLEVEL%==50 (
 start .\Tools\auto_update.bat .\Tools\%~n0%~x0
 exit
)
if %ERRORLEVEL%==60 (
 start .\Tools\createGameTradeDraft.bat .\Tools\%~n0%~x0
 exit
)


@REM デイリーミッション
java -jar sikulixide-2.0.4.jar -r .\scripts\NoxDailyMission.sikuli
if %ERRORLEVEL%==50 (
 start .\Tools\auto_update.bat .\Tools\%~n0%~x0
 exit
)
if %ERRORLEVEL%==60 (
 start .\Tools\createGameTradeDraft.bat .\Tools\%~n0%~x0
 exit
)


@REM レジェンド周回
java -jar sikulixide-2.0.4.jar -r .\scripts\LegendBattleBasic.sikuli
if %ERRORLEVEL%==50 (
 start .\Tools\auto_update.bat .\Tools\%~n0%~x0
 exit
)


@REM クイックピック周回
java -jar sikulixide-2.0.4.jar -r .\scripts\QuickPick.sikuli
if %ERRORLEVEL%==50 (
 start .\Tools\auto_update.bat .\Tools\%~n0%~x0
 exit
)
if %ERRORLEVEL%==60 (
 start .\Tools\createGameTradeDraft.bat .\Tools\%~n0%~x0
 exit
)

@REM セットアップ
java -jar sikulixide-2.0.4.jar -r .\scripts\NoxSetupAccount.sikuli
if %ERRORLEVEL%==50 (
 start .\Tools\auto_update.bat .\Tools\%~n0%~x0
 exit
)

@REM リセマラ用メインストーリー周回
@REM java -jar sikulixide-2.0.4.jar -r .\scripts\AllMainStories.sikuli -- reset
@REM if %ERRORLEVEL%==50 (
@REM  start .\Tools\auto_update.bat .\Tools\%~n0%~x0
@REM  exit
@REM )

@REM メインストーリー周回
java -jar sikulixide-2.0.4.jar -r .\scripts\AllMainStories.sikuli
if %ERRORLEVEL%==50 (
 start .\Tools\auto_update.bat .\Tools\%~n0%~x0
 exit
)
if %ERRORLEVEL%==60 (
 start .\Tools\createGameTradeDraft.bat .\Tools\%~n0%~x0
 exit
)

pause