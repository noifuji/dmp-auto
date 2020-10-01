# -*- coding: utf-8 -*-
from sikuli import *
import urllib2
import json
import shutil
import requests
import os
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import CommonDMLib
import AndAppResources

#ManaZone
mana0 = Pattern("mana0.png").similar(0.90)
mana1 = Pattern("mana1.png").similar(0.90)
mana2 = Pattern("mana2.png").similar(0.90)
mana3 = Pattern("mana3.png").similar(0.90)
mana4 = Pattern("mana4.png").similar(0.90)
mana5 = Pattern("mana5.png").similar(0.94)
mana6 = Pattern("mana6.png").similar(0.95)
mana7 = Pattern("mana7.png").similar(0.91)
mana8 = Pattern("mana8.png").similar(0.90)#
mana9 = Pattern("mana9.png").similar(0.95)
mana10 = Pattern("mana10.png").similar(0.91)
mana11 = Pattern("mana11.png").similar(0.90)
mana12 = Pattern("mana12.png").similar(0.90)

#Reaources
gcost1 = Pattern("1595030130228-1.png").similar(0.85).targetOffset(69,44)
gcost2 = Pattern("1594950595616-1.png").similar(0.85).targetOffset(79,55)
gcost3 = Pattern("1595029444929-1.png").similar(0.90).targetOffset(67,55)
gcost4 = Pattern("1594949422218-1.png").similar(0.83).targetOffset(69,54)
gcost5 = Pattern("1595030120503-1.png").similar(0.90).targetOffset(75,56)
gcost7 = Pattern("1596192523218.png").similar(0.90).targetOffset(55,41)
wcost2 = Pattern("wcost2.png").similar(0.85).targetOffset(68,61)
wcost4 = Pattern("wcost4.png").similar(0.90).targetOffset(72,61)
wcost6 = Pattern("wcost6.png").similar(0.85).targetOffset(70,51)
rcost2 = Pattern("rcost2.png").similar(0.90).targetOffset(64,59)
rcost3 = Pattern("rcost3.png").similar(0.90).targetOffset(67,54)
rcost4 = Pattern("rcost4.png").similar(0.90).targetOffset(66,56)
rcost5 = Pattern("kcost5.png").similar(0.90).targetOffset(53,51)
kcost2 = Pattern("kcost2.png").similar(0.90).targetOffset(61,61)
kcost3 = Pattern("kcost3.png").similar(0.90).targetOffset(64,55)
kcost4 = Pattern("kcost4.png").similar(0.90).targetOffset(61,53)

result = "result.png"

def RestartApp(resource, app):
    print 'RestartApp'
    app.close()
    wait(3)
    app.open()
    wait("1594988274658.png",60)
    click(Pattern("1594988274658.png").targetOffset(-185,175))
    #ログインボーナスやらキャンペーンをスキップ
    for num in range(60):
        print "checking login bonus.." + str(num)
        if len(findAny("1595113534743.png")) > 0: 
            click("1595113534743.png")
        if exists("1594988916491.png",2) != None:
            break
        wait(1)
        
    if CommonDMLib.skipNotifications(resource, 5) == -1:
        #SPリザルト画面表示
        wait(5)
        click("1595460202558.png")
        wait(5)
        click("1595460239140.png")
        wait(20)
    CommonDMLib.skipRewards(resource, 5)
    
def openAndStartMainStory(resource):
    print 'openAndStartMainStory'
    click(Pattern("1594989699401.png").similar(0.60).targetOffset(178,-50))
    wait("1595065859928.png",10)
    click("1595065868601.png")
    if exists(Pattern("1596699277800.png").similar(0.85),20) != None:
            click(Pattern("1596699277800.png").similar(0.85))
            wait(5)
            click(Pattern("1596699277800.png").similar(0.85))
            wait(5)
    wait("1595205824088.png",30)
    click(Pattern("1595205824088-1.png").targetOffset(-139,233))
    wait(1)
    strategy = 0
    if len(findAny(TITLE_EP4_STAGE3)) > 0 and len(findAny(TITLE_EP4_STAGE4)) == 0:
        strategy = 1
    elif len(findAny(TITLE_EP4_STAGE9)) > 0 and len(findAny(TITLE_EP4_STAGE10)) == 0:
        strategy = 1
    elif len(findAny(TITLE_EP2_STAGE21)) > 0 and len(findAny(TITLE_EP2_STAGE22)) == 0:
        strategy = 1
    elif len(findAny(TITLE_EP2_STAGE28)) > 0 and len(findAny(TITLE_EP2_STAGE29)) == 0:
        strategy = 1
    else:
        strategy = 0
    click("1595065941505.png")
    exists("1595065960896.png",30)
    if strategy == 1:
        if CommonDMLib.chooseDeck(resource, Pattern("1598888491089.png").similar(0.85)) == False:
            CommonDMLib.addNewDeckByCode(resource, EnvSettings.DECKCODE_RED_BLACK)
            
    elif strategy == 0:
        CommonDMLib.chooseDeck(resource, "DECK.png")
    click("1595065960896.png")
    return strategy

