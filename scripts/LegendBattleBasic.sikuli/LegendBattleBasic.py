import sys
import traceback

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
appname = 'LegendBattle'
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
DMApp = App(AppPath)
total_duel_count = 0
win_count =0
restart_count = 0

#Pre-processing Start
NoxDMLib.exitNox()
CommonDMLib.downloadDeckCodes()
#Pre-processing End

CommonDMLib.RestartApp(AndAppResources, DMApp)
click("1595253546948.png")
wait(3)
click(Pattern("1595993039410.png").similar(0.90))

#全体ループ
targetRewardFlag = False
exitFlag = False
entire_loop_flag = True
level = 0
strategy = 100
for entire_loop in range(100):
    try:
        for battleStartLoop in range(200):
            print "battleStartLoop..." + str(battleStartLoop)
            if len(findAny(AndAppResources.BUTTON_BACK2)) > 0:
                for skipTutorialLoop in range(10):
                    click(AndAppResources.BUTTON_BACK2)
                    wait(0.2)
    #        if exists("1600700995819.png", 2) != None:
    #            level = 3
    #            click("1600700995819.png")
            if len(findAny("1600700956975.png")) > 0:
                level = 2
                strategy = 2
                try:
                    click("1600700956975.png")
                except:
                    print "failed to click"
            elif len(findAny("1600697998210.png")) > 0:
                level = 1
                strategy = 2
                try:
                    click("1600697998210.png")
                except:
                    print "failed to click"

            if len(findAny(AndAppResources.BUTTON_SMALL_BATTLE_START)) > 0:
                try:
                    click(AndAppResources.BUTTON_SMALL_BATTLE_START)
                except:
                    print "failed to click"
            if len(findAny(AndAppResources.BUTTON_LARGE_BATTLE_START)) > 0:
                break
            CommonDMLib.skipRewards(AndAppResources)
            CommonDMLib.skipStory(AndAppResources)
            #バトルスタートループエンド
            
        deck = CommonDMLib.getDeckByStrategy(AndAppResources, strategy)
        if CommonDMLib.chooseDeck(AndAppResources, deck[0]) == False:
            CommonDMLib.addNewDeckByCode(AndAppResources, deck[1])
        click(AndAppResources.BUTTON_LARGE_BATTLE_START)
        #バトルループ
        for battle_loop in range(200):
            CommonDMLib.sendMessagetoSlack(mentionUser, 'win/total = ' + str(win_count) + "/" + str(battle_loop), appname)
            #バトル開始まで待機
            if CommonDMLib.waitStartingGame(AndAppResources) == -1:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'matching failed', appname)
                continue
            wait(10)
            # ゲームループ
            game_loop_flag = True
            for game_loop in range(10):
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
                #  攻撃
                DMLib.directAttack(DMApp, "1598593219619.png")
                #  ターンエンド
                if len(findAny(Pattern("1594954855862-1.png").similar(0.84))) > 0:          
                    keyDown(Key.SHIFT)
                    type(Key.ENTER)
                    keyUp(Key.SHIFT)
                wait(1)
                    
                #  イレギュラーループ
                if DMLib.irregularLoop() == 0:
                    break
            # ゲームループエンド
            total_duel_count+=1
            breakBattleLoopFlag = False
            winFlag = False
            for battleResultLoop in range(200):
                print "battleResultLoop..." + str(battleResultLoop)
                
                CommonDMLib.skipRewards(AndAppResources)
                if len(findAny("1600702754259.png")) > 0:
                    targetRewardFlag = True
                    #CommonDMLib.sendMessagetoSlack(mentionUser, 'Target SR is detected. The legend battle will be finished in a few games.', appname)
                if len(findAny("1600777270163.png")) > 0 and targetRewardFlag == True:
                    CommonDMLib.sendMessagetoSlack(mentionUser, 'A target reward was acquired.', appname)
                    exitFlag = True
                    break
                if len(findAny("1595034514931.png")) > 0:
                    winFlag = True
                    if level == 1:
                        click(AndAppResources.BUTTON_SMALL_OK)
                        breakBattleLoopFlag = True
                    else:
                        click(AndAppResources.BUTTON_SMALL_BATTLE_START)
                if len(findAny("1600770753632.png")) > 0:
                    click(AndAppResources.BUTTON_SMALL_BATTLE_START)
                if len(findAny(AndAppResources.BUTTON_SMALL_BATTLE_START)) == 0:
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
        restart_count+=1
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured. The app was restarted successfully .', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.uploadScreenShotToSlack(mentionUser, "screenshot" ,appname)
        CommonDMLib.RestartApp(AndAppResources,DMApp)
        click("1595253546948.png")
        wait(3)
        click(Pattern("1595977354621.png").targetOffset(-23,-92))
     
