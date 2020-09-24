import sys
import os
import urllib2
import json
import traceback
sys.path.append("NoxDMLib.sikuli")
sys.path.append("CommonDMLib.sikuli")
sys.path.append("NoxResources.sikuli")
import NoxDMLib
import CommonDMLib
import NoxResources
import EnvSettings

####################Settings####################
appname = 'ResetLoop'
mentionUser = 'U017DKDFGER'
Settings.MoveMouseDelay = 0.1
DMApp = App(EnvSettings.NoxAppPath)
####################Settings####################

#resources
dmpIcon = "dmpIcon.png"
amazeIcon = "amazeIcon.png"
settingIcon = "settingIcon.png"
closeIconBlack = Pattern("closeIconBlack.png").targetOffset(358,1)
closeIconBlue = Pattern("closeIconBlue.png").targetOffset(360,1)
closeIconGrey = Pattern("closeIconGrey.png").targetOffset(366,5)
closeIconDL = Pattern("closeIconDL.png").similar(0.85).targetOffset(361,3)
windowIcon = "windowIcon.png"
noTasksIcon = "noTasksIcon.png"
rename = Pattern("rename.png").targetOffset(-110,33)
save = Pattern("save.png").targetOffset(114,-5)
bolbalzarkSec = Pattern("bolbalzarkSec.png").similar(0.90)
bolbalzark = Pattern("bolbalzark.png").similar(0.90)
nikaku = Pattern("nikaku.png").similar(0.90)
blizard = "blizard.png"
roba = "roba.png"
dethphoenix = "dethphoenix.png"
dethphoenixSec = "dethphoenixSec.png"
eternalphoenix = "eternalphoenix.png"
sabaki = "sabaki.png"
kuchiyose = "kuchiyose.png"
lostsoul = "lostsoul.png"
burstshot = "burstshot.png"
surfer = "surfer.png"
daemonhand = "daemonhand.png"
extreme = "extreme.png"
skip = Pattern("skip.png").similar(0.90)
OK = Pattern("OK.png").similar(0.90)
OK2 = Pattern("OK2.png").similar(0.80)
tutorial = "tutorial.png"
retry = "retry.png"

def startApp():
    click(windowIcon)
    if exists(closeIconBlack,5) != None:
        click(closeIconBlack) 
    else:
        click(windowIcon)
        
    click(dmpIcon)
    #if exists("1597912712276.png", 30) != None:
    #    click("1597912737782.png")
     #   wait(5)
      #  click("1597912784096.png")
 #       exists("1597912950842.png",120)
  #      click("1597912950842.png")

def closeWindows():
    print 'closeWindows'
    if exists(windowIcon,20) != None:
        click(windowIcon)
        wait(1)
    if exists(closeIconBlack,1) != None:
        click(closeIconBlack)
        wait(1)
    if exists(closeIconGrey,1) != None:
        click(closeIconGrey)
        wait(1)
    if exists(closeIconDL,1) != None:
        click(closeIconDL)
        wait(1)
    if exists(noTasksIcon,1) != None:
        click(windowIcon)
        
def countCard(target):
    x1 = Pattern("x1.png").similar(0.85)
    x2 = Pattern("x2.png").similar(0.92)
    x3 = Pattern("x3.png").similar(0.91)
    x4 = Pattern("x4.png").similar(0.90)
    
    xArray = [x1, x2, x3, x4]
    
    offsetX = 200
    offsetY = 100
    
    res = findAny(target)
    if len(res) == 0:
       return 0
    resX = res[0].getX()
    resY = res[0].getY()
    
    f = Finder(SCREEN.capture())
    for i in range(len(xArray)):
        f.findAll(xArray[i])
        while f.hasNext():
           xresult = f.next()
           if (xresult.getX() - resX) < offsetX and (xresult.getX() - resX) > 0 and (resY - xresult.getY()) < offsetY and (resY - xresult.getY()) > 0:
               print "Count : " + str(i+1)
               print "(x,y)=(" + str(resX) + "," + str(resY) + ")"
               print "(x,y)=(" + str(xresult.getX()) + "," + str(xresult.getY()) + ")"
               return i + 1

def getTargetCount(targets):
    result = 0
    for t in targets:
        result += countCard(t)
    return result

CommonDMLib.callRemoveDataBat()

