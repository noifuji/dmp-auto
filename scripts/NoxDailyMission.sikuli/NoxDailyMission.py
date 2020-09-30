import sys
import traceback
import random
from datetime import datetime
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import NoxDMLib
import CommonDMLib
import NoxResources

####################Settings####################
Avator = Pattern("Avator.png").targetOffset(376,-12)
instances = EnvSettings.NOX_INSTANCES
####################Settings####################

mentionUser = EnvSettings.mentionUser
NoxAppPath = EnvSettings.NoxAppPath
NoxApp = App(NoxAppPath)
appname = 'NoxDailyMission'
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
mode = EnvSettings.RUN_MODE

#Pre-processing Start        
App(EnvSettings.AppPath).close()
App(EnvSettings.AndAppPath).close()

if CommonDMLib.isNewVersionAvailable():
    exit(50)
CommonDMLib.downloadDeckCodes()
instances = CommonDMLib.removeCompletedInstances(instances)
#Pre-processing End

def finishMissions(instance, statisticsData):
    CommonDMLib.sendMessagetoSlack(mentionUser, 'Account' + str(instances[instanceIndex]) + ' was completed.', appname)
    CommonDMLib.closeMission(NoxResources)
    CommonDMLib.getPresent(NoxResources)
    res = CommonDMLib.scanAccountInfo(NoxResources)
    CommonDMLib.updateAccountInfo(instance, res[0], res[1], res[2], res[3],res[4])
    CommonDMLib.updateCompletedInstanceJson(instance)
    statisticsData[CommonDMLib.STATISTICS_ENDTIME] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    CommonDMLib.uploadStatistics("DailyMission" ,statisticsData)
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
    
    if retryCount > 3:
        print "Too many retries. This instance will be skipped."
        retryCount = 0
        instanceIndex += 1
        continue
    
    try:
        NoxDMLib.RestartNox(instances[instanceIndex])
        CommonDMLib.RestartApp(NoxResources, NoxApp)
        CommonDMLib.openMission(NoxResources)
        NoxDMLib.changeMission()
        if mode == "DEV":
            wait(1)
            CommonDMLib.uploadScreenShotToSlack(mentionUser,'Account' + str(instances[instanceIndex]) + ' is in process.', appname)
        
        missions = CommonDMLib.getTargetMissions(NoxResources)
        
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
            for game_loop in range(50):
                print "Inside Game Loop : " + str(game_loop)
                try:
                    click("1598831333684.png")
                except:
                    print "failed to click card count"
                wait(0.5)
                #  手札選択
                if len(findAny(Avator)) > 0:
                    click(Avator)
                    wait(1)
    
                if strategy == 1:
                    print "SPELL_MISSIONS"
                    
                elif strategy == 2:
                    print "SPEED_MISSIONS"
                    #  マナチャージ
                    currentMana = NoxDMLib.ChargeManaRedBlack()
                    wait(1)
                    #  召喚
                    NoxDMLib.SummonRedBlack(currentMana)
                    wait(1)
                    #  攻撃
                    NoxDMLib.directAttack("1596773359735.png")
                elif strategy == 3:
                    print "BATTLE_MISSIONS"
                    #  攻撃
                    NoxDMLib.battle()
                elif strategy == 4:
                    print "SHIELDTRRIGER_MISSIONS"
                elif strategy == 5:
                    print "LARGE_CREATURES"
                    #  マナチャージ
                    currentMana = NoxDMLib.ChargeMana5()
                    wait(1)
                    #  召喚
                    NoxDMLib.Summon5(currentMana)
                    wait(1)
                    #  攻撃
                    if random.random() < 0.5:
                        NoxDMLib.directAttack("1596773359735.png")
                elif strategy == 6:
                    print "RETIRE"
                    NoxDMLib.retire()
                    exists("1596767585645.png",120)
                    
                #  ターンエンド
                if exists("1596773380235.png",10) != None:
                    click(Pattern("1597036183485.png").similar(0.85).targetOffset(-100,206))
                
                wait(1)
                #  イレギュラーループ
                if NoxDMLib.irregularLoop() == 0:
                    break
    
            # ゲームループエンド
            #レベルアップ報酬のスキップ
            for battleResultLoop in range(180):
                CommonDMLib.skipRewards(NoxResources)
                if exists("1596893006314.png",1) != None:
                    click("1596893006314.png")
                else:
                    break
            dailyReward = 0
            for checkRewardLoop in range(180):
                CommonDMLib.skipStory(NoxResources)
                rewardResult = CommonDMLib.skipRewards(NoxResources)
                dailyReward += rewardResult["daily"]
                if dailyReward > 0:
                    if len(findAny(Pattern("1596952408522.png").similar(0.85))) > 0:
                        click(Pattern("1596952408522.png").similar(0.85))
                    if len(findAny("1596952469317.png")) > 0:
                        break
                if len(findAny("1596767585645.png")) > 0 and dailyReward == 0:
                    try:
                        click("1596767585645.png")
                    except:
                        print "failed to click smallStart"
                if len(findAny("1596893264220.png")) > 0:
                    break
            if dailyReward > 0:
                CommonDMLib.openMission(NoxResources)
                
                missions = CommonDMLib.getTargetMissions(NoxResources)
                if mode == "DEV":
                    CommonDMLib.uploadScreenShotToSlack(mentionUser, 'Mission', appname)
                
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
    except:
        statisticsData["EXCEPTION"] += 1
        retryCount += 1
        Settings.MoveMouseDelay = 0.1
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured in ' + str(instances[instanceIndex]) + '. Retrying....', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.uploadScreenShotToSlack(mentionUser,"Screenshot" , appname)