# -*- coding: utf-8 -*-
from sikuli import *
import urllib2
import json
import shutil
import os
import subprocess
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import CommonDMLib
import NoxResources

#Resouces
#Nox Home
dmpIcon = Pattern("1596585539172.png").similar(0.80)
settingIcon = "settingIcon.png"
closeIconBlack = Pattern("closeIconBlack.png").targetOffset(358,1)
windowIcon = "windowIcon.png"
backIcon = Pattern("backIcon.png").similar(0.80)
noTasksIcon = "noTasksIcon.png"

#DMP Menu
skip = Pattern("skip.png").similar(0.91)
OK = Pattern("OK.png").similar(0.81)
smallOK = Pattern("smallOK.png").similar(0.84)
cancel = Pattern("1596765861356.png").similar(0.84)
smallBattleStart = Pattern("1596767585645.png").similar(0.86)
largeBattleStart = "1596767599082.png"
BUTTON_BACK = "1596962178461.png" 
MISSION_TITLE =  "1596776003050.png"
ICON_SOLO_PLAY = Pattern("1596767681008.png").similar(0.80)
ICON_MISSION = "1596775980978.png"
MENU_MAIN_STORY = "1596767702129.png"
TAP_AND_NEXT = "TAP_AND_NEXT.png"
TUTORIAL_MAIN = "1596767507281.png"

###################Daily Mission############################
#spell
TenTimesSpell = Pattern("TenTimesSpell-1.png").similar(0.85)
TwelveTimesSmallSpell = Pattern("TwelveTimesSmallSpell-1.png").similar(0.85)

#Summon
Summon10Creatures = Pattern("Summon10Creatures-1.png").similar(0.85)
Summon6BigCreaturesCost5 = Pattern("Summon6BigCreaturesCost5-1.png").similar(0.80)
Summon6BigCreaturesPower5000 = Pattern("Summon6BigCreaturesPower5000.png").similar(0.85)
Summon18Creatures = Pattern("Summon18Creatures-1.png").similar(0.85)
Play50CostCards = Pattern("Play50CostCards-1.png").similar(0.85)
#Duel
WinIn10Turns = Pattern("WinIn10Turns.png").similar(0.85)
Charge10Manas = Pattern("Charge10Manas.png").similar(0.85)
FiveTimesBattle = Pattern("FiveTimesBattle-1.png").similar(0.86)
Break3ShieldsInOneTurn = Pattern("Break3ShieldsInOneTurn-1.png").similar(0.86)
WinWith4ShieldsRemained = Pattern("WinWith4ShieldsRemained-1.png").similar(0.85)
WinWith2ShieldsRemained = Pattern("WinWith2ShieldsRemained.png").similar(0.85)
Win5Times = Pattern("Win5Times-1.png").similar(0.85)
WinIn7Turns = Pattern("WinIn7Turns.png").similar(0.85)
Draw20Cards = Pattern("Draw20Cards.png").similar(0.85)
Break10Shields = Pattern("Break10Shields.png").similar(0.85)

#Battle
Destroy4Creatures = Pattern("1596881282876-1.png").similar(0.85)
FiveTimesBattleWithCreatures = Pattern("FiveTimesBattleWithCreatures-1.png").similar(0.85)

#ST
FiveTimesST = Pattern("FiveTimesST-1.png").similar(0.85)


SPELL_MISSIONS = [TenTimesSpell,TwelveTimesSmallSpell]
SPEED_MISSIONS = [Draw20Cards,WinIn7Turns,WinWith2ShieldsRemained,Summon10Creatures,Summon18Creatures,Play50CostCards,WinWith4ShieldsRemained,Win5Times,WinIn10Turns,Charge10Manas,Break10Shields]
BATTLE_MISSIONS = [Destroy4Creatures,FiveTimesBattleWithCreatures]
SHIELDTRRIGER_MISSIONS = [FiveTimesST]
LARGE_CREATURES = [Summon6BigCreaturesCost5,Summon6BigCreaturesPower5000,Break3ShieldsInOneTurn]
RETIRE = [FiveTimesBattle]