def OpenAndStartCityBattle(img):
    click(Pattern("1594989699401-1.png").similar(0.60).targetOffset(178,-50))
    wait("1594989059402.png",10)
    click(Pattern("1594989059402.png").targetOffset(-3,-75))
    wait("1595392954553.png",10)
    for num in range(100):
        if len(findAny(img)) > 0:
            click(img)
            break
        else:
            print 'No target image. Trying to wheel.'
            wheel(Pattern("1595393111811.png").targetOffset(-146,134), Button.WHEEL_DOWN, 1)
            wait(1)

        if num == 99:
            print 'No target image.'
            raise Exception
    
    wait(1)
    click("1594990173795.png")
    wait("1594990194522.png",30)
    click("1594990194522.png")

def openAndStartSPBattle(resource, code) :
    print 'openAndStartSPBattle'
    click("1595253546948.png")
    wait(3)
    click("1595253556265.png")
    exists("1599121165504.png", 60)
    if exists("1599121179809.png", 1) != None:
        for tutorialLoop in range(5):
            click(Pattern("1599121165504.png").targetOffset(86,7))
            wait(1)
    click("1595253571082.png")
    exists("1595253595048.png",60)
    resultChoose = CommonDMLib.chooseDeck(resource, "1599121629375.png")
    if resultChoose == False:
        CommonDMLib.addNewDeckByCode(resource, code)
    click("1595253595048.png")

def openAndStartLegendBattle(img):
    print 'openAndStartLegendBattle'
    result = 0
    click("1595253546948.png")
    click(Pattern("1595977354621.png").targetOffset(-23,-92))
    
    wait(img, 60)
    click(img)
    click("1595977375290.png")
    wait("1595977394372.png",60)
    click("1595977394372.png")
    return result
    
#######################################################
#####################In Game View######################
#######################################################

#マナチャージ前の光ってる状態でマナ数を確認する。
#return : マナ数
def getManaNumBeforeCharge():
    print 'getManaNumBeforeCharge'
    targetImages = [mana0,mana1,mana2,mana3,mana4,mana5,mana6,mana7,mana8,mana9,mana10,mana11,mana12]
    res = findBest(targetImages)
    if res != None:
        return res.getIndex()
    return 7
            
#マナチャージ後の光が消えた状態でマナ数を確認する。
#return : マナ数
def getManaNumAfterCharge():
    print 'getManaNumAfterCharge'
    targetImages = [Pattern("1595036918941.png").similar(0.95),Pattern("1595036938436.png").similar(0.95),Pattern("1595036964263.png").similar(0.95),Pattern("1595036985457.png").similar(0.95),Pattern("1595036864104.png").similar(0.95),Pattern("1595048750355.png").similar(0.95),Pattern("1595048823156.png").similar(0.95),Pattern("1595048944275.png").similar(0.95),Pattern("1595049042692.png").similar(0.95),Pattern("1595049098156.png").similar(0.95),Pattern("1595049166140.png").similar(0.95),Pattern("1595049207141.png").similar(0.95)]
    counter = 1
    for target in targetImages:
        if len(findAny(target)) > 0:
            return counter
        counter+=1

def existsBlocker():
    if len(findAny(Pattern("1599114153262.png").similar(0.85),Pattern("1599114546868.png").similar(0.85),Pattern("1599114574848.png").similar(0.84))) > 0:
        return True
    return False

