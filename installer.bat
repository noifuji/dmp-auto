cd %~dp0
git init
git pull https://github.com/noifuji/dmp-auto.git

setx DMP_AUTO_HOME %~dp0

copy /Y .\Tools\sites.txt %APPDATA%\Sikulix\Lib\site-packages\

call Tools\RegisterDailyTask.bat

pause