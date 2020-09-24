import sys
import traceback
sys.path.append("DMLib.sikuli")
sys.path.append("CommonDMLib.sikuli")
sys.path.append("EnvSettings.sikuli")
import DMLib
import CommonDMLib
import EnvSettings

####################Settings####################
Avator = Pattern("Avator.png").similar(0.90).targetOffset(315,1)
#[Pattern("1597424555384.png").similar(0.95),"White1"],[Pattern("1597424593649.png").similar(0.95),"White2"],[Pattern("1597424607478.png").similar(0.95),"White3"]
#        ,[Pattern("1597424731368.png").similar(0.93),"Blue1"],[Pattern("1597424744007.png").similar(0.95),"Blue2"],[Pattern("1597424751985.png").similar(0.95),"Blue3"]
#[Pattern("1597424787191.png").similar(0.95),"Black3"]
#        ,[Pattern("1597424814414.png").similar(0.95),"Red1"],[Pattern("1597424822070.png").similar(0.95),"Red2"],[Pattern("1597424829789.png").similar(0.95),"Red3"]
#        ,[Pattern("1597424861488.png").similar(0.95),"Green1"],
#[Pattern("1597424869238.png").similar(0.95),"Green2"],[Pattern("1597424877984.png").similar(0.95),"Green3"]
#        ,[Pattern("1597063981103.png").similar(0.90),"Ushi3"]
#        ,[Pattern("1597064015074.png").similar(0.94),"Bucket1"],
targets = [[Pattern("1597064033286.png").similar(0.93),"Bucket2"],[Pattern("1597064046126.png").similar(0.94),"Bucket3"]]
####################Settings####################
slack_url = EnvSettings.slack_url
mentionUser = EnvSettings.mentionUser
AppPath = EnvSettings.AppPath
appname = 'CityBattle'
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
DMApp = App(AppPath)
total_duel_count = 0
win_count =0
restart_count = 0

#全体ループ
entire_loop_flag = True
for target in targets:
    DMLib.RestartApp(DMApp)
    DMLib.OpenAndStartCityBattle(target[0])
    #バトルループ
    for battle_loop in range(200):
        try:
            #バトル開始まで待機
            if DMLib.waitStartingGame(AndAppResources) == -1:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'matching failed', appname)
                continue
            wait(10)
            # ゲームループ
            game_loop_flag = True
            for game_loop in range(10):
                print "Inside Game Loop"
                #  手札選択
                if len(findAny(Avator)) > 0:
                    click(Avator)
                    wait(1)
                #  マナチャージ
                currentMana = DMLib.ChargeManaKuwakiri(DMApp)
                #  召喚
                DMLib.SummonKuwakiri(currentMana)
                #  攻撃
                DMLib.directAttack(DMApp,Pattern("1594948414271.png").similar(0.60))
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
            # 報酬を確認(WINで報酬なしなら終了)
            DMLib.skipRewards()
            total_duel_count+=1
            if len(findAny("1595034514931.png")) > 0:
                win_count+=1
                wait(1)
                #報酬をしぼりつくした場合、つぎのターゲットへ移行する。
                if len(findAny(Pattern("1595129681765.png").similar(0.97))) > 0:
                    print ''
                    CommonDMLib.sendMessagetoSlack(mentionUser, str(target[1]) + ' rewards were completed.', appname)
                    break
                    
            # 対戦開始をクリック
            click("1594949925094.png")
        except:
            e = sys.exc_info()
            for mes in e:
                print(mes)
            CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured. The app was restarted successfully .', appname)
            CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
            CommonDMLib.uploadScreenShotToSlack(mentionUser, "screenshot" ,appname)
            restart_count+=1
            DMLib.RestartApp(DMApp)
            DMLib.OpenAndStartCityBattle(target[0])
    #バトルループエンド

     