#現在のマナ数以内で召喚できるクリーチャーを召喚する。
#緑1-5までに対応済み
def Summon(currentMana):
    print 'Summon'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    for num in range(10):
        summon_creature = None
        res = findAny(gcost1,gcost2,gcost3,gcost4,gcost5,gcost7)
        g1 = None
        g2 = None
        g3 = None
        g4 = None
        g5 = None
        g7 = None
        for r in res:
            if r.getIndex() == 0:
                print 'Green Cost1 is detected.'
                g1 = gcost1
            elif r.getIndex() == 1:
                print 'Green Cost2 is detected.'
                g2 = gcost2
            elif r.getIndex() == 2:
                print 'Green Cost3 is detected.'
                g3 = gcost3
            elif r.getIndex() == 3:
                print 'Green Cost4 is detected.'
                g4 = gcost4
            elif r.getIndex() == 4:
                print 'Green Cost5 is detected.'
                g5 = gcost5
            elif r.getIndex() == 5:
                print 'Green Cost7 is detected.'
                g7 = gcost7

        if g7 != None and availableMana >= 7:
            summon_creature = g7
            availableMana-=7
        elif g5 != None and availableMana >= 5:
            summon_creature = g5
            availableMana-=5
        elif g4 != None and availableMana >= 4:
            summon_creature = g4
            availableMana-=4
        elif g2 != None and availableMana >= 2:
            summon_creature = g2
            availableMana-=2
        elif g1 != None and availableMana >= 1:
            summon_creature = g1
            availableMana-=1
        elif g3 != None and availableMana >= 3:
            summon_creature = g3
            availableMana-=3
        else:
            break
        try:
            click(summon_creature)
        except:
            continue
        wait(0.5)
        type("f")
        wait(0.5)

def SummonBasic(currentMana):
    print 'SummonBasic'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    count = 0
    for num in range(10):
        count += 1
        summon_creature = None
        res = findAny(gcost2,gcost3,gcost5,gcost7,wcost2,wcost4,wcost6)
        g2 = None
        g3 = None
        g5 = None
        g7 = None
        w2 = None
        w4 = None
        w6 = None
        for r in res:
            if r.getIndex() == 0:
                print 'Green Cost2 is detected.'
                g2 = gcost2
            elif r.getIndex() == 1:
                print 'Green Cost3 is detected.'
                g3 = gcost3
            elif r.getIndex() == 2:
                print 'Green Cost5 is detected.'
                g5 = gcost5
            elif r.getIndex() == 3:
                print 'Green Cost7 is detected.'
                g7 = gcost7
            elif r.getIndex() == 4:
                print 'White Cost2 is detected.'
                w2 = wcost2
            elif r.getIndex() == 5:
                print 'White Cost4 is detected.'
                w4 = wcost4
            elif r.getIndex() == 6:
                print 'White Cost6 is detected.'
                w6 = wcost6

        if g7 != None and availableMana >= 7:
            print 'Summon Green Cost7.'
            summon_creature = g7
            availableMana-=7
        elif w6 != None and availableMana >= 6:
            print 'Summon White Cost6.'
            summon_creature = w6
            availableMana-=6
        elif g5 != None and availableMana >= 5:
            print 'Summon Green Cost5.'
            summon_creature = g5
            availableMana-=5
        elif g3 != None and availableMana >= 3:
            print 'Summon Green Cost3.'
            summon_creature = g3
            availableMana-=2
        elif g2 != None and availableMana >= 2:
            print 'Summon Green Cost2.'
            summon_creature = g2
            availableMana-=1
        elif w2 != None and availableMana >= 2:
            print 'Summon White Cost2.'
            summon_creature = w2
            availableMana-=2
        elif w4 != None and availableMana >= 4:
            print 'Summon White Cost4.'
            summon_creature = w4
            availableMana-=4
        else:
            print 'Couldnt find a summonable creature. Break loop.'
            break
        try:
            click(summon_creature)
        except:
            continue
        wait(1)
        type("f")
        if exists("1597466883152.png", 2) != None:
            try:
                click("1597466883152.png")
                wait(1)
                click("1597466883152.png")
            except:
                print "failed to click"
        count = 0
        
