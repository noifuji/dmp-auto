import sys
import traceback
sys.path.append("DMLib.sikuli")
sys.path.append("EnvSettings.sikuli")
import DMLib
import EnvSettings

####################Settings####################
Avator = Pattern("Avator.png").similar(0.90).targetOffset(315,1)
DECK = "DECK.png"
retryCount = 0 #勝利した場合でも、コンプリートでなければ指定の回数リトライする。
####################Settings####################

slack_url = EnvSettings.slack_url
mentionUser = EnvSettings.mentionUser
AppPath = EnvSettings.AppPath
appname = 'MainStory'
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
DMApp = App(AppPath)
win_count =0
total_count = 0

#全体ループ
entire_loop_flag = True
for entire_loop in range(100):
    try:
        #バトルループ
        for battle_loop in range(2000):
            CommonDMLib.sendMessagetoSlack(mentionUser, 'win/total = ' + str(win_count) + "/" + str(total_count), appname)
            #バトル開始まで待機
            if DMLib.waitStartingGame(AndAppResources) == -1:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'matching failed', appname)
                break

            wait(10)
            # ゲームループ
            for game_loop in range(50):
                print "Inside Game Loop"
                click(Pattern("1594957113274.png").targetOffset(11,1))
                wait(0.5)
                #  手札選択
                if len(findAny(Avator)) > 0:
                    click(Avator)
                    wait(1)
                #  マナチャージ
                currentMana = DMLib.ChargeManaF30(DMApp)
                wait(1)
                #  召喚
                DMLib.SummonF30(currentMana)
                wait(1)
                #  攻撃
                DMLib.directAttackAvoidingBlocker(DMApp, Pattern("1594948414271.png").similar(0.60))
                wait(3)
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
            wait(5)
            #レベルアップ報酬のスキップ
            DMLib.skipRewards()
            # 報酬を確認(WINで報酬なしなら終了)
            total_count += 1
            if len(findAny("1595034514931.png")) > 0:
                win_count+=1
   
            # 対戦開始をクリック
            click("1594949925094.png")
            wait(30)
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
        DMLib.RestartApp(DMApp)
        DMLib.openAndStartMainStory(AndAppResources, DECK)