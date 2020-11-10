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

mentionUser = EnvSettings.mentionUser
appname = 'SP'
total_duel_count = 0
win_count =0
restart_count = 0
Settings.MoveMouseDelay = 0.1
instances = []
resources = None
targetRewardFlag = False
strategy = 101

#Pre-processing Start

if CommonDMLib.isNewVersionAvailable():
    exit(50)
CommonDMLib.downloadDeckCodes()

if EnvSettings.ENGINE_FOR_SP == "ANDAPP":
    resources = AndAppResources
    CommonDMLib.exitNox(NoxResources)
    instances = [0]
elif EnvSettings.ENGINE_FOR_SP == "NOX":
    resources = NoxResources
    App(EnvSettings.AppPath).close()
    App(EnvSettings.AndAppPath).close()
    instances = EnvSettings.NOX_INSTANCES
    statuses = CommonDMLib.downloadQuestStatus()
    temp = []
    for instance in instances:
        for status in statuses:
            if status["REF"] == str(instance) and status["SP"] == "incomplete":
                temp.append(instance)
    instances = temp
#Pre-processing End

instanceIndex = 0
while instanceIndex < len(instances):
    try:
        CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(instances[instanceIndex]) + ']launching instance...', appname)
        if EnvSettings.ENGINE_FOR_SP == "NOX":
            CommonDMLib.RestartNox(resources, instances[instanceIndex])
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
            if CommonDMLib.waitStartingGame(resources) == -1:
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
                #if EnvSettings.ENGINE_FOR_SP == "NOX":
                #    wait(random.randint(0,5))
                #else:
                #    wait(random.randint(0,2))
                    
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
                CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(instances[instanceIndex]) + ']A target reward was acquired.', appname)
                CommonDMLib.completeQuestStatus(instances[instanceIndex], "SP")
                targetRewardFlag = False
                total_duel_count = 0
                win_count =0
                instanceIndex += 1
                break

            if CommonDMLib.isNewVersionAvailable():
                exit(50)

            if len(findAny(resources.ICON_WIN)) > 0:
                win_count += 1

            click(resources.BUTTON_SMALL_BATTLE_START)
    except SystemExit as e:
        if e == 50:
            CommonDMLib.sendMessagetoSlack(mentionUser, '[' + str(instances[instanceIndex]) + ']A new version is detected. The instance will be restarted.', appname)
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