################DMP Game###############
turnEnd = "turnEnd.png"
mana0 = Pattern("mana0_beforeCharge.png").similar(0.95)
mana1 = Pattern("mana1.png").similar(0.95)
mana2 = Pattern("mana2_beforeCharge.png").similar(0.95)
mana3 = Pattern("mana3_beforeCharge.png").similar(0.95)
mana4 = Pattern("mana4_beforeCharge.png").similar(0.95)
mana5 = Pattern("mana5_beforeCharge.png").similar(0.95)
mana6 = Pattern("mana6_beforeCharge.png").similar(0.95)
mana7 = Pattern("mana7_beforeCharge.png").similar(0.95)
mana8 = Pattern("mana8_beforeCharge.png").similar(0.95)
mana9 = Pattern("mana9_beforeCharge.png").similar(0.95)
mana10 = Pattern("mana10_beforeCharge.png").similar(0.95)
mana11 = Pattern("mana11.png").similar(0.95)
wcost1 = Pattern("wcost1.png").similar(0.85).targetOffset(81,51)
wcost2 = Pattern("wcost2.png").similar(0.85).targetOffset(74,55)
wcost3 = Pattern("wcost3.png").similar(0.95).targetOffset(51,50)
wcost4 = Pattern("wcost4.png").similar(0.90).targetOffset(89,77)
wcost6 = Pattern("wcost6.png").similar(0.85).targetOffset(56,57)
wcost7 = Pattern("wcost7.png").similar(0.85).targetOffset(59,69)
gcost2 = Pattern("gcost2.png").similar(0.90).targetOffset(83,55)
gcost3 = Pattern("gcost3.png").similar(0.90).targetOffset(70,67)
gcost4 = Pattern("gcost4.png").similar(0.90).targetOffset(75,72)
gcost5 = Pattern("gcost5.png").similar(0.90).targetOffset(92,56)
gcost7 = Pattern("gcost7.png").similar(0.90).targetOffset(89,63)
bcost1 = Pattern("bcost1.png").similar(0.90).targetOffset(56,50)
bcost2 = Pattern("bcost2.png").similar(0.90).targetOffset(85,58)
bcost3 = Pattern("bcost3.png").similar(0.90).targetOffset(87,71)
bcost4 = Pattern("bcost4.png").similar(0.90).targetOffset(81,54)
rcost2 = Pattern("rcost2.png").similar(0.90).targetOffset(69,63)
rcost3 = Pattern("rcost3.png").similar(0.90).targetOffset(74,66)
rcost4 = Pattern("rcost4.png").similar(0.90).targetOffset(76,74)
rcost5 = Pattern("rcost5.png").similar(0.90).targetOffset(77,45)
kcost2 = Pattern("kcost2.png").similar(0.90).targetOffset(75,64)
kcost3 = Pattern("kcost3.png").similar(0.90).targetOffset(64,74)
kcost4 = Pattern("kcost4.png").similar(0.90).targetOffset(71,67)

creature = Pattern("creature.png").similar(0.90).targetOffset(5,77)

def openMission():
    print "openMission"
    for openLoop in range(100):
        print "opening mission..." + str(openLoop)
        if len(findAny(ICON_MISSION)) > 0:
            click(ICON_MISSION)
            wait(1)
        if len(findAny(MISSION_TITLE)) > 0:
            break

def getMissionStrategy(pattern):
    print "getMissionStrategy"
    if pattern in SPELL_MISSIONS:
        return 1
    if pattern in SPEED_MISSIONS:
        return 2
    if pattern in BATTLE_MISSIONS:
        return 3
    if pattern in SHIELDTRRIGER_MISSIONS:
        return 4
    if pattern in LARGE_CREATURES:
        return 5
    if pattern in RETIRE:
        return 6
    return 0

def changeMission():
    print "changeMission"
    if exists(Pattern("1596776105685.png").similar(0.85), 1) != None:
        click(Pattern("1596776105685.png").similar(0.85).targetOffset(414,63))
        wait(3)
        if exists(OK, 10) != None:
            click(OK)
            wait(1)
    if exists(Pattern("FourTimesBigSpell-1.png").similar(0.85), 1) != None:
        click(Pattern("FourTimesBigSpell-1.png").similar(0.85).targetOffset(464,66))
        wait(3)
        if exists(OK, 10) != None:
            click(OK)
            wait(1)
    wait(5)