def SummonKuwakiri(currentMana):
    print 'SummonKuwakiri'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    for num in range(10):
        summon_creature = None
        res = findAny(gcost1,gcost2,gcost3,gcost4,gcost5,gcost7)
        g1 = None
        g2 = None
        g3 = None
        g4 = None
        g5 = None
        g7 = None
        for r in res:
            if r.getIndex() == 0:
                print 'Green Cost1 is detected.'
                g1 = gcost1
            elif r.getIndex() == 1:
                print 'Green Cost2 is detected.'
                g2 = gcost2
            elif r.getIndex() == 2:
                print 'Green Cost3 is detected.'
                g3 = gcost3
            elif r.getIndex() == 3:
                print 'Green Cost4 is detected.'
                g4 = gcost4
            elif r.getIndex() == 4:
                print 'Green Cost5 is detected.'
                g5 = gcost5
            elif r.getIndex() == 5:
                print 'Green Cost7 is detected.'
                g7 = gcost7

        if g7 != None and availableMana >= 7:
            summon_creature = g7
            availableMana-=7
        elif g4 != None and availableMana >= 4:
            summon_creature = g4
            availableMana-=4
        elif g2 != None and availableMana >= 2:
            summon_creature = g2
            availableMana-=2
        elif g1 != None and availableMana >= 1:
            summon_creature = g1
            availableMana-=1
        elif g3 != None and availableMana >= 3:
            summon_creature = g3
            availableMana-=3
        elif g5 != None and availableMana >= 5:
            summon_creature = g5
            availableMana-=5
        else:
            break
        try:
            click(summon_creature)
        except:
            continue
        wait(0.5)
        type("f")
        wait(0.5)

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
            click(summon_creature)
        except:
            continue
        wait(0.5)
        type("f")
        wait(0.5)

def SummonF30(currentMana):
    print 'SummonF30'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    for num in range(10):
        print "checking summon..." + str(num)
        summon_creature = None
        r2 = findAny(rcost2)
        r3 = findAny(rcost3)
        r4 = findAny(rcost4)
        r5 = findAny(rcost5)
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
        elif availableMana == 4:
            if existsBlocker() == True and len(k4) > 0:
                summon_creature = k4
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
            elif len(r4) > 0:
                summon_creature = r4
                availableMana-=4
            elif len(k4) > 0:
                summon_creature = k4
                availableMana-=4
            else:
                break
        elif availableMana >= 5:
            if existsBlocker() == True and len(k4) > 0:
                summon_creature = k4
                availableMana-=4 
            elif existsBlocker() == True and len(r5) > 0:
                summon_creature = r5
                availableMana-=5
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
            elif len(r4) > 0:
                summon_creature = r4
                availableMana-=4
            elif len(k4) > 0:
                summon_creature = k4
                availableMana-=4
            elif len(r5) > 0:
                summon_creature = r5
                availableMana-=5
            else:
                break
        else:
            break
        try:
            click(summon_creature)
        except:
            continue
        wait(0.5)
        type("f")
        if exists("1599116790793.png",2) != None:
            res = findAny(Pattern("1599114153262.png").similar(0.85).targetOffset(1,47),Pattern("1599114546868.png").similar(0.85).targetOffset(-5,46),Pattern("1599114574848.png").similar(0.84).targetOffset(3,47),Pattern("1599116916920.png").similar(0.85).targetOffset(1,51))
            click(res[0])
            click("1599116995128.png")
        

