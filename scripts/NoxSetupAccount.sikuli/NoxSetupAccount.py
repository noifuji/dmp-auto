import sys
import urllib2
import json
import traceback
sys.path.append("EnvSettings.sikuli")
sys.path.append("NoxDMLib.sikuli")
sys.path.append("CommonDMLib.sikuli")
sys.path.append("NoxResources.sikuli")
import EnvSettings
import NoxDMLib
import CommonDMLib
import NoxResources

####################Settings####################
appname = 'NoxSetupAccount'
mentionUser = EnvSettings.mentionUser
deckCodes = ["336AEW","32XP47","336AHX","336ALY","336APZ"]
Settings.MoveMouseDelay = 0.1
NoxAppPath = EnvSettings.NoxAppPath
NoxApp = App(NoxAppPath)
####################Settings####################

#resources
OK = Pattern("OK.png").similar(0.90)
OK2 = Pattern("OK2.png").similar(0.80)
tutorial = "tutorial.png"

instances = [
#        [Pattern("1600150756252.png").similar(0.95).targetOffset(423,-2),1076],
#        [Pattern("1600150869090.png").similar(0.94).targetOffset(427,-1),1077],
#        [Pattern("1600150896461.png").similar(0.95).targetOffset(430,1),1078],
#        [Pattern("1600150917467.png").similar(0.95).targetOffset(421,-3),1079],
#        [Pattern("1600150940949.png").similar(0.95).targetOffset(421,0),1080],
#        [Pattern("1600150961485.png").similar(0.95).targetOffset(421,-1),1081],
#        [Pattern("1600150982535.png").similar(0.95).targetOffset(420,-4),1082],
#        [Pattern("1600151004590.png").similar(0.95).targetOffset(422,-2),1083],
#        [Pattern("1600151023104.png").similar(0.95).targetOffset(424,1),1084],
        [Pattern("1600151052221.png").similar(0.95).targetOffset(421,1),1085],
        [Pattern("1600151060273.png").similar(0.95).targetOffset(422,2),1086],
        [Pattern("1600151069275.png").similar(0.95).targetOffset(420,1),1087]
        ]

instanceIndex = 0
retryCount = 0
while instanceIndex < len(instances):
    username = instances[instanceIndex][1]
    NoxDMLib.RestartNox(NoxApp, instances[instanceIndex])
    CommonDMLib.callRemoveDataBat()
        
    for num in range(100):
        try:
            CommonDMLib.noxCallKillDMPApp()
            wait(3)
            CommonDMLib.noxCallStartDMPApp()
            breakFlag = False
            loop_without_action_count = 0
            action_flag = False
            while loop_without_action_count <= 120:
                if len(findAny("1596591221362.png")) > 0:
                    print 'An agreement button is detected.'
                    click("1596591221362.png")
                    wait(1)
                    action_flag = True
                    loop_without_action_count = 0
                if len(findAny("1596591250915.png")) > 0:
                    print 'A data button is detected.'
                    click(Pattern("1596591250915.png").targetOffset(-154,145))
                    break
                    
                if action_flag == False:
                    loop_without_action_count += 1
                    print 'loop without action : ' + str(loop_without_action_count)
                
                if loop_without_action_count >= 119:
                    sendMessagetoSlack(mentionUser,'Too many loops without actions. This app will be restarted.', appname)
                    breakFlag = True
                    loop_without_action_count = 0
    
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
                    
                if len(findAny(Pattern("1596592571942-1.png").similar(0.86))) > 0:
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
    
            #告知画面のスキップ
            for num in range(10):
                print 'checking OK buttons...' + str(num)
                if exists(OK,3) !=None:
                    click(OK)
                    wait(1)
                else:
                    break
            click("1596781025606.png")
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
            CommonDMLib.uploadScreenShotToSlack(mentionUser, str(username), appname)
            click("1597235388434.png")
            exists("1597235404354.png",10)
            click("1597235404354.png")
            click(Pattern("1600004482153.png").targetOffset(9,-27))
            exists("1600004545866.png", 60)
            click("1600004566684.png")
            click(Pattern("1600004640701.png").targetOffset(-263,282))
            click("1600004681385.png")
            exists("1600004729257.png",10)
            click(Pattern("1600004729257.png").targetOffset(6,330))
            exists("1600004802890.png", 120)
            click("1597235437582.png")
            exists("1597235476942.png",60)
            for openCardListLoop in range(100):
                if len(findAny("1596780580130.png")) > 0:
                    try:
                        click("1596780580130.png")
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
            for deckCode in deckCodes:
                click("1596780734703.png")
                click("1596780746138.png")
                click(Pattern("1596780800323.png").targetOffset(-2,35))
                wait(2)
                type(deckCode)
                click("1596792937212.png")
                click("1596780865630.png")
                for saveDeckLoop in range(100):
                    if len(findAny(Pattern("1596780884368.png").similar(0.90))) > 0:
                        try:
                            click(Pattern("1596780884368.png").similar(0.90))
                        except:
                            print "failed to click"
                    if len(findAny(Pattern("1600159324860.png").similar(0.90))) > 0:
                        try:
                            click("1600159349574.png")
                        except:
                            print "failed to click"
                        wait(1)
                        break
                    if len(findAny("1600160521444.png")) > 0:
                        try:
                            click(Pattern("1600160521444.png").targetOffset(-5,68))
                        except:
                            print "failed to click"
                exists("1596787598791.png", 30)
            CommonDMLib.sendMessagetoSlack(mentionUser,'Setup has finished.', appname)
            instanceIndex += 1
            break
        except:
            e = sys.exc_info()
            for mes in e:
                print(mes)
            CommonDMLib.sendMessagetoSlack(mentionUser,'Error occured. Restarting..', appname)
            CommonDMLib.sendMessagetoSlack( mentionUser,traceback.format_exc(), appname)
            wait(5)