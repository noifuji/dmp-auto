import sys
import traceback
import random
from datetime import datetime, timedelta
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import GameLib
import CommonDMLib
import NoxResources
from spreadsheetapis import SpreadSheetApis
from driveapis import DriveApis

####################Settings####################
####################Settings####################

mentionUser = EnvSettings.mentionUser
appname = 'DAILY'
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
mode = EnvSettings.RUN_MODE
MAX_RETRY_COUNT = 10

#Pre-processing Start        
App(EnvSettings.AppPath).close()
App(EnvSettings.AndAppPath).close()

if CommonDMLib.isNewVersionAvailable():
    exit(50)
CommonDMLib.deleteIdentifiers()
CommonDMLib.downloadDeckCodes()
sheets = SpreadSheetApis("DMPAuto", CommonDMLib.getCredentials())
drive = DriveApis("DMPAuto", CommonDMLib.getCredentials())
#Pre-processing End

def finishMissions(instance, statisticsData, sheets):
    CommonDMLib.sendMessagetoSlack(mentionUser, 'Account' + str(instance) + ' was completed.', appname)
    CommonDMLib.closeMission(NoxResources)
    CommonDMLib.getPresent(NoxResources)
    CommonDMLib.getMissionRewards(NoxResources)
    #CommonDMLib.openOmikuji(NoxResources)
    if CommonDMLib.getBeginnerRewards(NoxResources):
        CommonDMLib.openCardPack(NoxResources)
    if datetime.now().day == 2 or datetime.now().day == 16:
        for openCardListLoop in range(100):
            if len(findAny(NoxResources.ICON_CARD)) > 0:
                try:
                    click(NoxResources.ICON_CARD)
                except:
                    print "failed to click"
                wait(1)
            if len(findAny(NoxResources.BUTTON_CARD_LIST)) > 0:
                try:
                    click(NoxResources.BUTTON_CARD_LIST)
                except:
                    print "failed to click"
                wait(1)
            if len(findAny(NoxResources.BUTTON_BACK2)) > 0:
                break
        if exists(NoxResources.BUTTON_BACK2, 120) != None:
            for listTutorialLoop in range(10):
                click(NoxResources.BUTTON_BACK2)
                wait(0.2)
        cardCountResult = CommonDMLib.countAllCardsByRarity(NoxResources)
        CommonDMLib.updateCardCount(sheets, instance, cardCountResult["NAMES"], cardCountResult["CARDS"])
        type(Key.ESC)
        exists(NoxResources.ICON_SOLO_PLAY, 60)
    res = CommonDMLib.scanAccountInfo(NoxResources)
    CommonDMLib.updateAccountInfo(sheets, instance, res[0], res[1], res[2], res[3],res[4])
    CommonDMLib.completeRef(sheets, instance, appname)
    statisticsData[CommonDMLib.STATISTICS_ENDTIME] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    CommonDMLib.uploadStatistics(sheets, "DailyMission" ,statisticsData)
    if CommonDMLib.isNewVersionAvailable():
        exit(50)
    CommonDMLib.noxCallKillDMPApp()

statisticsData = {CommonDMLib.STATISTICS_COMPUTERNAME:"",CommonDMLib.STATISTICS_REF:"",
        CommonDMLib.STATISTICS_MISSION1:"",CommonDMLib.STATISTICS_MISSION2:"",
        CommonDMLib.STATISTICS_MISSION3:"",CommonDMLib.STATISTICS_STARTTIME:"",
        CommonDMLib.STATISTICS_ENDTIME:"",CommonDMLib.STATISTICS_EXCEPTION:0}