#手札の情報を取得する。
#TODO:現状緑の1-5コスト、白の6コストのみ対象
#return : 手札情報の配列
def getHandInfo():
    print 'getHandInfo'
    handInfo = []
    targetImages = [gcost1,gcost2,gcost3,gcost4,gcost5,gcost7,wcost2,wcost4,wcost6]

    DMApp = App(EnvSettings.AppPath)
    region_of_DMApp = DMApp.window()
    f = Finder(SCREEN.capture(region_of_DMApp))
    
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
#緑1-5、白6のみ対応ずみ
def ChargeMana(DMApp):
    print 'ChargeMana'
    #マナ取得
    mana = getManaNumBeforeCharge()
    print 'ManaZone(Before charge):' + str(mana)
    hand = getHandSum(getHandInfo())
    print 'Hand:' + str(hand)
    wResult = findAny(Pattern("1595071897888-2.png").similar(0.85).targetOffset(43,49),Pattern("1596874764898.png").similar(0.90))
    if len(wResult) > 0 and mana > 0:
        Hand = wResult
    else:
        #マナ0-2
        #　チャージ　大きい順にチャージ
        if mana >= 0 and mana <=2:
            Hand = findAny(Pattern("1595029444929-2.png").similar(0.90).targetOffset(67,55),Pattern("1594949422218-2.png").similar(0.83).targetOffset(69,54),Pattern("1595030120503-2.png").similar(0.90).targetOffset(75,56),Pattern("1596192523218.png").similar(0.90).targetOffset(61,49),Pattern("1594950595616-2.png").similar(0.85).targetOffset(62,48),Pattern("1595030130228-2.png").similar(0.90).targetOffset(47,46),)
        #マナ3
        #　チャージ　4以外を優先
        elif mana == 3:
            Hand = findAny(Pattern("1595029444929-2.png").similar(0.90).targetOffset(63,50),Pattern("1596192523218.png").similar(0.90).targetOffset(61,53),Pattern("1595030120503-2.png").similar(0.90).targetOffset(75,56),Pattern("1594950595616-2.png").similar(0.85).targetOffset(62,48),Pattern("1595030130228-2.png").similar(0.90).targetOffset(51,38),Pattern("1594949422218-2.png").similar(0.83).targetOffset(69,44))
        #マナ4
        #　手札が3枚以上ならチャージ
        elif mana >= 4 and hand >= 3:
            Hand = findAny(Pattern("1595029444929-2.png").similar(0.90).targetOffset(64,50),Pattern("1594949422218-2.png").similar(0.83).targetOffset(69,44),Pattern("1594950595616-2.png").similar(0.85).targetOffset(62,48),Pattern("1595030130228-2.png").similar(0.90).targetOffset(50,41),Pattern("1596192523218.png").similar(0.90).targetOffset(58,48),Pattern("1595030120503-2.png").similar(0.90).targetOffset(75,56))
        else:
            return mana
    if len(Hand) > 0:         
        click(Hand[0])
        wait(1)
        type("d")
        wait(1)
    return mana + 1

def ChargeManaBasic():
    print 'ChargeManaBasic'
    #マナ取得
    mana = getManaNumBeforeCharge()
    print 'ManaZone(Before charge):' + str(mana)
    hand = getHandSum(getHandInfo())
    print 'Hand:' + str(hand)
    wResult = findAny(wcost4,wcost6,wcost2)
    if len(wResult) > 0 and mana == 0:
        Hand = wResult
    else:
        #マナ0-2
        #　チャージ　大きい順にチャージ
        if mana >= 0 and mana <=3:
            Hand = findAny(gcost5,wcost4,gcost7,wcost6,gcost3,wcost2,gcost2)
        elif mana >= 4 and mana <= 5:
            Hand = findAny(wcost4,gcost5,gcost7,gcost3,wcost2,gcost2,wcost6)
        #　手札が3枚以上ならチャージ
        elif mana >= 5 and mana <= 6 and hand >= 3:
            Hand = findAny(wcost4,gcost3,gcost5,wcost2,gcost2,gcost7,wcost6)
        #elif mana >= 7 and hand >= 3:
        #    Hand = findAny(gcost5,wcost4,gcost3,wcost2,gcost2,gcost7,wcost6)
        else:
            return mana
    if len(Hand) > 0:         
        click(Hand[0])
        wait(1)
        type("d")
        wait(2)
    return mana + 1

