cd %~dp0\..
git fetch https://github.com/noifuji/dmp-auto.git
git reset --hard FETCH_HEAD
start .\Tools\%1
exit