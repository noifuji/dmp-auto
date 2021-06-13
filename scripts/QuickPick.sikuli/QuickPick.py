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
appname = 'SP'
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
restartCount = 0
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
            CommonDMLib.sendMessagetoSlack("INFO", mentionUser,'All QuickPick were completed.', appname)
            break
        if (not CommonDMLib.isNoxOn()) or exceptionFlag:
            print "MAIN is off"
            exceptionFlag = False
            restartCount = restartCount + 1
            CommonDMLib.RestartNox(NoxResources, "MAIN")
        CommonDMLib.loadRef(NoxResources, workingRef, drive)
        CommonDMLib.RestartApp(NoxResources)

        
        exists(NoxResources.ICON_SOLO_PLAY, 60)

        #open quick pick
        click(NoxResources.BUTTON_QUICK_PICK)
        exists(NoxResources.BUTTON_BACK, 60)
        #skip tutorial
        for num in range(10):
            click(NoxResources.BUTTON_BACK2)
            wait(1)
        

        #deck loop
        for loopCount in range(100):
            #check ticket quantity
            if exists(NoxResources.BUTTON_ENTER_USING_TICKT, 60) == None:
                break
            
            #create deck
            click(NoxResources.BUTTON_ENTER_USING_TICKT)
            wait(5)
            click(NoxResources.BUTTON_OK)
            exists(NoxResources.BUTTON_CREATE_DECK, 60)
            click(NoxResources.BUTTON_CREATE_DECK)

            for selectLoopCount in range(50):
                if exists(NoxResources.BUTTON_SELECT, 60) == None:
                    break
                wait(5)
                click(NoxResources.BUTTON_SELECT)
                wait(5)

            exists(NoxResources.BUTTON_QUICKPICK_RETIRE, 60)
            click(NoxResources.BUTTON_QUICKPICK_RETIRE)
            wait(5)
            click(NoxResources.BUTTON_OK)
            exists(NoxResources.BUTTON_QUICKPICK_REWARD, 60)
            click(NoxResources.BUTTON_QUICKPICK_REWARD)
            wait(5)
            click(NoxResources.BUTTON_OK)
            

        
        CommonDMLib.completeRef(sheets, workingRef, appname)
        CommonDMLib.sendMessagetoSlack("DEBUG", mentionUser, 'Instance ' + str(workingRef) + 'was completed.', appname)
        if CommonDMLib.isNewVersionAvailable():
            exit(50)

        if CommonDMLib.checkPrepareGameTradeDraft() != None:
            exit(60)
            
        CommonDMLib.noxCallKillDMPApp()
        wait(5)
            
    except SystemExit as e:
        if str(e) == "50":
            CommonDMLib.sendMessagetoSlack("INFO", mentionUser, '[' + str(workingRef) + ']A new version is detected. The instance will be restarted.', appname)
            exit(e)
        
        if str(e) == "60":
            CommonDMLib.sendMessagetoSlack("INFO", mentionUser, 'QuickPrepare will be started.', appname)
            exit(e)
    
    except:
        Settings.MoveMouseDelay = 0.1
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack("ERROR", mentionUser, 'Error occured in ' + str(workingRef) + '.', appname)
        CommonDMLib.sendMessagetoSlack("ERROR", mentionUser,traceback.format_exc(), appname)
        CommonDMLib.sendMessagetoSlack("ERROR", mentionUser, "Screenshot" ,appname)
        CommonDMLib.sendMessagetoSlack("ERROR", mentionUser,"RestartCount:" + str(restartCount), appname)
        if restartCount > EnvSettings.RESTART_COUNT_LIMIT:
            CommonDMLib.restartOS()
            CommonDMLib.sendMessagetoSlack("ERROR", mentionUser,"Restart OS", appname)
            exit()
        if CommonDMLib.isNewVersionAvailable():
            exit(50)
        exceptionFlag = True