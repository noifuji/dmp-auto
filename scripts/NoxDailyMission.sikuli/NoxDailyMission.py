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

slack_url = EnvSettings.slack_url
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
CommonDMLib.updateDeckCodes()
instances = CommonDMLib.removeCompletedInstances(instances)
#Pre-processing End

instanceIndex = 0
retryCount = 0
while instanceIndex < len(instances):
    if retryCount > 10:
        print "Too many retries. This instance will be skipped."
        retryCount = 0
        instanceIndex += 1
        continue
    
    try:
        NoxDMLib.RestartNox(NoxApp, instances[instanceIndex])
        CommonDMLib.RestartApp(NoxResources, NoxApp)
        CommonDMLib.openMission(NoxResources)
        NoxDMLib.changeMission()
        if mode == "DEV":
            wait(1)
            CommonDMLib.uploadScreenShotToSlack(mentionUser,'Account' + str(instances[instanceIndex][1]) + ' is in process.', appname)
        mission = CommonDMLib.getMissionPattern(NoxResources)
        if mission == None:
            CommonDMLib.uploadScreenShotToSlack(mentionUser,'Account' + str(instances[instanceIndex][1]) + ' is completed. Going to the next.', appname)
            NoxDMLib.closeMission()
            CommonDMLib.getPresent(NoxResources)
            res = CommonDMLib.scanAccountInfo(NoxResources)
            CommonDMLib.updateAccountInfo(instances[instanceIndex][1], "", res[0], res[1], res[2], res[3])
            CommonDMLib.updateCompletedInstanceJson(instances[instanceIndex][1]) 
            instanceIndex += 1
            continue
        strategy = CommonDMLib.getMissionStrategy(NoxResources,mission)
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
                if len(findAny("1596767585645.png")) > 0:
                    try:
                        click("1596767585645.png")
                    except:
                        print "failed to click smallStart"
                if len(findAny("1596893264220.png")) > 0:
                    break
            if dailyReward > 0:
                CommonDMLib.openMission(NoxResources)
                mission = CommonDMLib.getMissionPattern(NoxResources)
                if mode == "DEV":
                    CommonDMLib.uploadScreenShotToSlack(mentionUser, 'Mission', appname)
                if mission == None:
                    CommonDMLib.sendMessagetoSlack(mentionUser, 'Account' + str(instances[instanceIndex][1]) + ' was completed.', appname)
                    CommonDMLib.closeMission(NoxResources)
                    CommonDMLib.getPresent(NoxResources)
                    res = CommonDMLib.scanAccountInfo(NoxResources)
                    CommonDMLib.updateAccountInfo(instances[instanceIndex][1], "", res[0], res[1], res[2], res[3])
                    CommonDMLib.updateCompletedInstanceJson(instances[instanceIndex][1])
                    break
                strategy = CommonDMLib.getMissionStrategy(NoxResources,mission)
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
        retryCount += 1
        Settings.MoveMouseDelay = 0.1
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured in ' + str(instances[instanceIndex][1]) + '. Retrying....', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.uploadScreenShotToSlack(mentionUser,"Screenshot" , appname)