def getMissionPattern():
    print "getMissionPattern"
    spellResult = findAny(SPELL_MISSIONS)
    speedResult = findAny(SPEED_MISSIONS)
    battleResult = findAny(BATTLE_MISSIONS)
    STResult = findAny(SHIELDTRRIGER_MISSIONS)
    LargeResult = findAny(LARGE_CREATURES)
    retireResult = findAny(RETIRE)
    if len(spellResult) > 0:
        print "Spell strategy"
        return  SPELL_MISSIONS[spellResult[0].getIndex()]
    if len(battleResult) > 0:
        print "Battle strategy"
        return  BATTLE_MISSIONS[battleResult[0].getIndex()]
    if len(STResult) > 0:
        print "ST strategy"
        return  SHIELDTRRIGER_MISSIONS[STResult[0].getIndex()]
    if len(LargeResult) > 0:
        print "Large strategy"
        return  LARGE_CREATURES[LargeResult[0].getIndex()]
    if len(speedResult) > 0:
        print "Speed strategy"
        return  SPEED_MISSIONS[speedResult[0].getIndex()]
    if len(retireResult) > 0:
        print "Retire strategy"
        return  RETIRE[retireResult[0].getIndex()]
    return None

def closeMission():
    print "closeMission"
    click("1596776234501.png")
    waitVanish(MISSION_TITLE, 30)

#True : On
#False : Off
def isNoxOn():
    command1 = 'tasklist'
    command2 = 'findstr Nox.exe'
    proc1 = subprocess.Popen(
        command1,
        shell  = True,
        stdin  = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)
    
    proc2 = subprocess.Popen(
        command2,
        shell  = True,
        stdin  = proc1.stdout,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)
    
    stdout_data, stderr_data = proc2.communicate()
    return stdout_data != ""

def exitNox():
    if isNoxOn() == False:
        print "closing Multiplayer"
        App(EnvSettings.NoxMultiPlayerPath).close()
        return
    
    App(EnvSettings.NoxMultiPlayerPath).open()
    if exists(Pattern("1596962591946.png").targetOffset(92,154),120) == None:
        killMultiPlayerManager()
        raise Exception("MultiPlayerManager has error. Please retry to launch.")
    for num in range(10):
        if exists(Pattern("1596777933938.png").similar(0.90), 1) == None:
            wheel(Pattern("1596962591946.png").targetOffset(92,154), Button.WHEEL_DOWN, 1)
        else:
            break
    for num in range(10):
        if exists(Pattern("1596777933938.png").similar(0.90), 1) == None:
            wheel(Pattern("1596962591946.png").targetOffset(92,154), Button.WHEEL_UP, 2)
        else:
            break
    if len(findAny(Pattern("1596777933938.png").similar(0.90))) > 0:
        click(Pattern("1596777933938.png").similar(0.90))
        if exists(Pattern("1596777989679.png").similar(0.90), 10) != None:
            click(Pattern("1596777989679.png").similar(0.90))
        waitVanish(Pattern("1596777933938.png").similar(0.90), 120)
    App(EnvSettings.NoxMultiPlayerPath).close()

def openNoxInstance(ref):
    App(EnvSettings.NoxMultiPlayerPath).open()
    if exists(Pattern("1596962591946.png").targetOffset(92,154),120) == None:
        killMultiPlayerManager()
        raise Exception("MultiPlayerManager has error. Please retry to launch.")
    exists(Pattern("1601077335160.png").similar(0.95), 120)
    click(Pattern("1601077099284.png").similar(0.95).targetOffset(-59,2))
    wait(0.5)
    type(str(ref))
    type(Key.ENTER)
    wait(5)
    if len(findAny(Pattern("1601077335160.png").similar(0.95))) > 0:
        click(Pattern("1601077335160.png").similar(0.95))
    else:
        raise Exception("No instance : " + str(ref))
    App(EnvSettings.NoxMultiPlayerPath).close()
    
def RestartNox(ref):
    exitNox()
    wait(3)
    openNoxInstance(ref)

    for noxLaunchLoop in range(600):
        print "noxLaunchLoop..." + str(noxLaunchLoop)
        if len(findAny(NoxResources.MESSAGE_FAILED_TO_START_LAUNCHER)) > 0:
            try:
                click(NoxResources.MESSAGE_FAILED_TO_START_LAUNCHER)
            except:
                print "failed to click"
        if len(findAny(NoxResources.ICON_BROWSER)) > 0:
            break
        wait(1)
    wait(30)
    if len(findAny(NoxResources.MESSAGE_BACKUP)) > 0:
        click(NoxResources.MESSAGE_BACKUP)
        click(0.2)
        click(NoxResources.MESSAGE_BACKUP_NODISP)
        wait(1)
        click(NoxResources.BUTTON_NOX_OK)


    
