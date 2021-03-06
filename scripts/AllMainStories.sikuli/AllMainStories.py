import sys
import traceback
from datetime import datetime

sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import GameLib
import CommonDMLib
from spreadsheetapis import SpreadSheetApis
from driveapis import DriveApis

###################Settings######################
NORMAL_LAST_EPISODE = 4
NORMAL_LAST_STAGE = 10
RESET_LAST_EPISODE = 2
RESET_LAST_STAGE = 14
###################Settings######################

appname = 'MAIN'
mentionUser = EnvSettings.mentionUser
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
retryCount = 0
exceptionCout = 0
statisticsData = {"EPISODE":0,"STAGE":0}
resources = None

if len(sys.argv) >= 2 and sys.argv[1] == "reset":
    print "reset mode is selected."
    LAST_EPISODE = RESET_LAST_EPISODE
    LAST_STAGE = RESET_LAST_STAGE
else:
    LAST_EPISODE = NORMAL_LAST_EPISODE
    LAST_STAGE = NORMAL_LAST_STAGE

def isClearedStage(resources):
    res = False
    if len(findAny(resources.BUTTON_CONFIRM_REWARD)) > 0:
        click(resources.BUTTON_CONFIRM_REWARD)
        exists(resources.TITLE_REWARD_INFO,60)
        if len(findAny(resources.ICON_CLEARED)) > 0:
            res = True
        click(resources.BUTTON_CLOSE)
        wait(3)
    return res

#Pre-processing Start
sheets = SpreadSheetApis("DMPAuto", CommonDMLib.getCredentials())
if EnvSettings.ENGINE_FOR_MAIN == "ANDAPP":
    import AndAppResources
    import NoxResources
    resources = AndAppResources
    App(EnvSettings.NoxAppPath).close()
elif EnvSettings.ENGINE_FOR_MAIN == "NOX":
    import NoxResources
    resources = NoxResources
    App(EnvSettings.AppPath).close()
    App(EnvSettings.AndAppPath).close()
    CommonDMLib.deleteIdentifiers()
    drive = DriveApis("DMPAuto", CommonDMLib.getCredentials())

if CommonDMLib.isNewVersionAvailable():
    exit(50)

    
#Pre-processing End


