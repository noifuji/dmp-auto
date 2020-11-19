# -*- coding: utf-8 -*-
from sikuli import *
import sys
import traceback
import random
from datetime import datetime

sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import DMLib
import NoxDMLib
import CommonDMLib
import AndAppResources

def turnEnd(resources):
    if resources.APP_ENGINE == "NOX":
        click(Pattern("1597036183485.png").similar(0.85).targetOffset(-100,206))
    elif resources.APP_ENGINE == "ANDAPP":
        keyDown(Key.SHIFT)
        type(Key.ENTER)
        keyUp(Key.SHIFT)

def charge(resources, target):
    if resources.APP_ENGINE == "NOX":
        CommonDMLib.dragDropAtSpeed(target, resources.TARGET_POSITION_CHARGE, 2)
    elif resources.APP_ENGINE == "ANDAPP":
        click(target)
        wait(1)
        type("d")
        wait(2)
        
def summon(resources, target):
    if resources.APP_ENGINE == "NOX":
        CommonDMLib.dragDropAtSpeed(target, resources.TARGET_POSITION_SUMMON, 1.2)
    elif resources.APP_ENGINE == "ANDAPP":
        click(target)
        wait(1)
        type("f")
        wait(0.5)

def getHandCount(resources, cards):
    print 'getHandInfo'
    f = Finder(SCREEN.capture(App.focusedWindow()))
    count = 0
    f.findAll(resources.ICON_CARD_SQUARE)
    while f.hasNext():
       count += 1
       f.next()
    return count

def getManaNumBeforeCharge(resources):
    print 'getManaNumBeforeCharge'
    targetImages = resources.MANA_ICONS
    res = findAny(targetImages)
    if len(res) > 0:
        return res[0].getIndex()
    else:
        return 7

def countEnemyBlockers(resources):
    if resources.APP_ENGINE == "NOX":
        OFFSETX = -1000
        OFFSETY = 210
        WIDTH = 1270
        HEIGHT = 100
    elif resources.APP_ENGINE == "ANDAPP":
        OFFSETX = -780
        OFFSETY = 200
        WIDTH = 1000
        HEIGHT = 70
    else:
        raise Exception()
    res = findAny(resources.ICON_ENEMY_CARD_COUNT)
    if len(res) == 0:
        return
    cardListRegion = Region(res[0].getX()+OFFSETX,res[0]. getY()+OFFSETY,WIDTH,HEIGHT)
    cardListRegion.highlight(0.1)
    f = Finder(SCREEN.capture(cardListRegion))
    f.findAll(resources.ICON_ENEMY_UNTAPPED_BLOCKER)
    count = 0
    while f.hasNext():
        f.next()
        count += 1
    return count

def countMyBattleZone(resources, targetImage):
    if resources.APP_ENGINE == "NOX":
        OFFSETX = -1000
        OFFSETY = 400
        WIDTH = 1270
        HEIGHT = 150
    elif resources.APP_ENGINE == "ANDAPP":
        OFFSETX = -780
        OFFSETY = 335
        WIDTH = 1000
        HEIGHT = 110
    else:
        raise Exception()
    res = findAny(resources.ICON_ENEMY_CARD_COUNT)
    if len(res) == 0:
        return
    cardListRegion = Region(res[0].getX()+OFFSETX,res[0]. getY()+OFFSETY,WIDTH,HEIGHT)
    cardListRegion.highlight(0.1)
    f = Finder(SCREEN.capture(cardListRegion))
    f.findAll(targetImage)
    count = 0
    while f.hasNext():
        f.next()
        count += 1
    return count

def countEnemyCemetry(resources):
    std = findAny(resources.ICON_ENEMY_CARD_COUNT)
    if len(std) == 0:
        return
    click(Location(std[0].getX()-1090, std[0].getY()+230))
    exists(resources.TITLE_ENEMY_CEMETRY, 10)
    
    res = findAny(resources.TITLE_ENEMY_CEMETRY)
    if len(res) == 0:
        return
    cemetryRegion = Region(res[0].getX()+90, res[0].getY()+130, 1250, 600)
    cemetryRegion.highlight(0.1)
    f = Finder(SCREEN.capture(cemetryRegion))
    f.findAll(resources.ICON_CREATURE_CARD)
    count = 0
    while f.hasNext():
        c = f.next()
        count += 1

    click(resources.BUTTON_OK2)
    waitVanish(resources.BUTTON_OK2, 10)
    print count
    
    return count

                        
def countEnemyShields(resources):
    if resources.APP_ENGINE == "NOX":
        OFFSETX = -470
        OFFSETY = 100
    elif resources.APP_ENGINE == "ANDAPP":
        OFFSETX = -400
        OFFSETY = 90
    else:
        raise Exception()
    res = findAny(resources.ICON_ENEMY_CARD_COUNT)
    if len(res) == 0:
        return
    click(Location(res[0].getX()+OFFSETX, res[0].getY()+OFFSETY))
    wait(2)
    result = findBestList([
                resources.ICON_SHIELD_COUNT0,
                resources.ICON_SHIELD_COUNT1,
                resources.ICON_SHIELD_COUNT2,
                resources.ICON_SHIELD_COUNT3,
                resources.ICON_SHIELD_COUNT4,
                resources.ICON_SHIELD_COUNT5
                ])
    if result == None:
        count = 5
    else:
        count = result.getIndex()

    click(resources.BUTTON_OK2)
    waitVanish(resources.BUTTON_OK2, 5)
    return count

def getManaColor(resources):
    results = findAny(
            resources.ICON_MANA_WHITE
            ,resources.ICON_MANA_BLUE
            ,resources.ICON_MANA_BLACK
            ,resources.ICON_MANA_RED
            ,resources.ICON_MANA_GREEN)
    manaColors = {"WHITE" : False, "BLUE" : False,
            "BLACK" : False, "RED" : False,
            "GREEN" : False}
    for res in results:
        if res.getIndex() == 0:
            manaColors["WHITE"] = True
        elif res.getIndex() == 1:
            manaColors["BLUE"] = True
        elif res.getIndex() == 2:
            manaColors["BLACK"] = True
        elif res.getIndex() == 3:
            manaColors["RED"] = True
        elif res.getIndex() == 4:
            manaColors["GREEN"] = True
    return manaColors

