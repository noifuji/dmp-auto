import sys
import traceback
sys.path.append("DMLib.sikuli")
sys.path.append("CommonDMLib.sikuli")
sys.path.append("AndAppResources.sikuli")
sys.path.append("EnvSettings.sikuli")
import DMLib
import CommonDMLib
import AndAppResources
import EnvSettings

mentionUser = EnvSettings.mentionUser
AppPath = EnvSettings.AppPath
appname = 'SPBattle'
DMApp = App(AppPath)
total_duel_count = 0
win_count =0
restart_count = 0
Settings.MoveMouseDelay = 0.1

CommonDMLib.RestartApp(AndAppResources)
DMLib.openAndStartSPBattle(AndAppResources, EnvSettings.DECKCODE_SPBATTLE)

entireLoopFlag = True
for entire_loop in range(1000):
    try:
        #マッチングを待つ
        if CommonDMLib.waitStartingGame(AndAppResources) == -1:
            if EnvSettings.RUN_MODE == "DEV":
                CommonDMLib.sendMessagetoSlack(mentionUser, 'matching failed', appname)
            continue

        turn_count = 0
        for game_loop in range(1000):

            if len(findAny("1595317856423.png")) > 0:
                print 'click turnend'
                for turnendLoop in range(180):
                    keyDown(Key.SHIFT)
                    type(Key.ENTER)
                    keyUp(Key.SHIFT)
                    if len(findAny("1599193822994.png","1595254158740.png")) > 0:
                        break
                
                turn_count += 1
                if turn_count >= 3 :
                    print 'retire'
                    DMLib.retire()
            
            if DMLib.irregularLoopForSP() == 0:
                total_duel_count+=1
                if EnvSettings.RUN_MODE == "DEV":
                    if total_duel_count % 5 == 0:
                        CommonDMLib.sendMessagetoSlack(mentionUser,'SP Battle Count : ' + str(total_duel_count), appname)
                break

        #報酬獲得
        for battleResultLoop in range(180):
            if len(findAny("1599211042677.png")) > 0:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'SR Ticket was acquired.', appname)
                #entireLoopFlag = False
                #break
            if len(findAny("1595254158740.png")) > 0:
                click("1595254158740.png")
            else:
                break
            CommonDMLib.skipRewards(AndAppResources)
            
        if entireLoopFlag == False:
            break
    except:
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured. The app was restarted successfully .', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.uploadScreenShotToSlack(mentionUser, "screenshot" ,appname)
        restart_count+=1
        CommonDMLib.RestartApp(AndAppResources)
        DMLib.openAndStartSPBattle(AndAppResources, EnvSettings.DECKCODE_SPBATTLE)