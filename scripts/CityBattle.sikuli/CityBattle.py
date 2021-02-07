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
TARGETS = [Pattern("1612247246785.png").similar(0.89),Pattern("1612247256112.png").similar(0.86)]
TARGETS_COMP = [Pattern("1612247604601.png").similar(0.90),Pattern("1612247613700.png").similar(0.90)]
#####Settings####

mentionUser = EnvSettings.mentionUser
appname = 'SP'
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
strategy = 104
endFlag = False
targetIndex = 0
exceptionFlag = False
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
                CommonDMLib.sendMessagetoSlack(mentionUser,'All City Stories were completed.', appname)
                break
            if (not CommonDMLib.isNoxOn()) or exceptionFlag:
                print "restarting Nox..."
                exceptionFlag = False
                CommonDMLib.RestartNox(resources, "MAIN")
            CommonDMLib.loadRef(NoxResources, workingRef, drive)
        CommonDMLib.RestartApp(resources)
        CommonDMLib.openCityBattle(resources)

        exitFlag = True
        targetIndex = 0
        for (tar, comp) in zip(TARGETS, TARGETS_COMP):
            if len(findAny(comp)) == 0 and len(findAny(tar)) > 0:
                click(tar)
                click(resources.BUTTON_SMALL_BATTLE_START)
                exitFlag = False
                break
            targetIndex = targetIndex + 1

        if exitFlag:
            CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(workingRef) + ']All targets were acquired.', appname)
            CommonDMLib.completeRef(sheets, workingRef, appname)
            CommonDMLib.noxCallKillDMPApp()
            wait(5)
            continue

        exists(resources.BUTTON_LARGE_BATTLE_START,60)
        deck = CommonDMLib.getDeckByStrategy(resources, strategy)
        if CommonDMLib.chooseDeck(resources, deck[0]) == False:
            CommonDMLib.addNewDeckByCode(resources, deck[1])
        click(resources.BUTTON_LARGE_BATTLE_START)
        #バトルループ
        for battle_loop in range(200):
            if total_duel_count % 5 == 0:
                CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(workingRef) + ']win/total = ' + str(win_count) + "/" + str(total_duel_count), appname)
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

            if CommonDMLib.isNewVersionAvailable():
                exit(50)
            
            if len(findAny(resources.ICON_WIN)) > 0:
                if len(findAny(resources.IMAGE_NO_REWARDS)) > 0:
                    CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(workingRef) + ']The target ' + str(targetIndex) + ' was completed.', appname)
                    win_count = 0
                    total_duel_count = 0
                    break
                else:
                    win_count = win_count + 1
                
            click(resources.BUTTON_SMALL_BATTLE_START)
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
        if CommonDMLib.isNewVersionAvailable():
            exit(50)
        exceptionFlag = True
