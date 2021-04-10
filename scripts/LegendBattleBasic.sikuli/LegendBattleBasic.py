import sys
import traceback

sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import GameLib
import CommonDMLib
import AndAppResources
import NoxResources
from spreadsheetapis import SpreadSheetApis
from driveapis import DriveApis

#####Settings####
LOOP_LEVEL = 2
#####Settings####

mentionUser = EnvSettings.mentionUser
appname = 'LEGEND'
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
total_duel_count = 0
win_count =0
resources = None

sheets = SpreadSheetApis("DMPAuto", CommonDMLib.getCredentials())
#Pre-processing Start

if CommonDMLib.isNewVersionAvailable():
    exit(50)
CommonDMLib.downloadDeckCodes()

if EnvSettings.ENGINE_FOR_LEGEND == "ANDAPP":
    resources = AndAppResources
    CommonDMLib.exitNox(resources)
elif EnvSettings.ENGINE_FOR_LEGEND == "NOX":
    resources = NoxResources
    App(EnvSettings.AppPath).close()
    App(EnvSettings.AndAppPath).close()
    CommonDMLib.deleteIdentifiers()
    drive = DriveApis("DMPAuto", CommonDMLib.getCredentials())
#Pre-processing End



#全体ループ
targetRewardFlag = False
exitFlag = False
entire_loop_flag = True
level = 0
strategy = 100
exceptionCount = 0
restartCount = 0
endFlag = False
while True:
    try:
        workingRef = "0"
        if EnvSettings.ENGINE_FOR_LEGEND == "NOX":
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
                CommonDMLib.sendMessagetoSlack(mentionUser,'All Main Stories were completed.', appname)
                break
            if (not CommonDMLib.isNoxOn()) or exceptionCount > 3:
                exceptionCount = 0
                restartCount = restartCount + 1
                CommonDMLib.RestartNox(resources, "MAIN")
            CommonDMLib.loadRef(NoxResources, workingRef, drive)
        CommonDMLib.RestartApp(resources)
        click(resources.ICON_EXTRA)
        wait(3)
        click(resources.BUTTON_LEGEND_BATTLE)

        for skipTutorial in range(200):
            print "skipTutorial..." + str(skipTutorial)
            if len(findAny(resources.BUTTON_BACK2)) > 0:
                for skipTutorialLoop in range(10):
                    click(resources.BUTTON_BACK2)
                    wait(0.2)
                break
            wait(1)
        
        for selectStageLoop in range(200):
            print "selectStageLoop..." + str(selectStageLoop)
            if len(findAny(resources.TITLE_LEGEND_STAGE4)) > 0 and LOOP_LEVEL >= 4:
                level = 4
                strategy = 104
                click(resources.TITLE_LEGEND_STAGE4)
                break
            elif len(findAny(resources.TITLE_LEGEND_STAGE3)) > 0 and LOOP_LEVEL >= 3:
                level = 3
                strategy = 104
                click(resources.TITLE_LEGEND_STAGE3)
                break
            elif len(findAny(resources.TITLE_LEGEND_STAGE2)) > 0  and LOOP_LEVEL >= 2:
                level = 2
                strategy = 104
                try:
                    click(resources.TITLE_LEGEND_STAGE2)
                    break
                except:
                    print "failed to click"
            elif len(findAny(resources.TITLE_LEGEND_STAGE1)) > 0 and LOOP_LEVEL >= 1:
                level = 1
                strategy = 104
                try:
                    click(resources.TITLE_LEGEND_STAGE1)
                    break
                except:
                    print "failed to click"
                    
            wheel(resources.TITLE_LEGEND_BATTLE, Button.WHEEL_DOWN, 20)
                    
        for battleStartLoop in range(200):
            print "battleStartLoop..." + str(battleStartLoop)
            if len(findAny(resources.BUTTON_SMALL_BATTLE_START)) > 0:
                try:
                    click(resources.BUTTON_SMALL_BATTLE_START)
                except:
                    print "failed to click"
            if len(findAny(resources.BUTTON_LARGE_BATTLE_START)) > 0:
                break
            CommonDMLib.skipRewards(resources)
            CommonDMLib.skipStory(resources)
            #バトルスタートループエンド
            
        deck = CommonDMLib.getDeckByStrategy(resources, strategy)
        if CommonDMLib.chooseDeck(resources, deck[0]) == False:
            CommonDMLib.addNewDeckByCode(resources, deck[1])
        click(resources.BUTTON_LARGE_BATTLE_START)
        #バトルループ
        for battle_loop in range(200):
            #バトル開始まで待機
            if CommonDMLib.waitStartingGame(resources) == -1:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'matching failed', appname)
                continue
            wait(10)
            # ゲームループ
            gameResult = GameLib.gameLoop(resources, strategy, appname)
            # ゲームループエンド
            if not gameResult == "retire":
                total_duel_count+=1
            breakBattleLoopFlag = False
            winFlag = False
            for battleResultLoop in range(60):
                print "battleResultLoop..." + str(battleResultLoop)
                type(Key.ESC)
                #CommonDMLib.skipRewards(resources)
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
                if battleResultLoop >= 59:
                    raise Exception("Too many battleResultLoop")
                
            #if len(findAny(resources.ICON_TARGET_REWARD)) > 0:
            #    targetRewardFlag = True
                
            #if (len(findAny(resources.ICON_NEXT_REWARD_OF_TARGET)) > 0 and targetRewardFlag == True) or len(findAny(resources.ICON_REWARD_COMPLETED)) > 0:
            #    CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(workingRef) + ']A target reward was acquired.', appname)
            #    CommonDMLib.completeRef(sheets, workingRef, appname)
           #     targetRewardFlag = False
          #      total_duel_count = 0
        #        win_count =0
         #       break


            click(resources.BUTTON_CHECK_REWARD)
            exists(resources.TITLE_REWARD_POINT, 30)
            if len(findAny(resources.IMAGE_TARGET_POINT)) > 0:
                CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(workingRef) + ']A target reward was acquired.', appname)
                CommonDMLib.completeRef(sheets, workingRef, appname)
                targetRewardFlag = False
                total_duel_count = 0
                win_count =0
                break
            type(Key.ESC)
            waitVanish(resources.TITLE_REWARD_POINT, 60)
            wait(3)
                
            if CommonDMLib.isNewVersionAvailable():
                exit(50)
            
            if len(findAny(resources.ICON_WIN)) > 0:
                if level < LOOP_LEVEL:
                    click(resources.BUTTON_SMALL_OK)
                    win_count = 0
                    break
                else:
                    click(resources.BUTTON_SMALL_BATTLE_START)
                    win_count += 1
                    CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(workingRef) + ']win/total = ' + str(win_count) + "/" + str(total_duel_count), appname)
                    continue
                
            if len(findAny(resources.ICON_LOSE)) > 0:
                click(resources.BUTTON_SMALL_BATTLE_START)
                CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(workingRef) + ']win/total = ' + str(win_count) + "/" + str(total_duel_count), appname)
                continue
            
        #バトルループエンド
    except SystemExit as e:
        if e == 50:
            CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(workingRef) + ']A new version is detected. The instance will be restarted.', appname)
        exit(e)
    except:
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured. The app was restarted successfully .', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.uploadScreenShotToSlack(mentionUser, "screenshot" ,appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,"ExceptionCount:" + str(exceptionCount) + "/RestartCount:" + str(restartCount), appname)
        if restartCount > EnvSettings.RESTART_COUNT_LIMIT:
            CommonDMLib.restartOS()
            CommonDMLib.sendMessagetoSlack(mentionUser,"Restart OS", appname)
            exit()
        if CommonDMLib.isNewVersionAvailable():
            exit(50)
        CommonDMLib.noxCallKillDMPApp()
        exceptionCount = exceptionCount + 1