def solveEffect(resources):
    exists(resources.ICON_NOT_SELECTED, 2)
    if len(findAny(resources.MESSAGE_TAP)) > 0 or \
        len(findAny(resources.MESSAGE_DEST))   > 0 or \
        len(findAny(resources.MESSAGE_EFFECT)) > 0 or \
        len(findAny(resources.MESSAGE_MANA))   > 0 or \
        len(findAny(resources.MESSAGE_SELECT))   > 0 or \
        len(findAny(resources.MESSAGE_BOUNCE))   > 0:
        print 'Tap, Dest, Mana, Bounce'
        BZ = findAny(
                resources.ICON_ENEMY_UNTAPPED_BLOCKER,
                resources.ICON_MY_CREATURE1,
                resources.ICON_MY_CREATURE2,
                resources.ICON_MY_CREATURE3,
                resources.ICON_MY_CREATURE4,
                resources.ICON_ENEMY_CREATURE1,
                resources.ICON_ENEMY_CREATURE2,
                resources.ICON_ENEMY_CREATURE3,
                resources.ICON_ENEMY_CREATURE4,
                resources.ICON_ENEMY_CREATURE5)
        for b in BZ:
            click(b)
            wait(0.5)
            if exists(resources.ICON_SELECTED, 1) != None:
                try:
                    click(resources.BUTTON_OK4)
                except:
                    print "failed to click"
                break
        if len(findAny(resources.ICON_SELECTED)) > 0:
            try:
                click(resources.BUTTON_OK4)
            except:
                print "failed to click"
        wait(0.5)
        if exists(resources.MESSAGE_NO_CREATURE_SELECTED,5) != None:
            click(resources.BUTTON_OK2)
        wait(0.5)

def ChargeManaBasic(resources):
    print 'ChargeManaBasic'
    #マナ取得
    mana = getManaNumBeforeCharge(resources)
    print 'ManaZone(Before charge):' + str(mana)
    hand = getHandCount(resources, [
                resources.ICON_COST_GREEN_5,resources.ICON_COST_WHITE_4,
                resources.ICON_COST_GREEN_7,resources.ICON_COST_WHITE_6,
                resources.ICON_COST_GREEN_3,resources.ICON_COST_WHITE_2,
                resources.ICON_COST_GREEN_2])
    print 'Hand:' + str(hand)
    #マナ0-2
    #　チャージ　大きい順にチャージ
    if mana == 0:
        Hand = findAny(
                resources.ICON_COST_WHITE_4,resources.ICON_COST_WHITE_6,
                resources.ICON_COST_WHITE_2,resources.ICON_COST_GREEN_5,                
                resources.ICON_COST_GREEN_7,resources.ICON_COST_GREEN_3,
                resources.ICON_COST_GREEN_2)
    elif mana > 0 and mana <=3:
        Hand = findAny(
                resources.ICON_COST_GREEN_5,resources.ICON_COST_WHITE_4,
                resources.ICON_COST_GREEN_7,resources.ICON_COST_WHITE_6,
                resources.ICON_COST_GREEN_3,resources.ICON_COST_WHITE_2,
                resources.ICON_COST_GREEN_2)
    elif mana >= 4 and mana <= 5:
        Hand = findAny(
                resources.ICON_COST_WHITE_4,resources.ICON_COST_GREEN_5,
                resources.ICON_COST_GREEN_7,resources.ICON_COST_GREEN_3,
                resources.ICON_COST_WHITE_2,resources.ICON_COST_GREEN_2,
                resources.ICON_COST_WHITE_6)
    #　手札が3枚以上ならチャージ
    elif mana >= 5 and mana <= 6 and hand >= 3:
        Hand = findAny(
                resources.ICON_COST_WHITE_4,resources.ICON_COST_GREEN_3,
                resources.ICON_COST_GREEN_5,resources.ICON_COST_WHITE_2,
                resources.ICON_COST_GREEN_2,resources.ICON_COST_GREEN_7,
                resources.ICON_COST_WHITE_6)
    else:
        return mana
    
    if len(Hand) > 0:         
        charge(resources,Hand[0])
        mana += 1
    return mana

def ChargeManaRedBlack(resources):
    print 'ChargeManaRedBlack'
    #マナ取得
    mana = getManaNumBeforeCharge(resources)
    print 'ManaZone(Before charge):' + str(mana)
    #　チャージ
    if mana == 0:
        Hand = findAny(
                resources.ICON_COST_RED_5,resources.ICON_COST_RED_4,
                resources.ICON_COST_RED_3,resources.ICON_COST_RED_2,
                resources.ICON_COST_BLACK_4,resources.ICON_COST_BLACK_3,
                resources.ICON_COST_BLACK_2)
    elif mana == 1:
        Hand = findAny(
                resources.ICON_COST_BLACK_4,resources.ICON_COST_BLACK_3,resources.ICON_COST_BLACK_2,
                resources.ICON_COST_RED_5,resources.ICON_COST_RED_4,
                resources.ICON_COST_RED_3,resources.ICON_COST_RED_2)
    elif mana >= 2 and mana <=3:
        Hand = findAny(
                resources.ICON_COST_RED_5,resources.ICON_COST_BLACK_4,
                resources.ICON_COST_RED_3,resources.ICON_COST_BLACK_3,
                resources.ICON_COST_RED_4,resources.ICON_COST_RED_2,
                resources.ICON_COST_BLACK_2)
    elif mana >= 4:
        Hand = findAny(resources.ICON_COST_RED_5)
    else:
        return mana
    if len(Hand) > 0:         
        charge(resources,Hand[0])
        mana += 1
    return mana