#######################################################
#####################In Game View######################
#######################################################

#マナチャージ前の光ってる状態でマナ数を確認する。
#return : マナ数
def getManaNumBeforeCharge():
    print 'getManaNumBeforeCharge'
    targetImages = [mana0, mana1, mana2, mana3, mana4, mana5, mana6, mana7]#, mana8, mana9, mana10, mana11]
    res = findAny(targetImages)
    if len(res) > 0:
        return res[0].getIndex()
    else:
        return 7

#現在のマナ数以内で召喚できるクリーチャーを召喚する。
#緑1-5までに対応済み
def Summon5(currentMana):
    print 'Summon'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    for num in range(5):
        summon_creature = None
        w1 = findAny(wcost1)
        w2 = findAny(wcost2)
        w6 = findAny(wcost6)
        w7 = findAny(wcost7)
        g2 = findAny(gcost2)
        g3 = findAny(gcost3)
        g7 = findAny(gcost7)
                
        if len(w2) > 0 and availableMana >= 2 and len(findAny(Pattern("1600745743151.png").similar(0.80))) == 0:
            print 'Summon White Cost2'
            summon_creature = w2[0]
            availableMana-=2
        elif len(w1) > 0 and availableMana >= 1 and len(findAny(Pattern("1600745743151.png").similar(0.80))) == 0:
            print 'Summon White Cost1'
            summon_creature = w1[0]
            availableMana-=1
        elif len(g2) > 0 and availableMana >= 2 and availableMana <= 6:
            print 'Summon Green Cost2'
            summon_creature = g2[0]
            availableMana-=1
        elif len(g3) > 0 and availableMana >= 3 and availableMana <= 5:
            print 'Summon Green Cost3'
            summon_creature = g3[0]
            availableMana-=2
        elif len(w6) > 0 and availableMana >= 6:
            print 'Summon White Cost6'
            summon_creature = w6[0]
            availableMana-=6
        elif len(g7) > 0 and availableMana >= 7:
            print 'Summon Green Cost7'
            summon_creature = g7[0]
            availableMana-=7
        elif len(w7) > 0 and availableMana >= 7:
            print 'Summon White Cost7'
            summon_creature = w7[0]
            availableMana-=7
        else:
            break

        try:
            CommonDMLib.dragDropAtSpeed(summon_creature, Pattern("1596771916374.png").targetOffset(-430,221), 1.2)
        except:
            Settings.MoveMouseDelay = 0.1
            break
        wait(1)

def Summon2(currentMana):
    print 'Summon'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    for num in range(10):
        summon_creature = None
        w1 = findAny(wcost1)
        w2 = findAny(wcost2)
        w3 = findAny(wcost3)
        w4 = findAny(wcost4)
        g2 = findAny(gcost2)
        g3 = findAny(gcost3)
        g4 = findAny(gcost4)
        g5 = findAny(gcost5)
        g7 = findAny(gcost7)

        if len(w1) > 0 and availableMana >= 1:
            summon_creature = w1
            availableMana-=1
        elif len(w2) > 0 and availableMana >= 2:
            summon_creature = w2
            availableMana-=2
        elif len(g2) > 0 and availableMana >= 2:
            summon_creature = g2
            availableMana-=2
        elif len(g3) > 0 and availableMana >= 3:
            summon_creature = g3
            availableMana-=3
        elif len(w3) > 0 and availableMana >= 3:
            summon_creature = w3
            availableMana-=3
        elif len(g5) > 0 and availableMana >= 5:
            summon_creature = g5
            availableMana-=5
        elif len(w4) > 0 and availableMana >= 4:
            summon_creature = w4
            availableMana-=4
        
        else:
            break
        try:
            CommonDMLib.dragDropAtSpeed(summon_creature[0], Pattern("1596771916374.png").targetOffset(-430,221), 1.5)
        except:
            Settings.MoveMouseDelay = 0.1
            break
        wait(1)

