import sys
import traceback

sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import GameLib
import NoxDMLib
import CommonDMLib
import AndAppResources
import NoxResources

#####Settings####
LOOP_LEVEL = 2
#####Settings####

mentionUser = EnvSettings.mentionUser
appname = 'LegendBattle'
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
total_duel_count = 0
win_count =0
instances = []
resources = None

#Pre-processing Start
App(EnvSettings.AppPath).close()
App(EnvSettings.AndAppPath).close()
NoxDMLib.exitNox()

if CommonDMLib.isNewVersionAvailable():
    exit(50)
CommonDMLib.downloadDeckCodes()

if EnvSettings.ENGINE_FOR_LEGEND == "ANDAPP":
    resources = AndAppResources
    instances = [0]
elif EnvSettings.ENGINE_FOR_LEGEND == "NOX":
    resources = NoxResources
    instances = EnvSettings.NOX_INSTANCES
    statuses = CommonDMLib.downloadQuestStatus()
    temp = []
    for instance in instances:
        for status in statuses:
            if status["REF"] == str(instance) and status["MAIN"] == "incomplete":
                temp.append(instance)
    instances = temp
#Pre-processing End



#全体ループ
targetRewardFlag = False
exitFlag = False
entire_loop_flag = True
level = 0
strategy = 100
instanceIndex = 0
while instanceIndex < len(instances):
    try:
        if EnvSettings.ENGINE_FOR_MAIN == "NOX":
            NoxDMLib.RestartNox(instances[instanceIndex])
        CommonDMLib.RestartApp(resources)
        click(resources.ICON_EXTRA)
        wait(3)
        click(resources.BUTTON_LEGEND_BATTLE)
    
    
        for battleStartLoop in range(200):
            print "battleStartLoop..." + str(battleStartLoop)
            if len(findAny(resources.BUTTON_BACK2)) > 0:
                for skipTutorialLoop in range(10):
                    click(resources.BUTTON_BACK2)
                    wait(0.2)
            if len(findAny(resources.TITLE_LEGEND_STAGE3)) > 0 and LOOP_LEVEL >= 3:
                level = 3
                click(resources.TITLE_LEGEND_STAGE3)
            elif len(findAny(resources.TITLE_LEGEND_STAGE2)) > 0  and LOOP_LEVEL >= 2:
                level = 2
                strategy = 2
                try:
                    click(resources.TITLE_LEGEND_STAGE2)
                except:
                    print "failed to click"
            elif len(findAny(resources.TITLE_LEGEND_STAGE1)) > 0 and LOOP_LEVEL >= 1:
                level = 1
                strategy = 2
                try:
                    click(resources.TITLE_LEGEND_STAGE1)
                except:
                    print "failed to click"

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
            if battle_loop % 10 == 0:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'win/total = ' + str(win_count) + "/" + str(battle_loop), appname)
            #バトル開始まで待機
            if CommonDMLib.waitStartingGame(resources) == -1:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'matching failed', appname)
                continue
            wait(10)
            # ゲームループ
            GameLib.gameLoop(resources, strategy)
            # ゲームループエンド
            total_duel_count+=1
            breakBattleLoopFlag = False
            winFlag = False
            for battleResultLoop in range(200):
                print "battleResultLoop..." + str(battleResultLoop)
                
                CommonDMLib.skipRewards(resources)
                if len(findAny(resources.ICON_TARGET_REWARD)) > 0:
                    targetRewardFlag = True
                if (len(findAny(resources.ICON_NEXT_REWARD_OF_TARGET)) > 0 and targetRewardFlag == True) or len(findAny(resources.ICON_REWARD_COMPLETED)) > 0:
                    CommonDMLib.sendMessagetoSlack(mentionUser, 'A target reward was acquired.', appname)
                    CommonDMLib.completeQuestStatus(instances[instanceIndex], "LEGEND")
                    instanceIndex += 1
                    exitFlag = True
                    break
                if len(findAny(resources.ICON_WIN)) > 0:
                    winFlag = True
                    if level < LOOP_LEVEL:
                        click(resources.BUTTON_SMALL_OK)
                        breakBattleLoopFlag = True
                    else:
                        click(resources.BUTTON_SMALL_BATTLE_START)
                if len(findAny(resources.ICON_LOSE)) > 0:
                    click(resources.BUTTON_SMALL_BATTLE_START)
                if len(findAny(resources.BUTTON_SMALL_BATTLE_START)) == 0:
                    break
            if winFlag == True:
                win_count+=1
            if breakBattleLoopFlag == True or exitFlag == True:
                win_count = 0
                break
        #バトルループエンド
        if exitFlag == True:
            break
    except:
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured. The app was restarted successfully .', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.uploadScreenShotToSlack(mentionUser, "screenshot" ,appname)
     
