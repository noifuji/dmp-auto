import sys
import os
import urllib2
import json
import traceback
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import CommonDMLib
import NoxResources

bolbalzarkSec = Pattern("bolbalzarkSec.png").similar(0.90)
bolbalzark = Pattern("bolbalzark.png").similar(0.90)
nikaku = Pattern("nikaku.png").similar(0.90)
blizard = "blizard.png"
court="1603269640458.png"
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
vision = "vision.png"
lancer = "lancer.png"
sapphire = "sapphire.png"
dolbalom="1603262324332.png"
dolbalomSec="1603253252148.png"
spark ="spark.png"
apo = "apo.png"

####################Settings####################
TARGET_DMP = 4000
DECK_BLIZZARD = {"NAME":"Blizzard", "SR" : [blizard], "VR" : [spark,apo,court], "COLOR" : ["1603262159403.png", "1603262167793.png"]}
DECK_LANCER = {"NAME":"Lancer", "SR" : [lancer], "VR" : [vision,surfer], "COLOR" : ["1599975832115.png"]}
DECK_SAPPIRE = {"NAME":"Bolmeteus Sappire", "SR" : [sapphire,sabaki], "VR" : [extreme,surfer,daemonhand], "COLOR" : ["1599975832115.png","1599975856377.png","1599975849850.png"]}
DECK_BALOM = {"NAME":"Balom", "SR" : [dolbalom,dolbalomSec,lostsoul,sabaki], "VR" : [surfer,daemonhand], "COLOR" : ["1599975832115.png","1599975856377.png","1599975849850.png"]}
TARGET_DECKS = [DECK_SAPPIRE,DECK_BALOM,DECK_BLIZZARD,DECK_LANCER]
####################Settings####################
appname = 'RESET'
mentionUser = EnvSettings.mentionUser
Settings.MoveMouseDelay = 0.1
DMApp = App(EnvSettings.NoxAppPath)


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

skip = Pattern("skip.png").similar(0.90)
OK = Pattern("OK.png").similar(0.90)
OK2 = Pattern("OK2.png").similar(0.80)
tutorial = "tutorial.png"
retry = "retry.png"

        
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