def SummonRedBlack(currentMana):
    print 'SummonRedBlack'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    for num in range(10):
        print "checking summon..." + str(num)
        summon_creature = None
        r2 = findAny(rcost2)
        r3 = findAny(rcost3)
        r4 = findAny(rcost4)
        k2 = findAny(kcost2)
        k3 = findAny(kcost3)
        k4 = findAny(kcost4)


        if availableMana == 2:
            if len(k2) > 0:
                summon_creature = k2
                availableMana-=2
            elif len(r2) > 0:
                summon_creature = r2
                availableMana-=2
            else:
                break
        elif availableMana == 3:
            if len(k3) > 0:
                summon_creature = k3
                availableMana-=3
            elif len(r3) > 0:
                summon_creature = r3
                availableMana-=3
            elif len(k2) > 0:
                summon_creature = k2
                availableMana-=2
            elif len(r2) > 0:
                summon_creature = r2
                availableMana-=2
            else:
                break
        elif availableMana >= 4:
            if len(r4) > 0:
                summon_creature = r4
                availableMana-=4
            elif len(k2) > 0:
                summon_creature = k2
                availableMana-=2
            elif len(r2) > 0:
                summon_creature = r2
                availableMana-=2
            elif len(k3) > 0:
                summon_creature = k3
                availableMana-=3
            elif len(r3) > 0:
                summon_creature = r3
                availableMana-=3
            elif len(k4) > 0:
                summon_creature = k4
                availableMana-=4
            else:
                break
        else:
            break
        try:
            CommonDMLib.dragDropAtSpeed(summon_creature[0], Pattern("1596771916374.png").targetOffset(-430,221), 1.2)
        except:
            Settings.MoveMouseDelay = 0.1
            break
        wait(1)

def Summon1(currentMana):
    print 'Summon1'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    for num in range(10):
        summon_creature = None
        g2 = findAny(gcost2)
        g3 = findAny(gcost3)
        g4 = findAny(gcost4)
        g5 = findAny(gcost5)
        b1 = findAny(bcost1)
        b2 = findAny(bcost2)
        b3 = findAny(bcost3)
        b4 = findAny(bcost4)
        
        if len(b1) > 0 and availableMana >= 1:
            summon_creature = b1
            availableMana-=1
        elif len(g2) > 0 and availableMana >= 2:
            summon_creature = g2
            availableMana-=1
        elif len(b4) > 0 and availableMana >= 4:
            summon_creature = b4
            availableMana-=4
        elif len(b2) > 0 and availableMana >= 2:
            summon_creature = b2
            availableMana-=2
        elif len(g4) > 0 and availableMana >= 4:
            summon_creature = g4
            availableMana-=4
        elif len(b3) > 0 and availableMana >= 3:
            summon_creature = b3
            availableMana-=3
        elif len(g3) > 0 and availableMana >= 3:
            summon_creature = g3
            availableMana-=3
        elif len(g5) > 0 and availableMana >= 5:
            summon_creature = g5
            availableMana-=5
        else:
            break
        CommonDMLib.dragDropAtSpeed(summon_creature[0], Pattern("1596771916374.png").targetOffset(-430,221), 1.5)
        wait(1)
        if summon_creature == b2 or summon_creature == g4:
            if len(findAny(Pattern("1596934235569.png").similar(0.88),Pattern("1596934544674.png").similar(0.88))) > 0:
                c = findAny(Pattern("1596934367665.png").similar(0.90).targetOffset(10,59), Pattern("1596934765015.png").similar(0.85).targetOffset(0,56),Pattern("1596935014118.png").similar(0.90).targetOffset(-1,54))
                if len(c) > 0:
                    click(c[0])
                    click("1596934406657.png")
                else:
                    click("1596934685736.png")
        


#手札の情報を取得する。
#TODO:現状緑の1-5コスト、白の6コストのみ対象
#return : 手札情報の配列
def getHandInfo():
    print 'getHandInfo'
    handInfo = []
    targetImages = [gcost2,gcost3,gcost5,gcost7,wcost1,wcost2,wcost3,wcost4,wcost6,bcost1,bcost2,bcost3,bcost4,rcost2,rcost3,rcost4,kcost2,kcost3,kcost4]

    f = Finder(SCREEN.capture())
    
    for target in targetImages:
        f.findAll(target)
        counter = 0
        while f.hasNext():
           counter+=1
           f.next()
        handInfo.append(counter)
    return handInfo

def getHandSum(handInfo):
    sum = 0
    for hand in handInfo:
        sum+=hand
    return sum

