import sys
import traceback
import random
from datetime import datetime
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import GameLib
import CommonDMLib
import NoxResources
from spreadsheetapis import SpreadSheetApis

####################Settings####################
instances = EnvSettings.NOX_INSTANCES
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
CommonDMLib.downloadDeckCodes()
instances = CommonDMLib.removeCompletedInstances(instances)
sheets = SpreadSheetApis("DMPAuto", CommonDMLib.getCredentials())
#Pre-processing End

def finishMissions(instance, statisticsData):
    CommonDMLib.sendMessagetoSlack(mentionUser, 'Account' + str(instances[instanceIndex]) + ' was completed.', appname)
    CommonDMLib.closeMission(NoxResources)
    CommonDMLib.getPresent(NoxResources)
    CommonDMLib.getMissionRewards(NoxResources)
    res = CommonDMLib.scanAccountInfo(NoxResources)
    CommonDMLib.updateAccountInfo(sheets, instance, res[0], res[1], res[2], res[3],res[4], res[5])
    CommonDMLib.updateCompletedInstanceJson(instance)
    statisticsData[CommonDMLib.STATISTICS_ENDTIME] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    CommonDMLib.uploadStatistics(sheets, "DailyMission" ,statisticsData)
    if CommonDMLib.isNewVersionAvailable():
        exit(50)

statisticsData = {CommonDMLib.STATISTICS_COMPUTERNAME:"",CommonDMLib.STATISTICS_REF:"",
        CommonDMLib.STATISTICS_MISSION1:"",CommonDMLib.STATISTICS_MISSION2:"",
        CommonDMLib.STATISTICS_MISSION3:"",CommonDMLib.STATISTICS_STARTTIME:"",
        CommonDMLib.STATISTICS_ENDTIME:"",CommonDMLib.STATISTICS_EXCEPTION:0}

instanceIndex = 0
retryCount = 0
while instanceIndex < len(instances):
    
    if statisticsData[CommonDMLib.STATISTICS_REF] != str(instances[instanceIndex]):
        print "Initializing Statistics Data"
        statisticsData[CommonDMLib.STATISTICS_COMPUTERNAME] = os.environ["COMPUTERNAME"]
        statisticsData[CommonDMLib.STATISTICS_REF] = str(instances[instanceIndex])
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
    
    try:
        CommonDMLib.RestartNox(NoxResources, instances[instanceIndex])
        CommonDMLib.RestartApp(NoxResources)
        CommonDMLib.openMission(NoxResources)
        CommonDMLib.changeMission(NoxResources)
        
        missions = CommonDMLib.getTargetMissions(NoxResources)
        
        if mode == "DEV":
            wait(1)
            CommonDMLib.sendMessagetoSlack(mentionUser,'Account' + str(instances[instanceIndex]) + ' is in process.', appname)
        
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
            finishMissions(instances[instanceIndex], statisticsData)
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
                rewardResult = CommonDMLib.skipRewards(NoxResources)
                dailyReward += rewardResult["daily"]
                if dailyReward > 0:
                    if len(findAny(NoxResources.BUTTON_BACK)) > 0:
                        click(NoxResources.BUTTON_BACK)
                    if len(findAny("1604812430562.png")) > 0:
                        break
                if len(findAny(NoxResources.BUTTON_SMALL_BATTLE_START)) > 0 and dailyReward == 0:
                    try:
                        click(NoxResources.BUTTON_SMALL_BATTLE_START)
                    except:
                        print "failed to click smallStart"
                if len(findAny(NoxResources.BUTTON_LARGE_BATTLE_START)) > 0:
                    break
            if dailyReward > 0:
                CommonDMLib.openMission(NoxResources)
                missions = CommonDMLib.getTargetMissions(NoxResources)
                
                if len(missions) <= 0 or (all(elem == "SKIP" for elem in [d.get("GROUP") for d in missions])):
                    finishMissions(instances[instanceIndex], statisticsData)
                    break
                strategy = CommonDMLib.getMissionStrategy(NoxResources,missions[0])
                CommonDMLib.closeMission(NoxResources)
                CommonDMLib.openMainStory(NoxResources)
                CommonDMLib.chooseMainStoryStage(NoxResources, 1, NoxResources.TITLE_EP1_STAGE1)
                deck = CommonDMLib.getDeckByStrategy(NoxResources, strategy)
                CommonDMLib.startMainStoryBattle(NoxResources, deck[0], deck[1])
            else:
                deck = CommonDMLib.getDeckByStrategy(NoxResources, strategy)
                CommonDMLib.startMainStoryBattle(NoxResources, deck[0], deck[1])
        #バトルループエンド
        instanceIndex += 1
        retryCount = 0
    except SystemExit as e:
        if e == 50:
            CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(instances[instanceIndex]) + ']A new version is detected. The instance will be restarted.', appname)
        exit(e)
    except:
        statisticsData["EXCEPTION"] += 1
        retryCount += 1
        Settings.MoveMouseDelay = 0.1
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.uploadScreenShotToSlack(mentionUser,'Error occured in ' + str(instances[instanceIndex]) + '. Retrying....' , appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        if CommonDMLib.isNewVersionAvailable():
            exit(50)