#全体ループ
endFlag = False
exceptionFlag = False
while True:
    try:
        CommonDMLib.downloadDeckCodes()
        workingRef = "0"
        if EnvSettings.ENGINE_FOR_MAIN == "NOX":
            workingRef = None
            #Load Ref No
            for retryCountGetNextRef in range(10):
                workingRef = CommonDMLib.getNextRef(sheets, appname)
                if workingRef != None:
                    break
                if retryCountGetNextRef == 9:
                    endFlag = True
                    break
            if endFlag:
                CommonDMLib.sendMessagetoSlack("INFO", mentionUser,'All Main Stories were completed.', appname)
                break
            if not CommonDMLib.isNoxOn() or exceptionFlag:
                exceptionFlag = False
                CommonDMLib.RestartNox(resources, "MAIN")
            CommonDMLib.loadRef(NoxResources, workingRef, drive)
        CommonDMLib.sendMessagetoSlack("DEBUG", mentionUser, "["+str(workingRef)+"]"+'launching...', appname)
        CommonDMLib.RestartApp(resources)
        CommonDMLib.openMainStory(resources)
        
        for stage_loop in range(200):
            episode = CommonDMLib.getMainStoryEpisode(resources)
            stage = CommonDMLib.getMainStoryStage(resources)

            if (episode > LAST_EPISODE) or (episode == LAST_EPISODE and stage > LAST_STAGE) or \
                    (episode == LAST_EPISODE and stage == LAST_STAGE and isClearedStage(resources)):
                if len(sys.argv) >= 2 and sys.argv[1] == "reset" and EnvSettings.ENGINE_FOR_MAIN == "NOX":
                    for checkRewardLoop in range(180):
                        if len(findAny(NoxResources.BUTTON_BACK)) > 0:
                            click(NoxResources.BUTTON_BACK)
                        if len(findAny(NoxResources.ICON_HOME)) > 0:
                            break
                    CommonDMLib.getPresent(NoxResources)
                    CommonDMLib.getMissionRewards(NoxResources)
                    res = CommonDMLib.scanAccountInfo(NoxResources)
                    CommonDMLib.updateAccountInfo(sheets, workingRef, res[0], res[1], res[2], res[3],res[4])
                CommonDMLib.sendMessagetoSlack("DEBUG", mentionUser, 'All stories were cleared!', appname)
                CommonDMLib.completeRef(sheets, workingRef, "MAIN")
                CommonDMLib.noxCallKillDMPApp()
                break
            
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
                    CommonDMLib.sendMessagetoSlack("ERROR", mentionUser, 'matching failed', appname)
                    break
    
                # ゲームループ
                gameResult = GameLib.gameLoop(resources, strategy, appname)
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
                    if gameResult != "retire":
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
                        CommonDMLib.sendMessagetoSlack("DEBUG", mentionUser, 'Episode5 has started.', appname)
                        try:
                            click(resources.EPISODES[4]["IMAGE"])
                        except:
                            print "failed to click"
                    elif len(findAny(resources.EPISODES[3]["IMAGE"])) > 0:
                        CommonDMLib.sendMessagetoSlack("DEBUG", mentionUser, 'Episode4 has started.', appname)
                        try:
                            click(resources.EPISODES[3]["IMAGE"])
                        except:
                            print "failed to click"
                    elif len(findAny(resources.EPISODES[2]["IMAGE"])) > 0:
                        CommonDMLib.sendMessagetoSlack("DEBUG", mentionUser, 'Episode3 has started.', appname)
                        try:
                            click(resources.EPISODES[2]["IMAGE"])
                        except:
                            print "failed to click"
                    elif len(findAny(resources.EPISODES[1]["IMAGE"])) > 0:
                        CommonDMLib.sendMessagetoSlack("DEBUG", mentionUser, 'Episode2 has started.', appname)
                        try:
                            click(resources.EPISODES[1]["IMAGE"])
                        except:
                            print "failed to click"

                #レビュー依頼をキャンセルする。
                if len(findAny(resources.BUTTON_CANCEL)) > 0:
                    try:
                        click(resources.BUTTON_CANCEL)
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
                CommonDMLib.sendMessagetoSlack("DEBUG", mentionUser, "["+str(workingRef)+"]"+'[EP:'+str(episode)+',ST:'+str(stage)+']Battle Loop Count : ' + str(retryCount), appname)
            statisticsData["RETRY"] = retryCount
            statisticsData["EXCEPTION"] = exceptionCout
            statisticsData["ENDTIME"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            CommonDMLib.uploadStatistics(sheets, "MainStory" ,statisticsData)
            retryCount = 0
            exceptionCout = 0

            if CommonDMLib.checkPrepareGameTradeDraft() != None:
                exit(60)

        #stage_loop End
    except SystemExit as e:
        if str(e) == "50":
            CommonDMLib.sendMessagetoSlack("INFO", mentionUser, '[' + str(workingRef) + ']A new version is detected. The instance will be restarted.', appname)
        exit(e)
        
        if str(e) == "60":
            CommonDMLib.sendMessagetoSlack("INFO", mentionUser, 'QuickPrepare will be started.', appname)
        exit(e)
    except:
        exceptionCout += 1
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack("ERROR", mentionUser, 'Error occured. The app was restarted successfully .', appname)
        CommonDMLib.sendMessagetoSlack("ERROR", mentionUser,traceback.format_exc(), appname)
        CommonDMLib.uploadScreenShotToSlack(mentionUser, "Screenshot" , appname)
        if CommonDMLib.isNewVersionAvailable():
            exit(50)
        if EnvSettings.ENGINE_FOR_MAIN == "NOX":
            exceptionFlag = True