def ChargeManaLarge(resources):
    print 'ChargeLarge'
    #マナ取得
    mana = getManaNumBeforeCharge(resources)
    print 'ManaZone(Before charge):' + str(mana)

    if mana >= 7:
        return mana

    #マナゾーンの色チェック
    for manaColorLoop in range(20):
        manaColors = getManaColor(resources)    
        print manaColors
        countTrue = 0
        for key in manaColors:
            if manaColors[key] == True:
                countTrue += 1
        if countTrue <= mana:
            break
    
    chargeTargets = []
    #未チャージの色を抽出
    if not manaColors["GREEN"]:
        chargeTargets.append(resources.ICON_COST_GREEN_7)
        chargeTargets.append(resources.ICON_COST_GREEN_3)
        chargeTargets.append(resources.ICON_COST_GREEN_2)
    if not manaColors["WHITE"]:
        chargeTargets.append(resources.ICON_COST_WHITE_4)
        chargeTargets.append(resources.ICON_COST_WHITE_7)
        chargeTargets.append(resources.ICON_COST_WHITE_6)
        chargeTargets.append(resources.ICON_COST_WHITE_1)
        chargeTargets.append(resources.ICON_COST_WHITE_2)
    #手札探索対象を作成
    Hand = findAnyList(chargeTargets)
    print "findAnyList result : " +  str(len(Hand))
    
    #　チャージ
    if len(Hand) == 0 and mana <= 6:
        if len(findAny(resources.ICON_MY_UNTAPPED_BLOCKER)) > 0:
            Hand = findAny(
                    resources.ICON_COST_GREEN_5,resources.ICON_COST_WHITE_3,
                    resources.ICON_COST_WHITE_4,resources.ICON_COST_WHITE_1,
                    resources.ICON_COST_WHITE_2,
                    resources.ICON_COST_GREEN_7,
                    resources.ICON_COST_WHITE_7,resources.ICON_COST_WHITE_6,
                    resources.ICON_COST_GREEN_3,
                    resources.ICON_COST_GREEN_2)
        else:
            Hand = findAny(
                    resources.ICON_COST_GREEN_5,resources.ICON_COST_WHITE_3,
                    resources.ICON_COST_WHITE_4,
                    resources.ICON_COST_GREEN_3,
                    resources.ICON_COST_GREEN_2,resources.ICON_COST_GREEN_7,
                    resources.ICON_COST_WHITE_7,resources.ICON_COST_WHITE_6)
        
    if len(Hand) > 0:         
        charge(resources,Hand[0])
        mana += 1
        
    return mana

def ChargeManaFatty(resources):
    print 'ChargeManaFatty'
    #マナ取得
    mana = getManaNumBeforeCharge(resources)
    print 'ManaZone(Before charge):' + str(mana)
    hand = getHandCount(resources, [
                resources.ICON_COST_GREEN_5,resources.ICON_COST_WHITE_4,
                resources.ICON_COST_GREEN_7,resources.ICON_COST_WHITE_6,
                resources.ICON_COST_GREEN_3,resources.ICON_COST_WHITE_2,
                resources.ICON_COST_GREEN_2,resources.ICON_COST_WHITE_7,
                resources.ICON_COST_WHITE_1])
    print 'Hand:' + str(hand)
    #マナ0-2
    #　チャージ　大きい順にチャージ
    if mana == 0:
        Hand = findAny(
                resources.ICON_COST_WHITE_6,resources.ICON_COST_WHITE_4,
                resources.ICON_COST_WHITE_2,resources.ICON_COST_WHITE_1,
                resources.ICON_COST_GREEN_5,resources.ICON_COST_GREEN_3,
                resources.ICON_COST_GREEN_2)
    elif mana == 1:
        Hand = findAny(
                resources.ICON_COST_GREEN_5,resources.ICON_COST_GREEN_7,
                resources.ICON_COST_GREEN_3,resources.ICON_COST_GREEN_2,
                resources.ICON_COST_WHITE_1,resources.ICON_COST_WHITE_6,
                resources.ICON_COST_WHITE_4,resources.ICON_COST_WHITE_2)
    elif mana >= 2 and mana <= 3:
        Hand = findAny(
                resources.ICON_COST_GREEN_5,resources.ICON_COST_WHITE_1,
                resources.ICON_COST_WHITE_6,
                resources.ICON_COST_WHITE_4,resources.ICON_COST_WHITE_2,
                resources.ICON_COST_GREEN_2,resources.ICON_COST_GREEN_3,
                resources.ICON_COST_GREEN_7) 
    elif mana >= 4 and mana <= 5:
        Hand = findAny(
                resources.ICON_COST_GREEN_5,resources.ICON_COST_WHITE_1,
                resources.ICON_COST_WHITE_6,
                resources.ICON_COST_WHITE_4,resources.ICON_COST_WHITE_2,
                resources.ICON_COST_GREEN_2,resources.ICON_COST_GREEN_3,
                resources.ICON_COST_GREEN_7,) 
    #　手札が3枚以上ならチャージ
    elif mana == 6:
        Hand = findAny(
                resources.ICON_COST_GREEN_5,resources.ICON_COST_GREEN_3,
                resources.ICON_COST_GREEN_2,resources.ICON_COST_WHITE_4,
                resources.ICON_COST_WHITE_1,resources.ICON_COST_WHITE_2,
                resources.ICON_COST_WHITE_6,resources.ICON_COST_WHITE_7)
    else:
        return mana
    
    if len(Hand) > 0:         
        charge(resources,Hand[0])
        mana += 1
    return mana

def ChargeManaSpell(resources):
    print 'ChargeManaSpell'
    #マナ取得
    mana = getManaNumBeforeCharge(resources)
    print 'ManaZone(Before charge):' + str(mana)

    #マナゾーンの色チェック
    for manaColorLoop in range(20):
        manaColors = getManaColor(resources)    
        print manaColors
        countTrue = 0
        for key in manaColors:
            if manaColors[key] == True:
                countTrue += 1
        if countTrue <= mana:
            break
    
    chargeTargets = []
    #未チャージの色を抽出
    if not manaColors["RED"]:
        chargeTargets.append(resources.ICON_COST_RED_5)
        chargeTargets.append(resources.ICON_COST_RED_3)
    if not manaColors["BLACK"]:
        chargeTargets.append(resources.ICON_COST_BLACK_4)
        chargeTargets.append(resources.ICON_COST_BLACK_3)
    if not manaColors["GREEN"]:
        chargeTargets.append(resources.ICON_COST_GREEN_4)
        chargeTargets.append(resources.ICON_COST_GREEN_2)
    if not manaColors["WHITE"]:
        chargeTargets.append(resources.ICON_COST_WHITE_4)
        chargeTargets.append(resources.ICON_COST_WHITE_2)
    if not manaColors["BLUE"]:
        chargeTargets.append(resources.ICON_COST_BLUE_4)
        chargeTargets.append(resources.ICON_COST_BLUE_2)
    #手札探索対象を作成
    Hand = findAnyList(chargeTargets)
    print "findAnyList result : " +  str(len(Hand))
    #手札に無い場合は、全対象から確認
    if len(Hand) == 0 and mana <= 4:
        Hand = findAnyList(
                [
                    resources.ICON_COST_BLACK_4,resources.ICON_COST_WHITE_4,
                    resources.ICON_COST_BLUE_4,
                    resources.ICON_COST_GREEN_4,
                    resources.ICON_COST_BLUE_2,
                    resources.ICON_COST_WHITE_2,
                    resources.ICON_COST_GREEN_2,
                    resources.ICON_COST_RED_5,
                    resources.ICON_COST_RED_3,
                    resources.ICON_COST_BLACK_3])

        if len(Hand) == 0:
            return mana
    
    if len(Hand) > 0:         
        charge(resources,Hand[0])
        mana += 1
    return mana