def ChargeManaKuwakiri(DMApp):
    print 'ChargeManaKuwakiri'
    #マナ取得
    mana = getManaNumBeforeCharge()
    print 'ManaZone(Before charge):' + str(mana)
    hand = getHandSum(getHandInfo())
    print 'Hand:' + str(hand)
    wResult = findAny(Pattern("1595071897888-2.png").similar(0.85).targetOffset(43,49),Pattern("1596874764898.png").similar(0.90))
    if len(wResult) > 0 and mana > 0:
        Hand = wResult
    else:
        #マナ0-2
        #　チャージ　大きい順にチャージ
        if mana >= 0 and mana <=2:
            Hand = findAny(Pattern("1595029444929-2.png").similar(0.90).targetOffset(67,55),Pattern("1595030120503-2.png").similar(0.90).targetOffset(75,56),Pattern("1596192523218.png").similar(0.90).targetOffset(61,49),Pattern("1594949422218-2.png").similar(0.83).targetOffset(69,54),Pattern("1594950595616-2.png").similar(0.85).targetOffset(62,48),Pattern("1595030130228-2.png").similar(0.90).targetOffset(47,46),)
        #マナ3
        #　チャージ　4以外を優先
        elif mana == 3:
            Hand = findAny(Pattern("1595029444929-2.png").similar(0.90).targetOffset(63,50),Pattern("1596192523218.png").similar(0.90).targetOffset(61,53),Pattern("1595030120503-2.png").similar(0.90).targetOffset(75,56),Pattern("1594950595616-2.png").similar(0.85).targetOffset(62,48),Pattern("1595030130228-2.png").similar(0.90).targetOffset(51,38),Pattern("1594949422218-2.png").similar(0.83).targetOffset(69,44))
        #マナ4
        #　手札が3枚以上ならチャージ
        elif mana >= 4 and hand >= 3:
            Hand = findAny(Pattern("1595029444929-2.png").similar(0.90).targetOffset(64,50),Pattern("1594950595616-2.png").similar(0.85).targetOffset(62,48),Pattern("1595030130228-2.png").similar(0.90).targetOffset(50,41),Pattern("1596192523218.png").similar(0.90).targetOffset(58,48),Pattern("1595030120503-2.png").similar(0.90).targetOffset(75,56),Pattern("1594949422218-2.png").similar(0.83).targetOffset(69,44))
        else:
            return mana
    if len(Hand) > 0:         
        click(Hand[0])
        wait(1)
        type("d")
        wait(1)
    return mana + 1

def ChargeManaRedBlack():
    print 'ChargeManaRedBlack'
    #マナ取得
    mana = getManaNumBeforeCharge()
    print 'ManaZone(Before charge):' + str(mana)
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
        click(Hand[0])
        wait(1)
        type("d")
        wait(1)
    return mana + 1

def ChargeManaF30(DMApp):
    print 'ChargeManaF30'
    #マナ取得
    mana = getManaNumBeforeCharge()
    print 'ManaZone(Before charge):' + str(mana)
    hand = getHandSum(getHandInfo())
    print 'Hand:' + str(hand)
    #　チャージ
    if mana == 0:
        Hand = findAny(rcost5,rcost4,rcost3,rcost2,kcost4,kcost3,kcost2)
    elif mana == 1:
        Hand = findAny(kcost4,kcost3,rcost5,rcost4,rcost3,rcost2,kcost2)
    elif mana >= 2 and mana <=4:
        Hand = findAny(rcost3,kcost3,rcost4,rcost2,kcost2,rcost5,kcost4,)
    elif mana >= 5 and hand >= 3:
        Hand = findAny(rcost3,kcost3,rcost2,kcost2,rcost5,kcost4,rcost4)
    else:
        return mana
    if len(Hand) > 0:         
        click(Hand[0])
        wait(1)
        type("d")
        wait(1)
    return mana + 1

#シールド数を取得する。
#追加シールド(黄色)も対応済み
def getSheildObj(DMApp, img):
    handInfo = []
    targetImage = img

    region_of_DMApp = DMApp.window()
    f = Finder(SCREEN.capture(region_of_DMApp))
    f.findAll(targetImage)
    result = []
    while f.hasNext():
       result.append(f.next())
    return result

#バトルゾーンのクリーチャーで相手プレーヤーを攻撃する。
#U/UC/R/ダボラッシュに対応済み
#TODO:VR/SRのアタックに対応する。
#TODO:シールドトリガー発生時のクリーチャー選択、手札選択に対応する。
def directAttack():
    print 'directAttack'
    for num in range(3):
        print "checking W breaker...." + str(num)
        BZ = findAny(Pattern("1597610313690.png").similar(0.80).targetOffset(-53,30))
        if len(BZ) > 0:
            try:
                CommonDMLib.dragDropAtSpeed(BZ[0],Pattern("1594957113274.png").targetOffset(-371,82),1)

                if exists("1597065134484.png", 5) != None:
                    click(Pattern("1594948424162.png").targetOffset(-170,-387))
                    click(Pattern("1594948424162.png").targetOffset(185,-379))
                    click("1594948424162.png")
                wait(2)
            except:
                Settings.MoveMouseDelay = 0.1
                break
        else:
            break
    for num in range(7):
        print "checking Single breaker...." + str(num)
        BZ = findAny(Pattern("1594978601821.png").similar(0.97).targetOffset(1,63))#Pattern("1595034893803.png").similar(0.90).targetOffset(-1,55)Pattern("1595048461315.png").similar(0.97).targetOffset(0,32)
        if len(BZ) > 0:
            try:
                CommonDMLib.dragDropAtSpeed(BZ[0],Pattern("1594957113274.png").targetOffset(-371,82),1)

                if exists("1597065134484.png", 2) != None:
                    click(Pattern("1594948424162.png").targetOffset(-170,-387))
                    click(Pattern("1594948424162.png").targetOffset(185,-379))
                    click("1594948424162.png")
                wait(2)
            except:
                Settings.MoveMouseDelay = 0.1
                break
        else:
            break

