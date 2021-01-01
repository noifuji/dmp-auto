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
from spreadsheetapis import SpreadSheetApis
from driveapis import DriveApis

####################Settings####################
instances = EnvSettings.NOX_INSTANCES
####################Settings####################

mentionUser = EnvSettings.mentionUser
appname = 'LOGIN'
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
mode = EnvSettings.RUN_MODE

#Pre-processing Start        
App(EnvSettings.AppPath).close()
App(EnvSettings.AndAppPath).close()

if CommonDMLib.isNewVersionAvailable():
    exit(50)
CommonDMLib.deleteIdentifiers()
sheets = SpreadSheetApis("DMPAuto", CommonDMLib.getCredentials())
drive = DriveApis("DMPAuto", CommonDMLib.getCredentials())
#Pre-processing End

retryCount = 0
endFlag = False
exceptionFlag = False
while True:
    try:
        for retryCountGetNextRef in range(10):
            workingRef = CommonDMLib.getNextRef(sheets, appname)
            if workingRef != None:
                break
            if retryCountGetNextRef == 9:
                endFlag = True
                break
        if endFlag:
            CommonDMLib.sendMessagetoSlack(mentionUser,'All daily login were completed.', appname)
            break
        if not CommonDMLib.isNoxOn() or exceptionFlag:
            print "MAIN is off"
            exceptionFlag = True
            CommonDMLib.RestartNox(NoxResources, "MAIN")
        CommonDMLib.loadRef(NoxResources, workingRef, drive)
        CommonDMLib.RestartApp(NoxResources)
        CommonDMLib.getPresent(NoxResources)
        CommonDMLib.getMissionRewards(NoxResources)
        CommonDMLib.openOmikuji(NoxResources)
        exists(NoxResources.ICON_SOLO_PLAY, 60)
        res = CommonDMLib.scanAccountInfo(NoxResources)
        CommonDMLib.updateAccountInfo(sheets, workingRef, res[0], res[1], res[2], res[3],res[4])
        CommonDMLib.completeRef(sheets, workingRef, appname)
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Instance ' + str(workingRef) + 'was completed.', appname)
        if CommonDMLib.isNewVersionAvailable():
            exit(50)
        CommonDMLib.noxCallKillDMPApp()
        wait(5)
    except:
        Settings.MoveMouseDelay = 0.1
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured in ' + str(workingRef) + '.', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.sendMessagetoSlack(mentionUser, "Screenshot" ,appname)
        if CommonDMLib.isNewVersionAvailable():
            exit(50)
        exceptionFlag = True