def ChargeManaHakuho(resources):
    print 'ChargeManaHakuho'
    #マナ取得
    mana = getManaNumBeforeCharge(resources)
    print 'ManaZone(Before charge):' + str(mana)

    #マナゾーンの色チェック
    for retryLoop in range(10):
        manaColors = getManaColor(resources)
        print manaColors
        if manaColors["RED"] == False and manaColors["BLACK"] == False and mana >= 1:
            print "retry"
        elif (manaColors["RED"] == False or manaColors["BLACK"] == False) and mana >= 2:
            print "retry"
        else:
            break
            
    chargeTargets = []
    #未チャージの色を抽出
    if not manaColors["RED"]:
        chargeTargets.append(resources.ICON_COST_RED_4)
        chargeTargets.append(resources.ICON_COST_RED_3)
        chargeTargets.append(resources.ICON_COST_RED_2)
    if not manaColors["BLACK"]:
        chargeTargets.append(resources.ICON_COST_BLACK_4)
        chargeTargets.append(resources.ICON_COST_BLACK_2)
        chargeTargets.append(resources.ICON_COST_BLACK_3)
    #手札探索対象を作成
    Hand = findAnyList(chargeTargets)
    print "findAnyList result : " +  str(len(Hand))
    #手札に無い場合は、全対象から確認
    if len(Hand) == 0 and (mana <= 3 or (mana >= 4 and getHandCount(resources,[]) >= 3)):
        Hand = findAnyList(
                [
                    resources.ICON_COST_WHITE_6,
                    resources.ICON_COST_BLACK_4,
                    resources.ICON_COST_RED_4,
                    resources.ICON_COST_RED_3,
                    resources.ICON_COST_BLACK_2,
                    resources.ICON_COST_RED_2,
                    resources.ICON_COST_BLACK_3])

        if len(Hand) == 0:
            return mana
    
    if len(Hand) > 0:         
        charge(resources,Hand[0])
        mana += 1
    return mana

def SummonBasic(resources, currentMana):
    print 'SummonBasic'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    count = 0
    for num in range(10):
        summon_creature = None
        g2 = findAny(resources.ICON_COST_GREEN_2)
        g3 = findAny(resources.ICON_COST_GREEN_3)
        g5 = findAny(resources.ICON_COST_GREEN_5)
        g7 = findAny(resources.ICON_COST_GREEN_7)
        w2 = findAny(resources.ICON_COST_WHITE_2)
        w4 = findAny(resources.ICON_COST_WHITE_4)
        w6 = findAny(resources.ICON_COST_WHITE_6)

        if len(g7) > 0 and availableMana >= 7:
            print 'Summon Green Cost7.'
            summon_creature = g7[0]
            availableMana-=7
        elif len(w6) > 0  and availableMana >= 6:
            print 'Summon White Cost6.'
            summon_creature = w6[0]
            availableMana-=6
        elif len(g5) > 0  and availableMana >= 5:
            print 'Summon Green Cost5.'
            summon_creature = g5[0]
            availableMana-=5
        elif len(g3) > 0  and availableMana >= 3:
            print 'Summon Green Cost3.'
            summon_creature = g3[0]
            availableMana-=2
        elif len(g2) > 0  and availableMana >= 2:
            print 'Summon Green Cost2.'
            summon_creature = g2[0]
            availableMana-=2
        elif len(w2) > 0  and availableMana >= 2:
            print 'Summon White Cost2.'
            summon_creature = w2[0]
            availableMana-=2
        elif len(w4) > 0  and availableMana >= 4:
            print 'Summon White Cost4.'
            summon_creature = w4[0]
            availableMana-=4
        else:
            print 'Couldnt find a summonable creature. Break loop.'
            break
        
        try:
            summon(resources,summon_creature)
        except:
            Settings.MoveMouseDelay = 0.1
            break
        wait(2)
        if exists(resources.BUTTON_OK2, 2) != None:
            try:
                click(resources.BUTTON_OK2)
                wait(1)
                click(resources.BUTTON_OK2)
            except:
                print "failed to click"

def SummonRedBlack(resources, currentMana):
    print 'SummonRedBlack'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    for num in range(10):
        print "checking summon..." + str(num)
        summon_creature = None
        r2 = findAny(resources.ICON_COST_RED_2)
        r3 = findAny(resources.ICON_COST_RED_3)
        r4 = findAny(resources.ICON_COST_RED_4)
        k2 = findAny(resources.ICON_COST_BLACK_2)
        k3 = findAny(resources.ICON_COST_BLACK_3)
        k4 = findAny(resources.ICON_COST_BLACK_4)

        print "r2:" + str(len(r2)) + ",r3:" + str(len(r3)) + ",r4:" + str(len(r4)) + ",k2:" + str(len(k2)) + ",k3:" + str(len(k3)) + ",k4:" + str(len(k4))

        if availableMana == 2:
            if len(r2) > 0:
                summon_creature = r2[0]
                availableMana-=2
            elif len(k2) > 0:
                summon_creature = k2[0]
                availableMana-=2
            else:
                break
        elif availableMana == 3:
            if len(k3) > 0:
                summon_creature = k3[0]
                availableMana-=3
            elif len(r3) > 0:
                summon_creature = r3[0]
                availableMana-=3
            elif len(r2) > 0:
                summon_creature = r2[0]
                availableMana-=2
            elif len(k2) > 0:
                summon_creature = k2[0]
                availableMana-=2
            else:
                break
        elif availableMana >= 4:
            if len(r4) > 0:
                summon_creature = r4[0]
                availableMana-=4
            elif len(r2) > 0:
                summon_creature = r2[0]
                availableMana-=2
            elif len(k2) > 0:
                summon_creature = k2[0]
                availableMana-=2
            elif len(k3) > 0:
                summon_creature = k3[0]
                availableMana-=3
            elif len(r3) > 0:
                summon_creature = r3[0]
                availableMana-=3
            elif len(k4) > 0:
                summon_creature = k4[0]
                availableMana-=4
            else:
                break
        else:
            break
        try:
            summon(resources,summon_creature)
        except:
            Settings.MoveMouseDelay = 0.1
            break
        wait(2)

