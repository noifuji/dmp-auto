$sid = ([wmi]"win32_userAccount.Domain='$Env:Computername',Name='$env:username'").sid
$currentPath = $PSScriptRoot
$batPath = $currentPath +  "\DMPAutoDailyProcesses.bat"

$Trigger = New-ScheduledTaskTrigger -Daily -at "05:10:00"
$Action = New-ScheduledTaskAction -Execute $batPath
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 23:50:00
$Principal = New-ScheduledTaskPrincipal -UserId $sid -LogonType ServiceAccount -RunLevel Highest


Register-ScheduledTask -TaskPath "\DMPAuto\" -TaskName "DMPAutoDailyProcesses" -Trigger $Trigger -Action $Action -Principal $Principal -Settings $settings -Force


$sid = ([wmi]"win32_userAccount.Domain='$Env:Computername',Name='$env:username'").sid
$currentPath = $PSScriptRoot
$batPath = $currentPath +  "\killprocess.bat"

$Trigger = New-ScheduledTaskTrigger -Daily -at "04:55:00"
$Action = New-ScheduledTaskAction -Execute $batPath
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 01:00:00
$Principal = New-ScheduledTaskPrincipal -UserId $sid -LogonType ServiceAccount -RunLevel Highest


Register-ScheduledTask -TaskPath "\DMPAuto\" -TaskName "KillProcess" -Trigger $Trigger -Action $Action -Principal $Principal -Settings $settings -Force