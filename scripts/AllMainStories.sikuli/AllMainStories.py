import sys
import traceback
from datetime import datetime

sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import DMLib
import NoxDMLib
import CommonDMLib
import AndAppResources

####################Settings####################
Avator = Pattern("Avator.png").similar(0.90).targetOffset(315,1)
####################Settings####################

mentionUser = EnvSettings.mentionUser
AppPath = EnvSettings.AppPath
appname = 'AllMainStories'
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
DMApp = App(AppPath)
win_count =0
retryCount = 0

#Pre-processing Start
NoxDMLib.exitNox()
CommonDMLib.updateDeckCodes()
#Pre-processing End

CommonDMLib.RestartApp(AndAppResources, DMApp)
CommonDMLib.openMainStory(AndAppResources)
strategy = CommonDMLib.getStrategyByMainStoryStage(AndAppResources)
deck = CommonDMLib.getDeckByStrategy(AndAppResources, strategy)
CommonDMLib.startMainStoryBattle(AndAppResources, deck[0], deck[1])

#全体ループ
entire_loop_flag = True
for entire_loop in range(100):
    try:
        #バトルループ
        for battle_loop in range(2000):
            #バトル開始まで待機
            if CommonDMLib.waitStartingGame(AndAppResources) == -1:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'matching failed', appname)
                break

            wait(10)
            # ゲームループ
            for game_loop in range(50):
                print "Inside Game Loop"
                if len(findAny(Pattern("1594957113274.png").targetOffset(11,1))) > 0:
                    click(Pattern("1594957113274.png").targetOffset(11,1))
                    wait(1)
                #  手札選択
                if len(findAny(Avator)) > 0:
                    click(Avator)
                    wait(1)
                #  マナチャージ
                if strategy == 100:
                    currentMana = DMLib.ChargeManaBasic(DMApp)
                elif strategy == 2:
                    currentMana = DMLib.ChargeManaRedBlack()
                wait(1)
                #  召喚
                if strategy == 100:
                    DMLib.SummonBasic(currentMana)
                elif strategy == 2:
                    DMLib.SummonRedBlack(currentMana)
                wait(1)
                #  攻撃
                DMLib.directAttack(DMApp, Pattern("1594948414271.png").similar(0.60))
                wait(1)
                #  ターンエンド
                if len(findAny(Pattern("1594954855862.png").similar(0.84))) > 0:          
                    keyDown(Key.SHIFT)
                    type(Key.ENTER)
                    keyUp(Key.SHIFT)
                wait(1)
                #  イレギュラーループ
                if DMLib.irregularLoop() == 0:
                    break

            # ゲームループエンド
            winFlag = False
            for battleResultLoop in range(180):
                CommonDMLib.skipRewards(AndAppResources)
                if len(findAny("1595034514931.png")) > 0:
                    click("1599599373285.png")
                    winFlag = True
                if len(findAny("1599561314584.png")) > 0:
                    click("1594949925094.png")
                    winFlag = False
                if len(findAny("1594949925094.png")) == 0:
                    break
            if winFlag == False:
                retryCount += 1
                continue

            for checkRewardLoop in range(180):
                CommonDMLib.skipStory(AndAppResources)
                #レベルアップ報酬のスキップ
                CommonDMLib.skipRewards(AndAppResources)

                #エピソード選択画面にいる場合の処理
                if len(findAny("1600267657384.png")) > 0:
                    wait(10)
                    if len(findAny(Pattern("1598197418579.png").similar(0.87).targetOffset(-51,-214))) > 0:
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'Episode4 has started.', appname)
                        click(Pattern("1598197418579.png").similar(0.86).targetOffset(-51,-214))
                    elif len(findAny(Pattern("1595243394444.png").similar(0.94))) > 0:
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'Episode3 has started.', appname)
                        click(Pattern("1595243394444.png").similar(0.94).targetOffset(3,-65))
                    elif len(findAny(Pattern("1595243419652.png").similar(0.95))) > 0:
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'Episode2 has started.', appname)
                        click(Pattern("1595243419652.png").similar(0.95).targetOffset(1,-57))
                if len(findAny("1599610866634.png")) > 0:
                    click("1599610866634.png")
                    wait(0.5)
                if len(findAny("1599610908602.png")) > 0:
                    click("1599610920793.png")
                    break
                
            if EnvSettings.RUN_MODE == "DEV":
                wait(1)
                CommonDMLib.uploadScreenShotToSlack(mentionUser, 'Battle Loop Count : ' + str(retryCount), appname)
                retryCount = 0
            if len(findAny(Pattern("1596547428588.png").similar(0.90))) > 0 or len(findAny(Pattern("1596579505109.png").similar(0.90))) > 0:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'All stories are cleared!', appname)
                entire_loop_flag = False
                break
                
            strategy = CommonDMLib.getStrategyByMainStoryStage(AndAppResources)
            deck = CommonDMLib.getDeckByStrategy(AndAppResources, strategy)
            CommonDMLib.startMainStoryBattle(AndAppResources, deck[0], deck[1])
   
        #バトルループエンド
        if entire_loop_flag == False:
            break
    except:
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured. The app was restarted successfully .', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.uploadScreenShotToSlack(mentionUser, "Screenshot" , appname)
        CommonDMLib.RestartApp(AndAppResources, DMApp)
        CommonDMLib.openMainStory(AndAppResources)
        strategy = CommonDMLib.getStrategyByMainStoryStage(AndAppResources)
        deck = CommonDMLib.getDeckByStrategy(AndAppResources, strategy)
        CommonDMLib.startMainStoryBattle(AndAppResources, deck[0], deck[1])