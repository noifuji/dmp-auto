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

Avator = AndAppResources.AVATOR_DEFAULT_MALE
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
                if len(findAny(AndAppResources.ICON_ENEMY_CARD_COUNT)) > 0:
                    click(AndAppResources.ICON_ENEMY_CARD_COUNT)
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
                DMLib.directAttack(DMApp, AndAppResources.DESIGN_CARD_BACKSIDE_NORMAL)
                wait(1)
                #  ターンエンド
                if len(findAny(AndAppResources.BUTTON_TURN_END)) > 0:          
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
                if len(findAny(AndAppResources.ICON_WIN)) > 0:
                    click(AndAppResources.BUTTON_SMALL_OK)
                    winFlag = True
                if len(findAny(AndAppResources.ICON_LOSE)) > 0:
                    click(AndAppResources.BUTTON_SMALL_BATTLE_START)
                    winFlag = False
                if len(findAny(AndAppResources.BUTTON_SMALL_BATTLE_START)) == 0:
                    break
            if winFlag == False:
                retryCount += 1
                continue

            for checkRewardLoop in range(180):
                CommonDMLib.skipStory(AndAppResources)
                #レベルアップ報酬のスキップ
                CommonDMLib.skipRewards(AndAppResources)

                #エピソード選択画面にいる場合の処理
                if len(findAny(AndAppResources.BACKGROUND_EPISODE_LIST)) > 0:
                    wait(10)
                    if len(findAny(AndAppResources.TITLE_EP5)) > 0:
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'Episode5 has started.', appname)
                        click(AndAppResources.TITLE_EP5)
                    elif len(findAny(AndAppResources.TITLE_EP4)) > 0:#Pattern("1598197418579.png").similar(0.86).targetOffset(-51,-214)
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'Episode4 has started.', appname)
                        click(AndAppResources.TITLE_EP4)#Pattern("1598197418579.png").similar(0.86).targetOffset(-51,-214)
                    elif len(findAny(AndAppResources.TITLE_EP3)) > 0:#Pattern("1595243394444.png").similar(0.94)
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'Episode3 has started.', appname)
                        click(AndAppResources.TITLE_EP3)#Pattern("1595243394444.png").similar(0.94).targetOffset(3,-65)
                    elif len(findAny(AndAppResources.TITLE_EP2)) > 0:#Pattern("1595243419652.png").similar(0.95)
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'Episode2 has started.', appname)
                        click(AndAppResources.TITLE_EP2)#Pattern("1595243419652.png").similar(0.95).targetOffset(1,-57)
                if len(findAny(AndAppResources.BUTTON_CONFIRM_REWARD)) > 0:
                    click(AndAppResources.BUTTON_CONFIRM_REWARD)
                    wait(0.5)
                if len(findAny(AndAppResources.TITLE_REWARD_INFO)) > 0:
                    click(AndAppResources.BUTTON_CLOSE)
                    break
                
            if EnvSettings.RUN_MODE == "DEV":
                wait(1)
                CommonDMLib.uploadScreenShotToSlack(mentionUser, 'Battle Loop Count : ' + str(retryCount), appname)
                retryCount = 0
            if len(findAny(AndAppResources.TITLE_EP5_STAGE10)) > 0:
                if len(findAny(AndAppResources.BUTTON_CHECK_REWARD)) > 0:
                    click(AndAppResources.BUTTON_CHECK_REWARD)
                    exists(AndAppResources.TITLE_REWARD_INFO,60)
                    if len(findAny(AndAppResources.ICON_CLEARED)) > 0:
                        CommonDMLib.sendMessagetoSlack(mentionUser, 'All stories are cleared!', appname)
                        entire_loop_flag = False
                        break
                    click(AndAppResources.BUTTON_CLOSE)
                
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