def SummonLarge(resources, currentMana):
    print 'SummonLarge'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    for num in range(5):
        summon_creature = None
        w1 = findAny(resources.ICON_COST_WHITE_1)
        w2 = findAny(resources.ICON_COST_WHITE_2)
        w6 = findAny(resources.ICON_COST_WHITE_6)
        w7 = findAny(resources.ICON_COST_WHITE_7)
        g2 = findAny(resources.ICON_COST_GREEN_2)
        g3 = findAny(resources.ICON_COST_GREEN_3)
        g7 = findAny(resources.ICON_COST_GREEN_7)
                
        if len(w2) > 0 and availableMana >= 2 and len(findAny(resources.ICON_MY_UNTAPPED_BLOCKER)) == 0:
            print 'Summon White Cost2'
            summon_creature = w2[0]
            availableMana-=2
        elif len(w1) > 0 and availableMana >= 1 and len(findAny(resources.ICON_MY_UNTAPPED_BLOCKER)) == 0:
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
            CommonDMLib.dragDropAtSpeed(summon_creature, resources.TARGET_POSITION_SUMMON, 1.2)
        except:
            Settings.MoveMouseDelay = 0.1
            break
        wait(1)

def SummonFatty(resources, currentMana):
    print 'SummonFatty'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    count = 0
    for num in range(10):
        summon_creature = None
        g2 = findAny(resources.ICON_COST_GREEN_2)
        g3 = findAny(resources.ICON_COST_GREEN_3)
        g5 = findAny(resources.ICON_COST_GREEN_5)
        g7 = findAny(resources.ICON_COST_GREEN_7)
        w1 = findAny(resources.ICON_COST_WHITE_1)
        w2 = findAny(resources.ICON_COST_WHITE_2)
        w4 = findAny(resources.ICON_COST_WHITE_4)
        w6 = findAny(resources.ICON_COST_WHITE_6)
        w7 = findAny(resources.ICON_COST_WHITE_7)

        if len(w7) > 0  and availableMana >= 7:
            print 'Summon White Cost7.'
            summon_creature = w7[0]
            availableMana-=7
        elif len(g7) > 0 and availableMana >= 7:
            print 'Summon Green Cost7.'
            summon_creature = g7[0]
            availableMana-=7
        elif len(w2) > 0  and availableMana >= 2:
            print 'Summon White Cost2.'
            summon_creature = w2[0]
            availableMana-=2
        elif len(g3) > 0  and availableMana >= 3:
            print 'Summon Green Cost3.'
            summon_creature = g3[0]
            availableMana-=2
        elif len(g2) > 0  and availableMana >= 2:
            print 'Summon Green Cost2.'
            summon_creature = g2[0]
            availableMana-=1
        elif len(w4) > 0  and availableMana >= 4:
            print 'Summon White Cost4.'
            summon_creature = w4[0]
            availableMana-=4
        elif len(w1) > 0  and availableMana >= 1:
            print 'Summon White Cost1.'
            summon_creature = w1[0]
            availableMana-=1
        elif len(w6) > 0  and availableMana >= 6:
            print 'Summon White Cost6.'
            summon_creature = w6[0]
            availableMana-=6
        elif len(g5) > 0  and availableMana >= 5:
            print 'Summon Green Cost5.'
            summon_creature = g5[0]
            availableMana-=5
        else:
            print 'Couldnt find a summonable creature. Break loop.'
            break
        
        try:
            summon(resources,summon_creature)
        except:
            Settings.MoveMouseDelay = 0.1
            break
        wait(2)
        if exists(resources.BUTTON_OK2, 2) != None:
            try:
                click(resources.BUTTON_OK2)
                wait(1)
                click(resources.BUTTON_OK2)
            except:
                print "failed to click"

def SummonHakuho(resources, currentMana):
    print 'SummonSpell'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    count = 0

    #マナゾーンの色チェック
    for retryLoop in range(10):
        manaColors = getManaColor(resources)
        print manaColors
        if manaColors["RED"] == False and manaColors["BLACK"] == False and availableMana >= 1:
            print "retry"
        elif (manaColors["RED"] == False or manaColors["BLACK"] == False) and availableMana >= 2:
            print "retry"
        else:
            break
    
    for num in range(10):
        summon_creature = None
        r2 = findAny(resources.ICON_COST_RED_2)
        r3 = findAny(resources.ICON_COST_RED_3)
        r4 = findAny(resources.ICON_COST_RED_4)
        bk2 = findAny(resources.ICON_COST_BLACK_2)
        bk3 = findAny(resources.ICON_COST_BLACK_3)
        bk4 = findAny(resources.ICON_COST_BLACK_4)
        
        
        if len(r2) > 0 and manaColors["RED"] and availableMana == 2:
            summon_creature = r2[0]
            availableMana-=2
            count += 1
        elif len(bk2) > 0 and manaColors["BLACK"] and availableMana == 2:
            summon_creature = bk2[0]
            availableMana-=2
            count += 1
        elif len(bk3) > 0 and manaColors["BLACK"] and availableMana == 3:
            summon_creature = bk3[0]
            availableMana-=3
            count += 1
        elif len(r3) > 0 and manaColors["RED"] and availableMana == 3:
            summon_creature = r3[0]
            availableMana-=3
            count += 1
        elif len(r2) > 0 and manaColors["RED"] and availableMana >= 3:
            summon_creature = r2[0]
            availableMana-=2
            count += 1
        elif len(bk2) > 0 and manaColors["BLACK"] and availableMana >= 3:
            summon_creature = bk2[0]
            availableMana-=2
            count += 1
        elif len(bk3) > 0 and manaColors["BLACK"] and availableMana >= 4:
            summon_creature = bk3[0]
            availableMana-=3
            count += 1
        elif len(r3) > 0 and manaColors["RED"] and availableMana >= 4:
            summon_creature = r3[0]
            availableMana-=3
            count += 1
        elif len(r4) > 0 and manaColors["RED"] and availableMana >= 4:
            summon_creature = r4[0]
            availableMana-=4
        elif len(bk4) > 0 and manaColors["BLACK"] and availableMana >= 4:
            summon_creature = bk4[0]
            availableMana-=4
            count += 1
        else:
            print 'Couldnt find a summonable creature. Break loop.'
            break
        
        try:
            summon(resources,summon_creature)
            wait(1.5)
        except:
            Settings.MoveMouseDelay = 0.1
            break
    return count

