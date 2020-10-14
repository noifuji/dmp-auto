import sys
import traceback
import random
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import NoxDMLib
import CommonDMLib
import NoxResources

####################Settings####################
instances = [1086]
####################Settings####################

mentionUser = EnvSettings.mentionUser
appname = 'BWD'
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
mode = EnvSettings.RUN_MODE

#Pre-processing Start        
App(EnvSettings.AppPath).close()
App(EnvSettings.AndAppPath).close()

if CommonDMLib.isNewVersionAvailable():
    exit(50)
#Pre-processing End

instanceIndex = 0
retryCount = 0
while instanceIndex < len(instances):
    try:
        CommonDMLib.RestartNox(NoxResources, instances[instanceIndex])
        CommonDMLib.RestartApp(NoxResources)
        click(NoxResources.ICON_SHOP)
        for skipTutorialLoop in range(10):
            click(Pattern("1602495018278.png").targetOffset(93,-44))
            wait(0.5)
        click(Pattern("1602495063341.png").targetOffset(-6,-199))
        wait(3)
        click(Pattern("1602495086836.png").targetOffset(-14,-221))
        exists("1602495132908.png",60)
        click(Pattern("1602495164024.png").targetOffset(148,78))
        exists("1602495190769.png", 60)
        click("1602495200056.png")
        exists("1602495225721.png", 60)
        click(Pattern("1602495388492.png").targetOffset(-221,-42))
        wait(3)
        click(Pattern("1602495273120.png").targetOffset(3,53))
        exists("1602495190769.png", 60)
        click("1602495200056.png")
        exists("1602495225721.png", 60)
        click(Pattern("1602495388492.png").targetOffset(-221,-42))
        
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Instance ' + str(instances[instanceIndex]) + 'was completed.', appname)
        instanceIndex += 1
    except:
        Settings.MoveMouseDelay = 0.1
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured in ' + str(instances[instanceIndex]) + '. This instance was skipped.', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.sendMessagetoSlack(mentionUser, "Screenshot" ,appname)
        instanceIndex += 1