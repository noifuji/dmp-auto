import sys
import traceback
sys.path.append("DMLib.sikuli")
sys.path.append("EnvSettings.sikuli")
import DMLib
import EnvSettings

####################Settings####################
Avator = Pattern("Avator-1.png").similar(0.90).targetOffset(315,1)
DECK = "DECK.png"
####################Settings####################
slack_url = EnvSettings.slack_url
mentionUser = EnvSettings.mentionUser
AppPath = EnvSettings.AppPath
appname = 'LegendBattle'
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
DMApp = App(AppPath)
total_duel_count = 0
win_count =0
restart_count = 0


DMLib.RestartApp(DMApp)
click("1595253546948-1.png")
wait(3)
click(Pattern("1595993039410-1.png").similar(0.90))

#全体ループ
entire_loop_flag = True
level = 0
for entire_loop in range(100):
    try:
        if exists(Pattern("1596674596997-1.png").targetOffset(-234,-4),20) != None:
            click("1598593147785.png")
            wait(5)
            click("1598593147785.png")
            wait(5)
            click("1598593147785.png")
            wait(5)
            
        #if exists(Pattern("1598598402763.png").similar(0.95), 60) != None:
         #   level = 4
          #  click(Pattern("1598598402763.png").similar(0.95))
        if exists(Pattern("1598593795566.png").similar(0.95), 60) != None:
            level = 3
            click(Pattern("1598593795566.png").similar(0.95))
        
        elif exists(Pattern("1598593413852.png").similar(0.95), 60) != None:
            level = 2
            click(Pattern("1598593413852.png").similar(0.95))
        elif exists(Pattern("1598593117745.png").similar(0.95), 60) != None:
            level = 1
            click(Pattern("1598593117745.png").similar(0.95))
        click("1595977375290-2.png")
        wait("1595977394372-2.png",60)
        click(DECK)
        click("1595977394372-2.png")
    #バトルループ
        for battle_loop in range(200):
            CommonDMLib.sendMessagetoSlack(mentionUser, 'win/total = ' + str(win_count) + "/" + str(battle_loop), appname)
            #バトル開始まで待機
            if DMLib.waitStartingGame(AndAppResources) == -1:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'matching failed', appname)
                continue
            wait(10)
            # ゲームループ
            game_loop_flag = True
            for game_loop in range(10):
                print "Inside Game Loop"
                click(Pattern("1594957113274.png").targetOffset(11,1))
                wait(0.5)
                #  手札選択
                if len(findAny(Avator)) > 0:
                    click(Avator)
                    wait(1)
                #  マナチャージ
                currentMana = DMLib.ChargeManaKuwakiri(DMApp)
                #  召喚
                DMLib.SummonKuwakiri(currentMana)
                #  攻撃
                DMLib.directAttack(DMApp, "1598593219619.png")
                #  ターンエンド
                if len(findAny(Pattern("1594954855862-2.png").similar(0.84))) > 0:          
                    keyDown(Key.SHIFT)
                    type(Key.ENTER)
                    keyUp(Key.SHIFT)
                wait(1)
                    
                #  イレギュラーループ
                if DMLib.irregularLoop() == 0:
                    break
            # ゲームループエンド
            DMLib.skipRewards()
            total_duel_count+=1
            if len(findAny(Pattern("1596686772330-1.png").similar(0.90))) > 0:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'Galzark is detected. The legend battle will be finished in a few games.', appname)
            if len(findAny("1595034514931-1.png")) > 0:
                win_count+=1

                if level == 1 or level == 2:
                    click("1595066895612-1.png")
                    wait(20)
                    #ストーリースキップ
                    CommonDMLib.skipStory(AndAppResources)
                    wait(15)
                    #報酬のスキップ
                    DMLib.skipRewards()
                    wait(10)
                    break
                    
            # 対戦開始をクリック
            click(Pattern("1594949925094-1.png").similar(0.81))
        #バトルループエンド
    except:
        e = sys.exc_info()
        for mes in e:
            print(mes)
        restart_count+=1
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured. The app was restarted successfully .', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.uploadScreenShotToSlack(mentionUser, "screenshot" ,appname)
        DMLib.RestartApp(DMApp)
        click("1595253546948-1.png")
        wait(3)
        click(Pattern("1595977354621-1.png").targetOffset(-23,-92))
     
