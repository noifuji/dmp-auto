import sys
import traceback
from datetime import datetime

sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import GameLib
import CommonDMLib

appname = 'AllMainStories'
mentionUser = EnvSettings.mentionUser
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
retryCount = 0
exceptionCout = 0
statisticsData = {"EPISODE":0,"STAGE":0}
instances = []
stageRegionValues = []
resources = None

#Pre-processing Start
if EnvSettings.ENGINE_FOR_MAIN == "ANDAPP":
    import AndAppResources
    resources = AndAppResources
    CommonDMLib.exitNox(resources)
    stageRegionValues = [-200, 240, 110, 50]
    instances = [0]
elif EnvSettings.ENGINE_FOR_MAIN == "NOX":
    import NoxResources
    resources = NoxResources
    App(EnvSettings.AppPath).close()
    App(EnvSettings.AndAppPath).close()
    stageRegionValues = [-240, 284, 118, 70]
    instances = EnvSettings.NOX_INSTANCES
    statuses = CommonDMLib.downloadQuestStatus()
    temp = []
    for instance in instances:
        for status in statuses:
            if status["REF"] == str(instance) and status["MAIN"] == "incomplete":
                temp.append(instance)
    instances = temp

if CommonDMLib.isNewVersionAvailable():
    exit(50)
    
CommonDMLib.downloadDeckCodes()
#Pre-processing End


#全体ループ
instanceIndex = 0
while instanceIndex < len(instances):
    try:
        if EnvSettings.ENGINE_FOR_MAIN == "NOX":
            CommonDMLib.RestartNox(resources, instances[instanceIndex])
        CommonDMLib.RestartApp(resources)
        CommonDMLib.openMainStory(resources)
        
        #バトルループ
        for battle_loop in range(2000):
            episode = CommonDMLib.getMainStoryEpisode(resources)
            stage = CommonDMLib.getMainStoryStage(resources, 
                    stageRegionValues[0], 
                    stageRegionValues[1],
                    stageRegionValues[2],
                    stageRegionValues[3])
            strategy = CommonDMLib.getStrategyByMainStoryStage(episode, stage)
            deck = CommonDMLib.getDeckByStrategy(resources, strategy)
            CommonDMLib.startMainStoryBattle(resources, deck[0], deck[1])
            
            #initialize statistics data
            if statisticsData["STAGE"] != stage or statisticsData["EPISODE"] != episode :
                print "Initializing Statistics Data"
                statisticsData["COMPUTERNAME"] = os.environ["COMPUTERNAME"]
                statisticsData["EPISODE"] = episode
                statisticsData["STAGE"] = stage
                statisticsData["STRATEGY"] = strategy
                statisticsData["RETRY"] = 0
                statisticsData["STARTTIME"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                statisticsData["ENDTIME"] = ""
                statisticsData["EXCEPTION"] = 0
            
            #バトル開始まで待機
            if CommonDMLib.waitStartingGame(resources) == -1:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'matching failed', appname)
                break

            wait(10)
            # ゲームループ
            GameLib.gameLoop(resources, strategy)
            # ゲームループエンド
            winFlag = False
            for battleResultLoop in range(180):
                print "battleResultLoop..." + str(battleResultLoop)
                CommonDMLib.skipRewards(resources)
                
                if len(findAny(resources.ICON_WIN)) > 0:
                    try:
                        click(resources.BUTTON_SMALL_OK)
                    except:
                        print "failed to click"
                        
                    winFlag = True
                if len(findAny(resources.ICON_LOSE)) > 0:
                    try:
                        click(resources.BUTTON_SMALL_BATTLE_START)
                    except:
                        print "failed to click"
                    winFlag = False
                if len(findAny(resources.BUTTON_SMALL_BATTLE_START)) == 0:
                    break
            if winFlag == False:
                retryCount += 1
                continue

            for checkRewardLoop in range(180):
                print "checkRewardLoop..." + str(checkRewardLoop)
                CommonDMLib.skipStory(resources)
                #レベルアップ報酬のスキップ
                CommonDMLib.skipRewards(resources)

                #エピソード選択画面にいる場合の処理
                if len(findAny(resources.BACKGROUND_EPISODE_LIST)) > 0:
                    if len(findAny(resources.EPISODES[4]["IMAGE"])) > 0:
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'Episode5 has started.', appname)
                        try:
                            click(resources.EPISODES[4]["IMAGE"])
                        except:
                            print "failed to click"
                    elif len(findAny(resources.EPISODES[3]["IMAGE"])) > 0:
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'Episode4 has started.', appname)
                        try:
                            click(resources.EPISODES[3]["IMAGE"])
                        except:
                            print "failed to click"
                    elif len(findAny(resources.EPISODES[2]["IMAGE"])) > 0:
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'Episode3 has started.', appname)
                        try:
                            click(resources.EPISODES[2]["IMAGE"])
                        except:
                            print "failed to click"
                    elif len(findAny(resources.EPISODES[1]["IMAGE"])) > 0:
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'Episode2 has started.', appname)
                        try:
                            click(resources.EPISODES[1]["IMAGE"])
                        except:
                            print "failed to click"
                if len(findAny(resources.BUTTON_CONFIRM_REWARD)) > 0:
                    try:
                        click(resources.BUTTON_CONFIRM_REWARD)
                    except:
                        print "failed to click"
                    wait(0.5)
                if len(findAny(resources.TITLE_REWARD_INFO)) > 0:
                    try:
                        click(resources.BUTTON_CLOSE)
                    except:
                        print "failed to click"
                    break

            ###Stage Cleared###
            if EnvSettings.RUN_MODE == "DEV":
                wait(1)
                CommonDMLib.uploadScreenShotToSlack(mentionUser, 'Battle Loop Count : ' + str(retryCount), appname)
            statisticsData["RETRY"] = retryCount
            statisticsData["EXCEPTION"] = exceptionCout
            statisticsData["ENDTIME"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            CommonDMLib.uploadStatistics("MainStory" ,statisticsData)
            retryCount = 0
            exceptionCout = 0
                
            if len(findAny(resources.TITLE_EP5_STAGE10)) > 0:
                if len(findAny(resources.BUTTON_CONFIRM_REWARD)) > 0:
                    click(resources.BUTTON_CONFIRM_REWARD)
                    exists(resources.TITLE_REWARD_INFO,60)
                    if len(findAny(resources.ICON_CLEARED)) > 0:
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'All stories are cleared!', appname)
                        CommonDMLib.completeQuestStatus(instances[instanceIndex], "MAIN")
                        instanceIndex += 1
                        break
                    click(resources.BUTTON_CLOSE)

            
            if CommonDMLib.isNewVersionAvailable():
                exit(50)
        #バトルループエンド
    except:
        exceptionCout += 1
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured. The app was restarted successfully .', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.uploadScreenShotToSlack(mentionUser, "Screenshot" , appname)