def directAttackAvoidingBlocker(DMApp, sheildImg):
    print 'directAttackAvoidingBlocker'
    for num in range(3):
        print "checking W breaker...." + str(num)
        BZ = findAny(Pattern("1597610313690.png").similar(0.80).targetOffset(-53,30))
        if len(BZ) > 0:
            try:
                Settings.MoveMouseDelay = 1
                dragDrop(BZ[0],Pattern("1594957113274.png").targetOffset(-371,82))
                Settings.MoveMouseDelay = 0.1

                if exists("1597065134484.png", 5) != None:
                    click(Pattern("1594948424162.png").targetOffset(-170,-387))
                    click(Pattern("1594948424162.png").targetOffset(185,-379))
                    click("1594948424162.png")
                wait(2)
            except:
                Settings.MoveMouseDelay = 0.1
                break
        else:
            break
        
    if existsBlocker() == True:
        return
    
    for num in range(7):
        print "checking Single breaker...." + str(num)
        BZ = findAny(Pattern("1595048461315.png").similar(0.97).targetOffset(0,32),Pattern("1594978601821.png").similar(0.97).targetOffset(1,63))#Pattern("1595034893803.png").similar(0.90).targetOffset(-1,55)
        if len(BZ) > 0:
            try:
                Settings.MoveMouseDelay = 1
                dragDrop(BZ[0],Pattern("1594957113274.png").targetOffset(-371,82))
                Settings.MoveMouseDelay = 0.1

                if exists("1597065134484.png", 2) != None:
                    click(Pattern("1594948424162.png").targetOffset(-170,-387))
                    click(Pattern("1594948424162.png").targetOffset(185,-379))
                    click("1594948424162.png")
                wait(2)
            except:
                Settings.MoveMouseDelay = 0.1
                break
        else:
            break

def retire():
    type(Key.ESC)
    if exists("1595621916162.png", 1) != None:
        try:
            click("1595621916162.png")
        except:
            print "failed to click OK"


TurnEnd = Pattern("1594954855862.png").similar(0.84)
TurnEndMustAttack = Pattern("1594955483430.png").similar(0.85)
smallStartBattle = Pattern("1594949925094.png").similar(0.80)
Retry = "1594985735128.png"
ShieldTrigger = Pattern("1594949527193.png").similar(0.94).targetOffset(195,5)
CheckShield = Pattern("CheckShield.png").similar(0.88)
SelectCreature = Pattern("1594952630070.png").similar(0.95).targetOffset(-20,-217)
Hand = Pattern("1595035924385.png").similar(0.85)
DateChanged = Pattern("1596758627672.png").similar(0.90)
BLOCK_QUESTION1 = Pattern("Block.png").similar(0.86)
BLOCK_QUESTION2 = Pattern("BLOCK_QUESTION2.png").similar(0.90)
BLOCK = "1597156569299.png"
NOBLOCK = Pattern("1597133736767.png").similar(0.89)
TAP_QUESTION = Pattern("TAP_QUESTION.png").similar(0.90)
DEST_QUESTION = Pattern("DES_QUESTION.png").similar(0.90)

#ゲーム中のイレギュラーの処理
#return 0 ゲームの正常終了
#return 1 ゲーム継続
def irregularLoop():
    print 'irregularLoop'