def SummonSpell(resources, currentMana):
    print 'SummonSpell'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    count = 0

    #マナゾーンの色をチェック
    manaColors = getManaColor(resources)
    print manaColors
    
    for num in range(10):
        summon_creature = None
        r3 = findAny(resources.ICON_COST_RED_3)
        r5 = findAny(resources.ICON_COST_RED_5)
        bk3 = findAny(resources.ICON_COST_BLACK_3)
        b2 = findAny(resources.ICON_COST_BLUE_2)
        b4 = findAny(resources.ICON_COST_BLUE_4)
        w2 = findAny(resources.ICON_COST_WHITE_2)
        g2 = findAny(resources.ICON_COST_GREEN_2)
        g4 = findAny(resources.ICON_COST_GREEN_4)

        if len(g2) > 0 and manaColors["GREEN"] and availableMana >= 2:
            summon_creature = g2[0]
            availableMana-=1
        elif len(w2) > 0 and manaColors["WHITE"] and availableMana >= 2:
            summon_creature = w2[0]
            availableMana-=2
        elif len(b4) > 0 and manaColors["BLUE"] and availableMana >= 4:
            summon_creature = b4[0]
            availableMana-=4
        elif len(r3) > 0 and manaColors["RED"] and availableMana >= 3:
            summon_creature = r3[0]
            availableMana-=3
        elif len(bk3) > 0 and manaColors["BLACK"] and availableMana >= 3:
            summon_creature = bk3[0]
            availableMana-=3
        elif len(r5) > 0 and manaColors["RED"] and availableMana >= 5:
            summon_creature = r5[0]
            availableMana-=5
        elif len(b2) > 0 and manaColors["BLUE"] and availableMana >= 2:
            summon_creature = b2[0]
            availableMana-=2
        elif len(g4) > 0 and manaColors["GREEN"] and availableMana >= 4:
            summon_creature = g4[0]
            availableMana-=4
        else:
            print 'Couldnt find a summonable creature. Break loop.'
            break
        
        try:
            summon(resources,summon_creature)
        except:
            Settings.MoveMouseDelay = 0.1
            break
        solveEffect(resources)

def SummonDest(resources, currentMana):
    print 'SummonDest'
    availableMana = currentMana
    print 'Available Mana : ' + str(availableMana)
    count = 0

    #マナゾーンの色をチェック
    manaColors = getManaColor(resources)
    print manaColors
    
    for num in range(10):
        summon_creature = None
        r3 = findAny(resources.ICON_COST_RED_3)
        r5 = findAny(resources.ICON_COST_RED_5)
        bk3 = findAny(resources.ICON_COST_BLACK_3)
        bk4 = findAny(resources.ICON_COST_BLACK_4)
        b4 = findAny(resources.ICON_COST_BLUE_4)
        w2 = findAny(resources.ICON_COST_WHITE_2)
        w4 = findAny(resources.ICON_COST_WHITE_4)
        g2 = findAny(resources.ICON_COST_GREEN_2)

        if len(r3) > 0 and manaColors["RED"] and availableMana >= 3:
            summon_creature = r3[0]
            availableMana-=3
        elif len(bk3) > 0 and manaColors["BLACK"] and availableMana >= 3:
            summon_creature = bk3[0]
            availableMana-=3
        elif len(r5) > 0 and manaColors["RED"] and availableMana >= 5:
            summon_creature = r5[0]
            availableMana-=5
        elif len(g2) > 0 and manaColors["GREEN"] and availableMana >= 2:
            summon_creature = g2[0]
            availableMana-=1
        elif len(w2) > 0 and manaColors["WHITE"] and availableMana >= 2:
            summon_creature = w2[0]
            availableMana-=2
        elif len(b4) > 0 and manaColors["BLUE"] and availableMana >= 4:
            summon_creature = b4[0]
            availableMana-=4
        elif len(bk4) > 0 and manaColors["BLACK"] and availableMana >= 4:
            summon_creature = bk4[0]
            availableMana-=4
        elif len(w4) > 0 and manaColors["WHITE"] and availableMana >= 4:
            summon_creature = w4[0]
            availableMana-=4
        else:
            print 'Couldnt find a summonable creature. Break loop.'
            break
        
        try:
            summon(resources,summon_creature)
        except:
            Settings.MoveMouseDelay = 0.1
            break
        solveEffect(resources)

def directAttack(resources, attackerW, attackerS):
    print 'directAttack'
    creaturePositions = []
    for num in range(3):
        print "checking W breaker...." + str(num)
        BZ = findAny(attackerW)
        if len(BZ) > 0:
            try:
                print "attacking shield...."
                CommonDMLib.dragDropAtSpeed(BZ[0],resources.TARGET_POSITION_DIRECT_ATTACK,1)
                creaturePositions.append([BZ[0].getX(),BZ[0].getY()])
    
                if exists(resources.MESSAGE_SELECT_BREAK_ENEMY_SHIELD, 2) != None:
                    print "shields were detected"
                    click(resources.TARGET_POSITION_FIRST_SHIELD)
                    click(resources.TARGET_POSITION_SECOND_SHIELD)
                    click(resources.BUTTON_OK2)
                wait(1)
            except:
                Settings.MoveMouseDelay = 0.1
                break
        
    for num in range(7):
        print "checking Single breaker...." + str(num)
        BZ = findAny(attackerS)
        for b in BZ:
            try:
                attackFlag = True
                for cp in creaturePositions:
                    if b.getX() <= (cp[0]+10) and b.getX() >= (cp[0]-10) and b.getY() <= (cp[1]+10) and b.getY() >= (cp[1]-10):
                        attackFlag = False
                        break
                    
                if attackFlag:
                    print "attacking shield...."
                    CommonDMLib.dragDropAtSpeed(b,resources.TARGET_POSITION_DIRECT_ATTACK,1)
                    creaturePositions.append([b.getX(),b.getY()])
    
                    if exists(resources.MESSAGE_SELECT_BREAK_ENEMY_SHIELD, 2) != None:
                        print "shields were detected"
                        click(resources.TARGET_POSITION_FIRST_SHIELD)
                        click(resources.TARGET_POSITION_SECOND_SHIELD)
                        click(resources.BUTTON_OK2)
                    wait(2)
            except:
                Settings.MoveMouseDelay = 0.1
                print "exception was occured"
                break