instanceIndex = 0
retryCount = 0
exceptionCount = 0
restartCount = 0
endFlag = False
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
            CommonDMLib.sendMessagetoSlack(mentionUser,'All daily missions were completed.', appname)
            break
        
        if statisticsData[CommonDMLib.STATISTICS_REF] != str(workingRef):
            print "Initializing Statistics Data"
            statisticsData[CommonDMLib.STATISTICS_COMPUTERNAME] = os.environ["COMPUTERNAME"]
            statisticsData[CommonDMLib.STATISTICS_REF] = str(workingRef)
            statisticsData[CommonDMLib.STATISTICS_MISSION1] = ""
            statisticsData[CommonDMLib.STATISTICS_MISSION2] = ""
            statisticsData[CommonDMLib.STATISTICS_MISSION3] = ""
            statisticsData[CommonDMLib.STATISTICS_STARTTIME] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            statisticsData[CommonDMLib.STATISTICS_ENDTIME] = ""
            statisticsData[CommonDMLib.STATISTICS_EXCEPTION] = 0
        
        if retryCount > MAX_RETRY_COUNT:
            print "Too many retries. This instance will be skipped."
            retryCount = 0
            instanceIndex += 1
            continue
        
        if (not CommonDMLib.isNoxOn()) or exceptionCount > 3:
            print "restarting Nox..."
            exceptionCount = 0
            CommonDMLib.RestartNox(NoxResources, "MAIN")
            restartCount = restartCount + 1
        CommonDMLib.loadRef(NoxResources, workingRef, drive)
        CommonDMLib.RestartApp(NoxResources)
        CommonDMLib.openMission(NoxResources)
        CommonDMLib.changeMission(NoxResources)
        
        missions = CommonDMLib.getTargetMissions(NoxResources)
        
        if mode == "DEV":
            wait(1)
            CommonDMLib.sendMessagetoSlack(mentionUser,'Account' + str(workingRef) + ' is in process.', appname)
        
        if statisticsData[CommonDMLib.STATISTICS_MISSION1] == "":
            for i in range(len(missions)):
                if i == 0:
                    statisticsData[CommonDMLib.STATISTICS_MISSION1] = missions[i]["NAME"]
                elif i == 1:
                    statisticsData[CommonDMLib.STATISTICS_MISSION2] = missions[i]["NAME"]
                elif i == 2:
                    statisticsData[CommonDMLib.STATISTICS_MISSION3] = missions[i]["NAME"]
            print statisticsData
            
        if len(missions) <= 0 or (all(elem == "SKIP" for elem in [d.get("GROUP") for d in missions])):
            finishMissions(workingRef, statisticsData ,sheets)
            instanceIndex += 1
            retryCount = 0
            continue
        
        strategy = CommonDMLib.getMissionStrategy(NoxResources,missions[0])
        CommonDMLib.closeMission(NoxResources)
        CommonDMLib.openMainStory(NoxResources)
        CommonDMLib.chooseMainStoryStage(NoxResources, 1, NoxResources.TITLE_EP1_STAGE1)
        deck = CommonDMLib.getDeckByStrategy(NoxResources, strategy)
        CommonDMLib.startMainStoryBattle(NoxResources, deck[0], deck[1])
        
        #バトルループ
        for battle_loop in range(200):
            #バトル開始まで待機
            if CommonDMLib.waitStartingGame(NoxResources) == -1:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'matching failed', appname)
                raise Exception
    
            wait(10)
            # ゲームループ
            GameLib.gameLoop(NoxResources, strategy, appname)
            # ゲームループエンド
            #レベルアップ報酬のスキップ
            for battleResultLoop in range(180):
                CommonDMLib.skipRewards(NoxResources)
                if exists(NoxResources.BUTTON_SMALL_OK,1) != None:
                    click(NoxResources.BUTTON_SMALL_OK)
                else:
                    break
            dailyReward = 0
            for checkRewardLoop in range(180):
                CommonDMLib.skipStory(NoxResources)
                type(Key.ESC)
                wait(1)
                #if len(findAny(NoxResources.BUTTON_BACK)) > 0:
                #    click(NoxResources.BUTTON_BACK)
                if len(findAny(NoxResources.MESSAGE_CONFIRM_BACK_TITLE)) > 0:
                    type(Key.ESC)
                    wait(1)
                    break
            CommonDMLib.openMission(NoxResources)
            missions = CommonDMLib.getTargetMissions(NoxResources)
            if len(missions) <= 0 or (all(elem == "SKIP" for elem in [d.get("GROUP") for d in missions])):
                click(NoxResources.BUTTON_DAILY_REWARD_RECEIVE_ALL)
                exists(NoxResources.BUTTON_OK, 60)
                click(NoxResources.BUTTON_OK)
                finishMissions(workingRef, statisticsData, sheets)
                break
            strategy = CommonDMLib.getMissionStrategy(NoxResources,missions[0])
            CommonDMLib.closeMission(NoxResources)
            CommonDMLib.openMainStory(NoxResources)
            CommonDMLib.chooseMainStoryStage(NoxResources, 1, NoxResources.TITLE_EP1_STAGE1)
            deck = CommonDMLib.getDeckByStrategy(NoxResources, strategy)
            CommonDMLib.startMainStoryBattle(NoxResources, deck[0], deck[1])
        #バトルループエンド
        instanceIndex += 1
        retryCount = 0
    except SystemExit as e:
        if e == 50:
            CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(workingRef) + ']A new version is detected. The instance will be restarted.', appname)
        exit(e)
    except:
        statisticsData["EXCEPTION"] += 1
        retryCount += 1
        Settings.MoveMouseDelay = 0.1
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.uploadScreenShotToSlack(mentionUser,'Error occured in ' + str(workingRef) + '. Retrying....' , appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        if restartCount > EnvSettings.RESTART_COUNT_LIMIT:
            CommonDMLib.restartOS()
            CommonDMLib.sendMessagetoSlack(mentionUser,"Restart OS", appname)
            exit()
        if CommonDMLib.isNewVersionAvailable():
            exit(50)
        CommonDMLib.noxCallKillDMPApp()
        exceptionCount = exceptionCount + 1
        wait(5)