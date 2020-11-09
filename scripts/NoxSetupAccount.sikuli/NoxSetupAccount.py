import sys
import urllib2
import json
import traceback
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import NoxDMLib
import CommonDMLib
import NoxResources

####################Settings####################
appname = 'NoxSetupAccount'
mentionUser = EnvSettings.mentionUser
Settings.MoveMouseDelay = 0.1
NoxApp = App(EnvSettings.NoxAppPath)
####################Settings####################

#resources
OK = Pattern("OK.png").similar(0.90)
OK2 = Pattern("OK2.png").similar(0.80)
tutorial = "tutorial.png"


CommonDMLib.downloadDeckCodes()

for count in range(100):
    try:
        ref = "setup"
        username = ref
        CommonDMLib.RestartNox(NoxResources,ref)
        CommonDMLib.callRemoveDataBat()
    except:
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack(mentionUser,'Failed to launch instance. Setup was canceled.', appname)
        break
        
    for num in range(100):
        try:
            CommonDMLib.noxCallKillDMPApp()
            wait(3)
            CommonDMLib.noxCallStartDMPApp()
            breakFlag = False
            loop_without_action_count = 0
            action_flag = False
            while loop_without_action_count <= 120:
                if len(findAny(NoxResources.BUTTON_AGREE)) > 0:
                    print 'An agreement button is detected.'
                    click(NoxResources.BUTTON_AGREE)
                    wait(1)
                    action_flag = True
                    loop_without_action_count = 0
                if len(findAny(NoxResources.BUTTON_TAKEOVER)) > 0:
                    print 'A data button is detected.'
                    click(NoxResources.BUTTON_TAKEOVER)
                    break
                    
                if action_flag == False:
                    loop_without_action_count += 1
                    print 'loop without action : ' + str(loop_without_action_count)
                
                if loop_without_action_count >= 119:
                    CommonDMLib.sendMessagetoSlack(mentionUser,'Too many loops without actions. This app will be restarted.', appname)
                    breakFlag = True
                    loop_without_action_count = 0

                wait(1)
    
                action_flag = False
                
            if breakFlag == True:
                continue
    
            breakFlag = False
            loop_without_action_count = 0
            action_flag = False
            while loop_without_action_count <= 120:
                if len(findAny(NoxResources.BUTTON_SKIP)) > 0:
                    print 'A skip button is detected.'
                    try:
                        click(NoxResources.BUTTON_SKIP)
                    except:
                        print "failed to click skip"
                    action_flag = True
                    loop_without_action_count = 0
                if len( findAny("1596591807133-1.png")) > 0:
                    print 'A player name text box is detected.'
                    try:
                        click(Pattern("1596591807133-1.png").targetOffset(351,196))
                    except:
                        print "failed to click name"
                    wait(0.5)
                    type(str(username))
                    try:
                        click(Pattern("1596591807133-1.png").targetOffset(-44,101))
                        click(OK)
                    except:
                        print "failed to click name"
                    wait(0.5)
                    action_flag = True 
                    
                if len(findAny(OK)) > 0:
                    if len( findAny("1596591807133-1.png")) > 0:
                        continue
                    print 'A OK button1 is detected.'
                    try:
                        click(OK)
                    except:
                        print "failed to click OK"
                    action_flag = True
                    loop_without_action_count = 0
    
                if len(findAny(tutorial)) > 0:
                    print 'A Training button is detected.'
                    try:
                        click(tutorial)
                    except:
                        print "failed to click tutorial"
                    action_flag = True
                    loop_without_action_count = 0
                    
                if len(findAny(OK2)) > 0:
                    if len( findAny("1596591807133-1.png")) > 0:
                        continue
                    print 'A OK button2 is detected.'
                    try:
                        click(OK2)
                    except:
                        print "failed to click OK2"
                    action_flag = True
                    loop_without_action_count = 0
    
                if len(findAny(NoxResources.BUTTON_RETRY)) > 0:
                    click(NoxResources.BUTTON_RETRY)
                    
                if len(findAny(NoxResources.ICON_HOME)) > 0:
                    print 'Home view was detected. This download loop will be broken.'
                    break
    
                if action_flag == False:
                    loop_without_action_count += 1
                    print 'loop without action : ' + str(loop_without_action_count)
                
                if loop_without_action_count >= 119:
                    CommonDMLib.sendMessagetoSlack(mentionUser,'Too many loops without actions. This app will be restarted.', appname)
                    breakFlag = True
                    loop_without_action_count = 0
                    break
    
                action_flag = False
                
            if breakFlag == True:
                continue
    
            for skipLoop in range(120):
                if CommonDMLib.skipNotifications(NoxResources) == -1:
                    exists(resource.BUTTON_SMALL_OK, 60)
                    for backLoop in range(60):
                        print "backLoop"
                        if len(findAny(NoxResources.BUTTON_SMALL_OK)) > 0:
                            try:
                                click(NoxResources.BUTTON_SMALL_OK)
                            except:
                                print "failed to click"
                        if len(findAny(NoxResources.BUTTON_BACK)) > 0:
                            try:
                                click(NoxResources.BUTTON_BACK)
                            except:
                                print "failed to click"
                        if len(findAny(NoxResources.ICON_HOME)) > 0:
                            break
                
                type(Key.ESC)
                if len(findAny(NoxResources.ICON_MISSION)) > 0:
                    try:
                        click(NoxResources.ICON_MISSION)
                    except:
                        print "failed to click"
                    if exists(NoxResources.TITLE_MISSION,1) != None:
                        type(Key.ESC)
                        break
                    
            wait(5)
            CommonDMLib.getPresent(NoxResources)
            
            for openCardListLoop in range(100):
                if len(findAny(NoxResources.ICON_CARD)) > 0:
                    try:
                        click(NoxResources.ICON_CARD)
                    except:
                        print "failed to click"
                    wait(1)
                if len(findAny("1596780592222.png")) > 0:
                    try:
                        click("1596780592222.png")
                    except:
                        print "failed to click"
                    wait(1)
                if len(findAny("1596780703269.png")) > 0:
                    break
                        
            for deleteDeck in range(5):
                if exists("1597553140601.png", 1) != None:
                    break
                click("1596780671063.png")
                wait(2)
                click("1596780684705.png")
                wait(1)
            exists("1596780703269.png",60)
            
            CommonDMLib.addNewDeckByCode(NoxResources, CommonDMLib.getDeckCode("DECKCODE_STSPELL"))
            CommonDMLib.addNewDeckByCode(NoxResources, CommonDMLib.getDeckCode("DECKCODE_RED_BLACK"))
            CommonDMLib.addNewDeckByCode(NoxResources, CommonDMLib.getDeckCode("DECKCODE_ST"))
            CommonDMLib.addNewDeckByCode(NoxResources, CommonDMLib.getDeckCode("DECKCODE_LARGE_CREATURE"))
            CommonDMLib.addNewDeckByCode(NoxResources, CommonDMLib.getDeckCode("DECKCODE_MAIN"))
            click("1597235437582.png")
            exists(NoxResources.ICON_SOLO_PLAY,60)
            click(NoxResources.ICON_OTHER)
            wait(3)
            click("1596781081109.png")
            exists("1596781095779.png", 30)
            wheel(Pattern("1596781095779.png").targetOffset(19,145), Button.WHEEL_DOWN, 100)
            wait(5)
            click(Pattern("1596781218965.png").targetOffset(503,-3))
            click(Pattern("1596781239281.png").targetOffset(499,-1))
            click(Pattern("1596781253234.png").targetOffset(511,1))
            click(Pattern("1596781269013.png").targetOffset(500,8))
            click(Pattern("1596781287439.png").similar(0.60).targetOffset(506,0))
            click("1596781316064.png")
            exists("1597235336512.png",10)
            click("1597235336512.png")
            exists("1597235361421.png",30)
            click(Pattern("1600004482153.png").targetOffset(9,-27))
            exists("1600004545866.png", 60)
            click("1600004566684.png")
            click(Pattern("1600004640701.png").targetOffset(-263,282))
            click("1600004681385.png")
            exists("1600004729257.png",10)
            click(Pattern("1600004729257.png").targetOffset(6,330))
            exists("1600004802890.png", 120)
            ref = CommonDMLib.getSetupAccountRef()
            if ref == "":
                CommonDMLib.sendMessagetoSlack(mentionUser,"No empty Ref numbers. Add Refs to the inventory list.", appname)
                breakFlag = True
                break
            playerId = CommonDMLib.scanNumberChangeWidth("1601082545206.png", -270, 0, 233, 38, 0, 25)
            #プレーヤー名をrefに変更する。
            click(Pattern("1603534330138.png").targetOffset(106,81))
            for bkLoop in range(10):
                type(Key.BACKSPACE)
                wait(0.2)
            type(str(ref))
            wait(0.5)
            click("1603541423678.png")
            wait(1)
            CommonDMLib.uploadScreenShotToSlack(mentionUser, str(ref), appname)
            CommonDMLib.updatePlayerId(ref, playerId, os.environ["COMPUTERNAME"])
            CommonDMLib.renameRunningNoxInstance(NoxResources, str(ref))
            CommonDMLib.sendMessagetoSlack(mentionUser,'Setup has finished.', appname)
            break
        except:
            e = sys.exc_info()
            for mes in e:
                print(mes)
            CommonDMLib.updatePlayerId(ref, "", "")
            CommonDMLib.sendMessagetoSlack(mentionUser,'Error occured. Restarting..', appname)
            CommonDMLib.sendMessagetoSlack( mentionUser,traceback.format_exc(), appname)
            wait(5)