#手札からマナへチャージする。
def ChargeMana5():
    print 'ChargeMana'
    #マナ取得
    mana = getManaNumBeforeCharge()
    print 'ManaZone(Before charge):' + str(mana)
    Hand = None
    #　チャージ
    if len(findAny("1600745743151.png")) > 0:
        Hand = findAny(gcost5,wcost3,wcost4,wcost1,gcost3,wcost2,gcost2)
    else:
        Hand = findAny(gcost5,wcost3,wcost4,gcost3,gcost2)
        
    
    if len(Hand) > 0:
        CommonDMLib.dragDropAtSpeed(Hand[0], Pattern("1596771322109.png").targetOffset(25,-78), 1.5)
    return mana + 1

def ChargeMana1():
    print 'ChargeMana1'
    #マナ取得
    mana = getManaNumBeforeCharge()
    print 'ManaZone(Before charge):' + str(mana)
    hand = getHandSum(getHandInfo())
    print 'Hand:' + str(hand)
    #　チャージ
    if mana >= 0 and mana <=20 and hand >= 0:
        Hand = findAny(gcost5,bcost3,gcost3,bcost1)
    else:
        return mana
    
    if len(Hand) > 0:         
        CommonDMLib.dragDropAtSpeed(Hand[0], Pattern("1596771322109.png").targetOffset(25,-78), 1.5)
    return mana + 1

def ChargeMana2():
    print 'ChargeMana2'
    #マナ取得
    mana = getManaNumBeforeCharge()
    print 'ManaZone(Before charge):' + str(mana)
    hand = getHandSum(getHandInfo())
    print 'Hand:' + str(hand)
    #　チャージ
    if mana == 0:
        Hand = findAny(wcost4,wcost1,wcost2,gcost5,gcost3,gcost2)
    elif mana >= 1 and mana <=6 and hand >= 3:
        Hand = findAny(wcost4,gcost5,gcost3,gcost2,wcost1,wcost2)
    else:
        return mana
    
    if len(Hand) > 0:         
        CommonDMLib.dragDropAtSpeed(Hand[0], Pattern("1596771322109.png").targetOffset(25,-78), 1.5)
    return mana + 1

def ChargeManaRedBlack():
    print 'ChargeManaRedBlack'
    #マナ取得
    mana = getManaNumBeforeCharge()
    print 'ManaZone(Before charge):' + str(mana)
    #hand = getHandSum(getHandInfo())
    #print 'Hand:' + str(hand)
    #　チャージ
    if mana == 0:
        Hand = findAny(rcost5,rcost4,rcost3,rcost2,kcost4,kcost3,kcost2)
    elif mana == 1:
        Hand = findAny(kcost4,kcost3,rcost5,rcost4,rcost3,rcost2,kcost2)
    elif mana >= 2 and mana <=3:
        Hand = findAny(rcost5,kcost4,rcost3,kcost3,rcost4,rcost2,kcost2)
    elif mana >= 4:
        Hand = findAny(rcost5)
    else:
        return mana
    
    if len(Hand) > 0:         
        CommonDMLib.dragDropAtSpeed(Hand[0], Pattern("1596771322109.png").targetOffset(25,-78), 1.2)
        mana += 1
    return mana

#シールド数を取得する。
#追加シールド(黄色)も対応済み
def getSheildObj(img):
    handInfo = []
    targetImage = img

    f = Finder(SCREEN.capture())
    f.findAll(targetImage)
    result = []
    while f.hasNext():
       result.append(f.next())
    return result

#バトルゾーンのクリーチャーで相手プレーヤーを攻撃する。
#U/UC/R/ダボラッシュに対応済み
#TODO:VR/SRのアタックに対応する。
#TODO:シールドトリガー発生時のクリーチャー選択、手札選択に対応する。
def directAttack(sheildImg):
    print 'directAttack'
    for num in range(7):
        print "directAttack..." + str(num)
        BZ = findAny(creature)
        if len(BZ) > 0:
            try:
                CommonDMLib.dragDropAtSpeed(BZ[0],Pattern("1596770245448.png").targetOffset(-419,68), 1.2)

                if exists(Pattern("1599317424929.png").similar(0.85), 5) != None:
                    for directAttackLoop in range(10):
                        click(Pattern("1596770307126.png").targetOffset(-244,-376))
                        click(Pattern("1596770307126.png").targetOffset(241,-386))
                        click("1596770360694.png")
                        wait(0.2)
                        if len(findAny("1596770360694.png")) == 0:
                            break
                wait(1)
            except:
                Settings.MoveMouseDelay = 0.1
                break
        else:
            break