def directAttackHakuho(resources, attackers):
    print 'directAttack'
    if resources.APP_ENGINE == "NOX":
        OFFSETX = -1000
        OFFSETY = 400
        WIDTH = 1270
        HEIGHT = 150
    elif resources.APP_ENGINE == "ANDAPP":
        OFFSETX = -780
        OFFSETY = 335
        WIDTH = 1000
        HEIGHT = 110
    else:
        raise Exception()
        
    for attacker in attackers:
        for num in range(4):
            print "checking Single breaker...." + str(num)
            res = findAny(resources.ICON_ENEMY_CARD_COUNT)
            if len(res) == 0:
                return
            myAttackerRegion = Region(res[0].getX()+OFFSETX,res[0]. getY()+OFFSETY,WIDTH,HEIGHT)
            myAttackerRegion.highlight(0.1)
            BZ = myAttackerRegion.findAny(attacker)
            if len(BZ) == 0:
                print "no attackers"
                break
            for b in BZ:
                try:
                    print "attacking shield...."
                    click(b.getTarget())
                    CommonDMLib.dragDropAtSpeed(b,resources.TARGET_POSITION_DIRECT_ATTACK,1)
    
                    if exists(resources.MESSAGE_SELECT_BREAK_ENEMY_SHIELD, 2) != None:
                        print "shields were detected"
                        click(resources.TARGET_POSITION_FIRST_SHIELD)
                        click(resources.TARGET_POSITION_SECOND_SHIELD)
                        click(resources.BUTTON_OK2)
                    wait(1)
                except:
                    Settings.MoveMouseDelay = 0.1
                    print "exception was occured"
                    break


def battle(resources):
    print "Battle"
    for num in range(7):
        BZ = findAny(resources.ICON_MY_UNTAPPED_CREATURE)
        if len(BZ) > 0:
            c = findAny(resources.ICON_ENEMY_TAPPED_CREATURE_1, resources.ICON_ENEMY_TAPPED_CREATURE_2)
            if len(c) > 0:
                CommonDMLib.dragDropAtSpeed(BZ[0],c[0], 1.5)
                wait(0.5)

def retire(resources):
    for retireLoop in range(5):
       type(Key.ESC)
       if exists(resources.MESSAGE_RETIRE, 3) != None:
           try:
               click(resources.BUTTON_OK3)
           except:
               print "failed to click"
           break

#ゲーム中のイレギュラーの処理
#return 0 ゲームの正常終了
#return 1 ゲーム継続
def irregularLoop(resources, appname):
    print 'irregularLoop'
#  イレギュラーループ
    for enemyturn_loop in range(50):
        print 'This is ' + str(enemyturn_loop) + ' times loop.'
        
        #   自分のターンを検知
        if len(findAny(resources.BUTTON_TURN_END)) > 0:
            print 'My Turn is detected.'
            wait(1)
            break
        
        #不落の超人の強制アタックを検知
        if len(findAny(resources.BUTTON_TURN_END_RED)) > 0:
            print 'Force attack is detected. Retiring this game.'
            retire(resources)
        
        #   トリガー発動 
        if appname not in ["SP"]:
            if len(findAny(resources.BUTTON_ST)) > 0:
                print 'My ST is triggered.'
                try:
                    click(resources.BUTTON_ST)
                except:
                    print "failed to click"
                wait(0.5)

        #   シールド確認
        if len(findAny(resources.MESSAGE_SHIELD)) > 0:
            print 'My sheild is broken.'
            try:
                click(resources.BUTTON_OK2)
            except:
                print "failed to click"
            wait(0.5)

        #効果によるクリーチャー選択
        if appname not in ["SP"]:
            if len(findAny(resources.MESSAGE_TAP)) > 0 or \
            len(findAny(resources.MESSAGE_DEST))   > 0 or \
            len(findAny(resources.MESSAGE_EFFECT)) > 0 or \
            len(findAny(resources.MESSAGE_MANA))   > 0 or \
            len(findAny(resources.MESSAGE_SELECT))   > 0 or \
            len(findAny(resources.MESSAGE_BOUNCE))   > 0:
                print 'Tap, Dest, Mana, Bounce'
                BZ = findAny(
                        resources.ICON_MY_CREATURE1,
                        resources.ICON_MY_CREATURE2,
                        resources.ICON_MY_CREATURE3,
                        resources.ICON_MY_CREATURE4,
                        resources.ICON_ENEMY_UNTAPPED_BLOCKER,
                        resources.ICON_ENEMY_CREATURE1,
                        resources.ICON_ENEMY_CREATURE2,
                        resources.ICON_ENEMY_CREATURE3,
                        resources.ICON_ENEMY_CREATURE4,
                        resources.ICON_ENEMY_CREATURE5)
                for b in BZ:
                    click(b)
                    wait(0.5)
                    if exists(resources.ICON_SELECTED, 1) != None:
                        try:
                            click(resources.BUTTON_OK4)
                        except:
                            print "failed to click"
                        break
                if len(findAny(resources.ICON_SELECTED)) > 0:
                    try:
                        click(resources.BUTTON_OK4)
                    except:
                        print "failed to click"
                    break
                wait(0.5)
                if exists(resources.MESSAGE_NO_CREATURE_SELECTED,5) != None:
                    click(resources.BUTTON_OK2)
                wait(0.5)
            
        if len(findAny(resources.BUTTON_SMALL_BATTLE_START)) > 0:
            print 'Game has Finished.'
            return 0

        #ブロック
        if appname not in ["LEGEND", "SP"]:
            if len(findAny(resources.MESSAGE_BLOCK)) > 0 or len(findAny(resources.MESSAGE_CHOOSE_BLOCKER)) > 0:
                print 'Block?'
                if len(findAny(resources.ICON_MY_UNTAPPED_BLOCKER)) > 0:
                    try:
                        click(resources.ICON_MY_UNTAPPED_BLOCKER)
                        click(resources.BUTTON_BLOCK)
                    except:
                        print "failed to click"
                if len(findAny(resources.ICON_MY_UNTAPPED_BLOCKER2)) > 0:
                    try:
                        click(resources.ICON_MY_UNTAPPED_BLOCKER2)
                        click(resources.BUTTON_BLOCK)
                    except:
                        print "failed to click"

                if len(findAny(resources.BUTTON_NOBLOCK)) > 0:
                    try:
                        click(resources.BUTTON_NOBLOCK)
                    except:
                        print "failed to click"
                wait(1)

        
        if appname not in ["LEGEND", "DAILY"]:
            if len(findAny(resources.BUTTON_RETRY)) > 0:
                #game_loopを終了する。
                click(resources.BUTTON_RETRY)
                
        if appname not in ["LEGEND", "DAILY"]:
            #デモニックバイス
            if len(findAny(resources.TITLE_HAND1)) > 0:
                print 'Player need to select his hands.'
                click(resources.TITLE_HAND1)
                click(resources.TITLE_HAND2)
                click(resources.BUTTON_OK2)
                wait(1)
        
        if  enemyturn_loop == 49:
            print 'Irregular loop is over 50. Restart is necessary.'
            raise Exception
    
    return 1

