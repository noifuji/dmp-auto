import sys
import traceback
import random

sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import GameLib
import CommonDMLib
import AndAppResources
import NoxResources
import EnvSettings
from spreadsheetapis import SpreadSheetApis
from driveapis import DriveApis

mentionUser = EnvSettings.mentionUser
appname = 'SP'
total_duel_count = 0
win_count =0
restart_count = 0
Settings.MoveMouseDelay = 0.1
resources = None
targetRewardFlag = False
strategy = 2

def waitStartingGame(resource):
    print 'waitStartingGame'
    WAIT_TIME = 60
    myTurnCount = 0
    for num in range(WAIT_TIME):
        print "waiting game start..." + str(num) + "/" + str(WAIT_TIME)
        #ストーリースキップ
        CommonDMLib.skipStory(resource)
        #マッチングしなかった場合
        if len(findAny(resource.MESSAGE_NO_OPPONENTS)) > 0:
            try:
                click(resource.BUTTON_OK)
                wait(resource.BUTTON_SMALL_BATTLE_START, 60)
                click(resource.BUTTON_SMALL_BATTLE_START)
                wait(resource.BUTTON_LARGE_BATTLE_START,60)
                click(resource.BUTTON_LARGE_BATTLE_START)
                return -1
            except:
                print "failed to click"
        if len(findAny(resource.BUTTON_RETRY)) > 0:
            click(resource.BUTTON_RETRY)
        if len(findAny(resource.MESSAGE_ERROR_9003)) > 0:
            raise Exception
            
        if len(findAny(resource.MESSAGE_CONNECTION_LOST)) >0 :
            click(resource.BUTTON_OK)
            exists(resource.ICON_EXTRA,120)
            return -1
        if len(findAny(resource.BUTTON_TURN_END)) > 0:
            break
        if len(findAny(resource.BUTTON_SMALL_BATTLE_START)) > 0:
            break
        if num >= (WAIT_TIME-1):
            raise Exception("Too many waitStartingGame loop")
        wait(1)
    return 0

#Pre-processing Start
sheets = SpreadSheetApis("DMPAuto", CommonDMLib.getCredentials())

if CommonDMLib.isNewVersionAvailable():
    exit(50)
CommonDMLib.downloadDeckCodes()

if EnvSettings.ENGINE_FOR_SP == "ANDAPP":
    resources = AndAppResources
    CommonDMLib.exitNox(NoxResources)
elif EnvSettings.ENGINE_FOR_SP == "NOX":
    resources = NoxResources
    App(EnvSettings.AppPath).close()
    App(EnvSettings.AndAppPath).close()
    drive = DriveApis("DMPAuto", CommonDMLib.getCredentials())
#Pre-processing End

endFlag = False
while True:
    try:
        workingRef = "0"
        if EnvSettings.ENGINE_FOR_SP == "NOX":
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
            CommonDMLib.RestartNox(resources, "MAIN")
            CommonDMLib.loadRef(NoxResources, workingRef, drive)
                CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(workingRef) + ']launching instance...', appname)
        CommonDMLib.RestartApp(resources)
        wait(3)
        if len(findAny(resources.BUTTON_SP_BATTLE)) > 0:
            click(resources.BUTTON_SP_BATTLE)
        else:
            click(resources.ICON_EXTRA)
            wait(3)
            click(resources.BUTTON_SP_BATTLE)

        for battleStartLoop in range(200):
            print "battleStartLoop..." + str(battleStartLoop)
            if len(findAny(resources.BUTTON_BACK2)) > 0:
                for skipTutorialLoop in range(10):
                    try:
                        click(resources.BUTTON_BACK2)
                    except:
                        print "failed to click"
                    wait(0.2)
            if len(findAny(resources.BUTTON_SMALL_BATTLE_START)) > 0:
                try:
                    click(resources.BUTTON_SMALL_BATTLE_START)
                except:
                    print "failed to click"
            if len(findAny(resources.BUTTON_LARGE_BATTLE_START)) > 0:
                deck = CommonDMLib.getDeckByStrategy(resources, strategy)
                if CommonDMLib.chooseDeck(resources, deck[0]) == False:
                    CommonDMLib.addNewDeckByCode(resources, deck[1])
                click(resources.BUTTON_LARGE_BATTLE_START)
                break
        
        #バトルループ
        for battle_loop in range(2000):
        
            #マッチングを待つ
            if waitStartingGame(resources) == -1:
                if EnvSettings.RUN_MODE == "DEV":
                    CommonDMLib.sendMessagetoSlack(mentionUser, 'matching failed', appname)
                continue
    
            turn_count = 0
            for game_loop in range(10):
    
                #if len(findAny(resources.BUTTON_TURN_END)) > 0:
                    #print 'click turnend'
                    #for turnendLoop in range(20):
                    #    GameLib.turnEnd(resources)
                    #    if len(findAny(resources.BUTTON_ENEMY_TURN, resources.BUTTON_SMALL_BATTLE_START)) > 0:
                    #        break
                    
                    #turn_count += 1
                    
                #if turn_count >= 0 :
                if EnvSettings.ENGINE_FOR_SP == "NOX":
                    wait(random.randint(0,5))
                else:
                    wait(random.randint(0,2))
                    
                print 'retire'
                GameLib.retire(resources)
                
                if GameLib.irregularLoop(resources, appname) == 0:
                    break

                if game_loop >= 14:
                    raise Exception("over game loop limit")
                
            #ゲームループエンド
            total_duel_count+=1
            if EnvSettings.RUN_MODE == "DEV":
                if total_duel_count % 5 == 0:
                    CommonDMLib.sendMessagetoSlack(mentionUser,'WIN/TOTAL = ' + str(win_count) + "/" + str(total_duel_count), appname)
         
            for battleResultLoop in range(200):
                print "battleResultLoop..." + str(battleResultLoop)
                type(Key.ESC)
                if len(findAny(resources.BUTTON_DUEL_HISTORY)) > 0:
                    try:
                        click(resources.BUTTON_DUEL_HISTORY)
                    except:
                        print "failed to click"
                if len(findAny(resources.TITLE_DUEL_HISTORY)) > 0:
                    try:
                        click(resources.BUTTON_RESULT)
                        wait(0.5)
                    except:
                        print "failed to click"
                    break
                if battleResultLoop >= 199:
                    raise Exception("Too many battleResultLoop")

            if len(findAny(resources.ICON_SP_TARGET_REWARD)) > 0:
                targetRewardFlag = True
                
            if (len(findAny(resources.ICON_NEXT_REWARD_OF_TARGET)) > 0 and targetRewardFlag == True) or len(findAny(resources.ICON_REWARD_COMPLETED)) > 0:
                CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(workingRef) + ']A target reward was acquired.', appname)
                CommonDMLib.completeRef(sheets, workingRef, appname)
                targetRewardFlag = False
                total_duel_count = 0
                win_count =0
                break
            
            if total_duel_count % 5 == 0:
                if CommonDMLib.isNewVersionAvailable():
                    exit(50)

            if len(findAny(resources.ICON_WIN)) > 0:
                win_count += 1

            click(resources.BUTTON_SMALL_BATTLE_START)
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
        CommonDMLib.exitNox(NoxResources)