def battle():
    print "Battle"
    for num in range(7):
        BZ = findAny(creature)
        if len(BZ) > 0:
            c = findAny(Pattern("1596980426580.png").similar(0.85).targetOffset(0,60))
            if len(c) > 0:
                CommonDMLib.dragDropAtSpeed(BZ[0],c[0], 1.5)
                wait(0.5)
    
def retire():
    for retireLoop in range(5):
       click(backIcon)
       if exists("1598228582187.png", 10) != None:
           click("1598228593885.png")
           break
       if retireLoop == 4:
           raise Exception


EFFECT_QUESTION = Pattern("1596934235569.png").similar(0.81)
BOUNCE_QUESTION = Pattern("1596934544674.png").similar(0.88)
TAP_QUESTION = Pattern("TAP_QUESTION.png").similar(0.90)
DEST_QUESTION = Pattern("DEST_QUESTION.png").similar(0.85)
TARGET_QUESTION = Pattern("TARGET_QUESTION.png").similar(0.89)

#ゲーム中のイレギュラーの処理
#return 0 ゲームの正常終了
#return 1 ゲーム継続
def irregularLoop():
    print 'irregularLoop'
#  イレギュラーループ
    for enemyturn_loop in range(50):
        print 'This is ' + str(enemyturn_loop) + ' times loop.'
        #   自分のターンを検知
        if len(findAny(turnEnd)) > 0:
            print 'My Turn is detected.'
            wait(3)
            break
        #   対戦開始を検知→ゲームループをbreak
        if len(findAny(smallBattleStart)) > 0:
            print 'Game has Finished.'
            return 0
        if len(findAny("1596901274897.png")) > 0:
           #game_loopを終了する。
            click("1596901274897.png")
        #ブロックするか
        
        #   トリガー発動 
        if len(findAny("1596775378272.png")) > 0:
            print 'Block?'
            if len(findAny(Pattern("1596903270708.png").similar(0.80).targetOffset(-4,74))) > 0:
                try:
                    click(Pattern("1596903270708.png").similar(0.80).targetOffset(-4,74))
                    click("1596903354174.png")
                except:
                    click("1596775410348.png")
            else:
                click("1596775410348.png")
            wait(1)
        if len(findAny("1596770856485.png")) > 0:
            print 'My ST is triggered.'
            click(Pattern("1596770865154.png").targetOffset(221,-1))
            wait(1)
        if len(findAny(EFFECT_QUESTION,BOUNCE_QUESTION,TAP_QUESTION,DEST_QUESTION,TARGET_QUESTION)) > 0:
            c = findAny(Pattern("1596934367665.png").similar(0.90).targetOffset(10,59),Pattern("1596935014118.png").similar(0.90).targetOffset(-1,54))
            if len(c) == 0:
                click("1599178222891.png")
            for t in c:
                click(t)
                click("1596934406657.png")
                wait(0.5)
                if len(findAny("1596934406657.png")) == 0:
                   break 
        
        #   シールド確認
        if len(findAny("1596770897993.png"))   > 0:
            print 'My sheild is broken.'
            click("1596770734776.png")
            wait(1)
        #死の宣告、デスモーリー等
#        if len(findAny(Pattern("1594952630070.png").similar(0.95).targetOffset(-20,-217))) > 0:
#            print 'Player need to select his creature.'                       
#            BZ = findAny(Pattern("1595121206331.png").similar(0.95).targetOffset(13,41),Pattern("1595121260947.png").similar(0.90).targetOffset(5,35))
#            if len(BZ) > 0: 
#                click(BZ[0])
#            click("1594951143014.png")
        #デモニックバイス
#        if len(findAny(Pattern("1595035924385.png").similar(0.85))) > 0:
#            print 'Player need to select his hands.'
#            click(Pattern("1595035924385.png").targetOffset(363,188))
#            click(Pattern("1595035924385.png").targetOffset(174,190))
#            click("1595035999600.png")
#            wait(1)

        #日付変更
#        if len(findAny(Pattern("1596758627672.png").similar(0.90))) > 0:
#            raise Exception
        
        if  enemyturn_loop == 49:
            print 'Irregular loop is over 50. Restart is necessary.'
            raise Exception
    
    return 1
            