for num in range(100):
    try:
        startApp()

        breakFlag = False
        loop_without_action_count = 0
        action_flag = False
        while loop_without_action_count <= 120:
            if len(findAny("1596591221362.png")) > 0:
                print 'An agreement button is detected.'
                click("1596591221362.png")
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
                CommonDMLib.sendMessagetoSlack(mentionUser,'Too many loops without actions. This app will be restarted.', appname)
                breakFlag = True
                loop_without_action_count = 0
                break

            action_flag = False
            
        if breakFlag == True:
            continue

        breakFlag = False
        loop_without_action_count = 0
        action_flag = False
        while loop_without_action_count <= 120:
            
            if len(findAny(skip)) > 0:
                print 'A skip button is detected.'
                try:
                    click(skip)
                except:
                    print "failed to click skip"
                action_flag = True
                loop_without_action_count = 0
            if len( findAny("1596591807133.png")) > 0:
                print 'A player name text box is detected.'
                try:
                    click(Pattern("1596591807133.png").targetOffset(351,196))
                except:
                    print "failed to click name"
                wait(0.5)
                type('aaaaa')
                try:
                    click(Pattern("1596591807133.png").targetOffset(-44,101))
                    click(OK)
                except:
                    print "failed to click name"
                wait(0.5)
                action_flag = True 
                
            if len(findAny(OK)) > 0:
                if len( findAny("1596591807133.png")) > 0:
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
                if len( findAny("1596591807133.png")) > 0:
                    continue
                print 'A OK button2 is detected.'
                try:
                    click(OK2)
                except:
                    print "failed to click OK2"
                action_flag = True
                loop_without_action_count = 0

            if len(findAny(retry)) > 0:
                click(retry)
                
            if len(findAny(Pattern("1596592571942.png").similar(0.86))) > 0:
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
        #ホーム画面から初回プレゼントを取得
        click("1596592701367.png")
        exists("1596592717517.png",60)
        click("1596592717517.png")
        if exists(OK2, 20) != None:
            click(OK2)       
            wait(1)
        click(Pattern("1596592773454.png").similar(0.84))
        #ショップでパック開封
        click("1596592801262.png")
        for shopTutorialLoop in range(10):
            click(Pattern("1599838544906.png").targetOffset(85,-53))
            wait(0.2)
        click(Pattern("1596592864693.png").similar(0.90).targetOffset(-5,-237))
        wait(5)
        click(Pattern("1596592907696.png").similar(0.90).targetOffset(-6,-215))

        if exists(Pattern("1596592933299.png").similar(0.83),30) == None:
            continue
        
        DMPPs = ["1596592954751.png","1596592948219.png","1596592961199.png","1597914079551.png"]#"1596592961199.png","1596592954751.png","1596592948219.png","1596592965835.png","1597914079551.png"
        DMPP_loop_count = 0
        continue_flag = False
        for DMPP in DMPPs:
            click(DMPP)
            for loop in range(50):
                print 'Opening pack'
                if exists(Pattern("1596592980976.png").similar(0.90),5) == None:
                    break
                click(Pattern("1596592980976.png").similar(0.90).targetOffset(0,55))
                if exists("1596593005414.png",10) != None:
                    click("1596593005414.png")
                click(OK)
                wait(1)
                click(OK)
                exists("1596593059270.png",10)
                click("1596593059270.png")

                for pack_loop in range(10):
                    if exists("1596601134437.png",5) == None:
                        print 'You got super rare.'
                        #スーパーレア発生
                        click(Pattern("1597929821232.png").targetOffset(561,167))
                        continue
                    else:
                        break

                for pack_loop in range(10):
                    if exists("1596601134437.png",1) != None:
                        click("1596601134437.png")
                        print 'OK is clicked to confirm pack results.'
                        wait(2)
                        continue
                    else:
                        break
                 
        exists("1596593154431.png",10)                
        click("1596593154431.png")
        if exists(OK2,60) != None:
            click(OK2)
        wait(1)
        click("1596593298299.png")
        wait(5)
        click(Pattern("1596593310453.png").targetOffset(-2,-214))
        if exists("1596593154431.png", 120) != None:
            for listTutorialLoop in range(10):
                click(Pattern("1596593154431.png").targetOffset(-2,47))
                wait(0.2)
        countKeyCard = {"VR" : 0, "SR" : 0}
        for i in range(len(NoxResources.BUTTON_RARITY)):
            click(Pattern("1596590519784.png").similar(0.90))
            wait(0.2)
            click("1599973746387.png")
            wait(0.2)
            if i == 0:
                click("1599975832115.png")
                wait(0.2)
                click("1599975856377.png")
                wait(0.2)
                click("1599975849850.png")
                wait(0.2)
            click(NoxResources.BUTTON_RARITY[i])
            wait(1)
            wheel(NoxResources.BUTTON_RARITY[i], Button.WHEEL_DOWN, 10)
            wait(2)
            click("1596590582220.png")
            click("1596590589379.png")
            click("1596590596951.png")
            click("1596590604315.png")
            click("1597921929724.png")
            click("1596590612922.png")
            wait(3)
            if i == 0:
                countKeyCard["VR"] = getTargetCount([burstshot, surfer, daemonhand, extreme])
            elif i == 1:
                countKeyCard["SR"] = getTargetCount([bolbalzarkSec,bolbalzark,sabaki,kuchiyose])
        
        score = countKeyCard["VR"] * 800 + countKeyCard["SR"] * 2400
        
        if score >= 7200:
            CommonDMLib.sendMessagetoSlack(mentionUser,'Target SRs are detected!!', appname)
            CommonDMLib.uploadScreenShotToSlack(mentionUser,"Screenshot" , appname)
            break
        else:
            print "No Target SRs."
            CommonDMLib.sendMessagetoSlack(mentionUser,'Score : ' + str(score), appname)
            CommonDMLib.uploadScreenShotToSlack(mentionUser,"Screenshot" , appname)

        closeWindows()
        wait(1)
        CommonDMLib.callRemoveDataBat()
        wait(3)
    except:
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack(mentionUser,'Error occured. Restarting..', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.uploadScreenShotToSlack(mentionUser,"Screenshot" , appname)
        wait(5)