def gameLoop(resources, strategy, appname):
    #リタイア
    if strategy == 6:
        retire(resources)
        exists(resources.BUTTON_SMALL_BATTLE_START,120)
        return
    elif  strategy == 103:
        if len(findAny(resources.ICON_ENEMY_MANA0)) == 0:
            retire(resources)
            exists(resources.BUTTON_SMALL_BATTLE_START, 120)
            return "retire"
        
    for game_loop in range(50):
        print "Inside Game Loop"
        if strategy not in [1,3,4,6]:
            if len(findAny(resources.ICON_ENEMY_CARD_COUNT)) > 0:
                click(resources.ICON_ENEMY_CARD_COUNT)
                wait(1)
            #  手札選択
            if len(findAny(resources.AVATOR_DEFAULT_MALE)) > 0:
                click(resources.AVATOR_DEFAULT_MALE)
                wait(1)
            
        #  マナチャージ
        if strategy in [1,3,4,6]:
            print "no charge"
        elif strategy in [2,7]:
            currentMana = ChargeManaRedBlack(resources)
        elif strategy in [5,8]:
            currentMana = ChargeManaLarge(resources)
        elif strategy == 100:
            currentMana = ChargeManaBasic(resources)
        elif strategy == 102:
            currentMana = ChargeManaFatty(resources)
        elif strategy == 103:
            currentMana = ChargeManaHakuho(resources)
        wait(1)
        
        #  召喚
        if strategy in [1,3,4,6]:
            print "no summon"
        elif strategy in [2,7]:
            SummonRedBlack(resources,currentMana)
        elif strategy == 5:
            SummonLarge(resources,currentMana)
        elif strategy == 8:
            if currentMana >= 3 and currentMana <= 6 and len(findAny(resources.ICON_MY_UNTAPPED_BLOCKER)) == 0:
                retire(resources)
                exists(resources.BUTTON_SMALL_BATTLE_START, 120)
                return
            SummonLarge(resources,currentMana)
        elif strategy == 100:
            SummonBasic(resources,currentMana)
        elif strategy == 102:
            SummonFatty(resources,currentMana)
        elif strategy == 103:
            SummonHakuho(resources,currentMana)
        wait(1)
        
        #  攻撃
        if strategy in [1,6]:
            print "no attack"
        elif strategy in [2,100,102]:
            directAttack(resources,[resources.ICON_W_BREAKER],[resources.ICON_MY_UNTAPPED_CREATURE, resources.ICON_MY_UNTAPPED_CREATURE2])
        elif strategy in [7]:
            attackersList = []
            for countLoop in range(5):
                a = countMyBattleZone(resources, resources.ICON_MY_UNTAPPED_CREATURE)
                print "a : " + str(a)
                attackersList.append(a)
            attackers = min(attackersList)
            if attackers >= 3:
                directAttack(resources,[resources.ICON_W_BREAKER],[resources.ICON_MY_UNTAPPED_CREATURE, resources.ICON_MY_UNTAPPED_CREATURE2])
        elif strategy in [3,4]:
            battle(resources)
        elif strategy in [5,8]:
            attackersList = []
            for countLoop in range(5):
                a = countMyBattleZone(resources, resources.ICON_W_BREAKER)
                print "a : " + str(a)
                attackersList.append(a)
            attackers = max(attackersList)
            if attackers >= 3:
                directAttack(resources,[resources.ICON_W_BREAKER],[resources.ICON_MY_UNTAPPED_CREATURE, resources.ICON_MY_UNTAPPED_CREATURE2])
        elif strategy in [103]:
            for attackLoop in range(2):
                blockers = countEnemyBlockers(resources)
                print "blockers : " + str(blockers)
                if blockers == 0:
                    directAttackHakuho(resources, [resources.ICON_MY_UNTAPPED_CREATURE])
                    break
                else:
                    attackersList = []
                    for countLoop in range(10):
                        a = countMyBattleZone(resources, resources.ICON_MY_UNTAPPED_CREATURE)
                        print "a : " + str(a)
                        attackersList.append(a)
                    attackers = min(attackersList)
                    print "attackers : " + str(attackers)
                    if attackers - blockers * 2 > 0 or attackers >= 6:
                        directAttackHakuho(resources, [
                                    resources.ICON_BELBET,
                                    resources.ICON_JOE,
                                    resources.ICON_GREGORIA,
                                    resources.ICON_TILER,
                                    resources.ICON_VOGUE,
                                    resources.ICON_TENTIKE,
                                    resources.ICON_MEZZ,
                                    resources.ICON_KISHA,
                                    resources.ICON_KAMIKAZE,
                                    resources.ICON_MY_UNTAPPED_CREATURE])
                        break
                    else:
                        shields = countEnemyShields(resources)
                        print "shields : " + str(shields)
                        lethal = attackers - shields - blockers
                        print "lethal : " + str(lethal)
                        if lethal > 0:
                            directAttackHakuho(resources, [
                                    resources.ICON_BELBET,
                                    resources.ICON_JOE,
                                    resources.ICON_GREGORIA,
                                    resources.ICON_TILER,
                                    resources.ICON_VOGUE,
                                    resources.ICON_TENTIKE,
                                    resources.ICON_MEZZ,
                                    resources.ICON_KISHA,
                                    resources.ICON_KAMIKAZE,
                                    resources.ICON_MY_UNTAPPED_CREATURE])
                            break
                        elif len(findAny(resources.ICON_BELBET)) > 0:
                            directAttackHakuho(resources, [resources.ICON_BELBET])
                        else:
                            break
                
        wait(1)
            
        #  ターンエンド
        if len(findAny(resources.BUTTON_TURN_END)) > 0:          
            turnEnd(resources)
        wait(1)
        #  イレギュラーループ
        if irregularLoop(resources, appname) == 0:
            break