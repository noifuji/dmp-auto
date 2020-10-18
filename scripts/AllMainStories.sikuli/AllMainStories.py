import sys
import traceback
from datetime import datetime

sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import GameLib
import CommonDMLib

appname = 'MAIN'
mentionUser = EnvSettings.mentionUser
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
retryCount = 0
exceptionCout = 0
statisticsData = {"EPISODE":0,"STAGE":0}
instances = []
stageRegionValues = []
resources = None

###################Settings######################
LAST_EPISODE = 4
LAST_STAGE = 10
###################Settings######################

#Pre-processing Start
if EnvSettings.ENGINE_FOR_MAIN == "ANDAPP":
    import AndAppResources
    import NoxResources
    resources = AndAppResources
    CommonDMLib.exitNox(NoxResources)
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
        
        for stage_loop in range(200):
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
            
            for battle_loop in range(200):
                #バトル開始まで待機
                if CommonDMLib.waitStartingGame(resources) == -1:
                    CommonDMLib.sendMessagetoSlack(mentionUser, 'matching failed', appname)
                    break
    
                wait(10)
                # ゲームループ
                GameLib.gameLoop(resources, strategy, appname)
                # ゲームループエンド
                for battleResultLoop in range(200):
                    print "battleResultLoop..." + str(battleResultLoop)
                    CommonDMLib.skipRewards(resources)
                    if len(findAny(resources.BUTTON_DUEL_HISTORY)) > 0:
                        try:
                            click(resources.BUTTON_DUEL_HISTORY)
                        except:
                            print "failed to click"
                    if len(findAny(resources.TITLE_DUEL_HISTORY)) > 0:
                        try:
                            click(resources.BUTTON_RESULT)
                            wait(2)
                            break
                        except:
                            print "failed to click"
                    if battleResultLoop >= 199:
                        raise Exception("Too many battleResultLoop")
                #battleResultLoop End
    
                if CommonDMLib.isNewVersionAvailable():
                    exit(50)
                    
                if len(findAny(resources.ICON_WIN)) > 0:
                    click(resources.BUTTON_SMALL_OK)
                    break
                elif len(findAny(resources.ICON_LOSE)) > 0:
                    click(resources.BUTTON_SMALL_BATTLE_START)
                    retryCount += 1
                    continue
                else:
                    raise Exception("No results. restarting...")
            # battle_loop End

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
            #checkRewardLoop End

            if EnvSettings.RUN_MODE == "DEV":
                wait(1)
                CommonDMLib.uploadScreenShotToSlack(mentionUser, 'Battle Loop Count : ' + str(retryCount), appname)
            statisticsData["RETRY"] = retryCount
            statisticsData["EXCEPTION"] = exceptionCout
            statisticsData["ENDTIME"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            CommonDMLib.uploadStatistics("MainStory" ,statisticsData)
            retryCount = 0
            exceptionCout = 0

            episode = CommonDMLib.getMainStoryEpisode(resources)
            stage = CommonDMLib.getMainStoryStage(resources, 
                    stageRegionValues[0], 
                    stageRegionValues[1],
                    stageRegionValues[2],
                    stageRegionValues[3])
            if (episode > LAST_EPISODE) or (episode == LAST_EPISODE and stage >= LAST_STAGE):
                if len(findAny(resources.BUTTON_CONFIRM_REWARD)) > 0:
                    click(resources.BUTTON_CONFIRM_REWARD)
                    exists(resources.TITLE_REWARD_INFO,60)
                    if len(findAny(resources.ICON_CLEARED)) > 0:
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'All stories are cleared!', appname)
                        CommonDMLib.completeQuestStatus(instances[instanceIndex], "MAIN")
                        instanceIndex += 1
                        break
                    click(resources.BUTTON_CLOSE)

        #stage_loop End
    except SystemExit as e:
        CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(instances[instanceIndex]) + ']A new version is detected. The instance will be restarted.', appname)
        exit(e)
    except:
        exceptionCout += 1
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured. The app was restarted successfully .', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.uploadScreenShotToSlack(mentionUser, "Screenshot" , appname)
        if CommonDMLib.isNewVersionAvailable():
            exit(50)