for count in range(100):
    try:
        ref = CommonDMLib.getSetupAccountRef()
        if ref == "":
            print "There are no setup accounts."
            break
        print "SetupAccount is started. ref : " + str(ref)
        CommonDMLib.updatePlayerId(ref, "working", os.environ["COMPUTERNAME"])
        print "A tempporary Player ID is updated."
        username = ref
        CommonDMLib.RestartNox(NoxResources,ref)
        CommonDMLib.callRemoveDataBat()
    except:
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.updatePlayerId(ref, "", "")
        CommonDMLib.sendMessagetoSlack(mentionUser,'Failed to launch instance ' + str(ref) + ". Setup was canceled.", appname)
        CommonDMLib.sendMessagetoSlack( mentionUser,traceback.format_exc(), appname)
        break
    
    for num in range(100):
        try:
            CommonDMLib.noxCallKillDMPApp()
            wait(1)
            CommonDMLib.noxCallStartDMPApp()
    
            breakFlag = False
            loop_without_action_count = 0
            action_flag = False
            while loop_without_action_count <= 120:
                if len(findAny("1596591221362.png")) > 0:
                    print 'An agreement button is detected.'
                    try:
                        click("1596591221362.png")
                    except:
                        print "failed to click"
                    action_flag = True
                    loop_without_action_count = 0
                    wait(0.5)
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
                    type(ref)
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
                    print 'Home view was detected. This download loop will break.'
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
                CommonDMLib.skipRewards(NoxResources)
                if len(findAny(NoxResources.ICON_MISSION)) > 0:
                    click(NoxResources.ICON_MISSION)
                    if len(findAny(NoxResources.TITLE_MISSION)) > 0:
                        click(NoxResources.BUTTON_CLOSE)
                        break

            #ホーム画面から初回プレゼントを取得
            wait(5)
            CommonDMLib.getPresent(NoxResources)
            #ショップでパック開封
            click("1596592801262.png")
            for shopTutorialLoop in range(5):
                click(Pattern("1599838544906.png").targetOffset(85,-53))
                wait(1)
            click(Pattern("1596592864693.png").similar(0.90).targetOffset(-5,-237))
            wait(5)
            click(Pattern("1596592907696.png").similar(0.90).targetOffset(-6,-215))
            if exists(Pattern("1603247550151.png").targetOffset(3,75),60) == None:
                continue
            
            for shopTutorialLoop in range(5):
                click(Pattern("1603247550151.png").targetOffset(3,75))
                wait(1)
            
            
            DMPPs = ["1603247648602.png","1603247659238.png","1603247666375.png","1603247673472.png","1603247697352.png","1603247681473.png"]
            #DMPPs = ["1603247648602.png","1603247659238.png","1603247666375.png","1603247673472.png","1603247681473.png","1603247697352.png"]
            DMPP_loop_count = 0
            continue_flag = False
            for DMPP in DMPPs:
                click(DMPP)
                for loop in range(50):
                    print 'Opening pack'
                    if exists(Pattern("1603247969848.png").similar(0.90).targetOffset(-2,56),2) != None:
                        click(Pattern("1603247969848.png").similar(0.90).targetOffset(-2,56))
                    elif exists(Pattern("1603251761995.png").similar(0.90).targetOffset(-1,56),2) != None:
                        click(Pattern("1603251761995.png").similar(0.90).targetOffset(-1,56))
                    else:
                        break
                    exists("1603251877777.png",30)
                    if len(findAny("1596593005414.png")) > 0:
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
                CommonDMLib.dragDropAtSpeed(Pattern("1603248230975.png").targetOffset(85,125),Pattern("1603248251851.png").targetOffset(-234,107),0.5)
                wait(1)
                     
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

            #スキャン後、すべてのレアリティの枚数をカウントする。
            score = 0
            deckName = ""
            successFlag = False
            TARGET_RARITY = [NoxResources.BUTTON_RARITY_VERYRARE, NoxResources.BUTTON_RARITY_SUPERRARE]
            for targetDeck in TARGET_DECKS:
                countKeyCard = {"VR" : 0, "SR" : 0}
                for i in range(len(TARGET_RARITY)):
                    click(Pattern("1596590519784.png").similar(0.90))
                    wait(0.2)
                    click("1599973746387.png")
                    wait(0.2)
                    for color in targetDeck["COLOR"]:
                        click(color)
                        wait(0.2)
                    click(TARGET_RARITY[i])
                    wait(1)
                    wheel(TARGET_RARITY[i], Button.WHEEL_DOWN, 10)
                    wait(2)
                    click("1596590582220.png")
                    click("1596590589379.png")
                    click("1596590596951.png")
                    click("1596590604315.png")
                    click("1597921929724.png")
                    click("1603248373413.png")
                    click("1596590612922.png")
                    wait(3)
                    if i == 0:
                        countKeyCard["VR"] = getTargetCount(targetDeck["VR"])
                    elif i == 1:
                        countKeyCard["SR"] = getTargetCount(targetDeck["SR"])
                
                score = countKeyCard["VR"] * 800 + countKeyCard["SR"] * 2400
                if score >= TARGET_DMP:
                    successFlag = True
                    deckName = targetDeck["NAME"]
                    break
            
            if successFlag:
                mes = 'Success!! [ref = ' + ref  + ", name = " + deckName + ", score=" + str(score) + "]"
                CommonDMLib.sendMessagetoSlack(mentionUser,mes, appname)
                CommonDMLib.uploadScreenShotToSlack(mentionUser,"Screenshot" , appname)
                cardCountResult = CommonDMLib.countAllCardsByRarity(NoxResources)
                CommonDMLib.updateCardCount(ref, cardCountResult["NAMES"], cardCountResult["CARDS"])
                click("1603258852950.png")
                exists("1596781025606.png", 120)
                click("1596781025606.png")
                exists("1597235336512.png",10)
                click("1597235336512.png")
                exists("1597235361421.png",30)
                CommonDMLib.uploadScreenShotToSlack(mentionUser, str(username), appname)
                playerId = CommonDMLib.scanNumberChangeWidth("1601082545206.png", -270, 0, 233, 38, 0, 25)
                CommonDMLib.updatePlayerId(ref, playerId, os.environ["COMPUTERNAME"])
                #スコアとデッキ名称をシートに記載する。
                break
            else:
                print "No Target SRs."
                CommonDMLib.sendMessagetoSlack(mentionUser,'Score : ' + str(score), appname)
                CommonDMLib.uploadScreenShotToSlack(mentionUser,"Screenshot" , appname)
    
            CommonDMLib.noxCallKillDMPApp()
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