#  イレギュラーループ
    for enemyturn_loop in range(50):
        print 'This is ' + str(enemyturn_loop) + ' times loop.'
        
        #   自分のターンを検知
        if len(findAny(TurnEnd,TurnEndMustAttack)) > 0:
            print 'My Turn is detected.'
            wait(3)
            break
        #   トリガー発動 
        if len(findAny(ShieldTrigger)) > 0:
            print 'My ST is triggered.'
            click(ShieldTrigger)
            wait(0.5)
        #   シールド確認
        if len(findAny(CheckShield))   > 0:
            print 'My sheild is broken.'
            click("1597465916311.png")
            wait(0.5)
        if len(findAny(TAP_QUESTION))   > 0:
            print 'Tap.'          
            BZ = None
            for num in range(5):
                BZ = findAny(Pattern("1597464166732.png").similar(0.85).targetOffset(0,51))
                if len(BZ) > 0: 
                    click(BZ[0])
                    break
                wait(0.5)
            click("1597464206941.png")
            if exists("1597464225195.png",5) != None:
                click("1597464245892.png")
            wait(0.5)
        if len(findAny(DEST_QUESTION))   > 0:
            print 'Dest.'          
            BZ = None
            for num in range(5):
                BZ = findAny(Pattern("1601365170781.png").similar(0.85).targetOffset(-1,50),Pattern("1597464166732.png").similar(0.85).targetOffset(0,51), Pattern("1598791717218.png").similar(0.85))
                if len(BZ) > 0: 
                    click(BZ[0])
                    break
                wait(0.5)
            click("1597464206941.png")
            wait(0.5)
        if len(findAny(BLOCK_QUESTION1)) > 0 or len(findAny(BLOCK_QUESTION2)) > 0:
            print 'Block?'
            if len(findAny(Pattern("1597156496305.png").similar(0.80))) > 0:
                click(Pattern("1597156496305.png").similar(0.80).targetOffset(-7,58))
                click(BLOCK)
            else:
                click(NOBLOCK)
            wait(1)
        #   対戦開始を検知→ゲームループをbreak
        if len(findAny(smallStartBattle)) > 0:
            print 'Game has Finished.'
            return 0
        if len(findAny(Retry)) > 0:
            #game_loopを終了する。
            click(Retry)
        #死の宣告、デスモーリー等
        if len(findAny(SelectCreature)) > 0:
            for chooseCreatureLoop in range(10):
                print 'Player need to select his creature.'                       
                BZ = findAny(Pattern("1595121206331.png").similar(0.95).targetOffset(13,41),Pattern("1595121260947.png").similar(0.90).targetOffset(5,35),Pattern("1598096217499.png").similar(0.90).targetOffset(1,64),Pattern("1598254898927.png").similar(0.90).targetOffset(3,60))
                if len(BZ) > 0: 
                    click(BZ[0])
                    click("1594951143014.png")
                    break
                wait(0.5)
        #デモニックバイス
        if len(findAny(Hand)) > 0:
            print 'Player need to select his hands.'
            click(Pattern("1595035924385.png").targetOffset(363,188))
            click(Pattern("1595035924385.png").targetOffset(174,190))
            click("1595035999600.png")
            wait(1)

        #日付変更
        if len(findAny(DateChanged)) > 0:
            raise Exception
        
        if  enemyturn_loop == 49:
            print 'Irregular loop is over 50. Restart is necessary.'
            raise Exception
    
    return 1

def irregularLoopForSP():
    print 'irregularLoopForSP'
#  イレギュラーループ
    for enemyturn_loop in range(50):
        print 'This is ' + str(enemyturn_loop) + ' times loop.'
        
        #   自分のターンを検知
        if len(findAny(TurnEnd)) > 0:
            print 'My Turn is detected.'
            break
        #   トリガー発動 
        if len(findAny(ShieldTrigger)) > 0:
            print 'My ST is triggered.'
            click(Pattern("1594949527193.png").similar(0.94).targetOffset(-170,3))
            wait(0.1)
            continue
        #   シールド確認
        if len(findAny(CheckShield))   > 0:
            print 'My sheild is broken.'
            click("1597465916311.png")
            wait(0.1)
            continue
        #   対戦開始を検知→ゲームループをbreak
        if len(findAny(smallStartBattle)) > 0:
            print 'Game has Finished.'
            return 0
        
        if  enemyturn_loop == 49:
            print 'Irregular loop is over 50. Restart is necessary.'
            raise Exception
    
    return 1