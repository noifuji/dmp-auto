# -*- coding: utf-8 -*-
from sikuli import *
import sys
import traceback
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
        CommonDMLib.dragDropAtSpeed(target, resources.TARGET_POSITION_CHARGE, 1.2)
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

        print "r2:" + len(r2) + ",r3:" + len(r3) + ",r4:" + len(r4) + ",k2:" + len(k2) + ",k3:" + len(k3) + ",k4:" + len(k4)

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



def directAttack(resources):
    print 'directAttack'
    creaturePositions = []
    for num in range(3):
        print "checking W breaker...." + str(num)
        BZ = findAny(resources.ICON_W_BREAKER)
        if len(BZ) > 0:
            try:
                CommonDMLib.dragDropAtSpeed(BZ[0],resources.TARGET_POSITION_DIRECT_ATTACK,1)
                creaturePositions.append([b.getX(),b.getY()])

                if exists(resources.MESSAGE_SELECT_BREAK_ENEMY_SHIELD, 5) != None:
                    click(resources.TARGET_POSITION_FIRST_SHIELD)
                    click(resources.TARGET_POSITION_SECOND_SHIELD)
                    click(resources.BUTTON_OK2)
                wait(2)
            except:
                Settings.MoveMouseDelay = 0.1
                break
        else:
            break
    for num in range(5):
        print "checking Single breaker...." + str(num)
        BZ = findAny(resources.ICON_MY_UNTAPPED_CREATURE, resources.ICON_MY_UNTAPPED_CREATURE2)
        for b in BZ:
            try:
                attackFlag = True
                for cp in creaturePositions:
                    if b.getX() <= (cp[0]+10) and b.getX() >= (cp[0]-10) and b.getY() <= (cp[1]+10) and b.getY() >= (cp[1]-10):
                        attackFlag = False
                        break
                if attackFlag:
                    CommonDMLib.dragDropAtSpeed(b,resources.TARGET_POSITION_DIRECT_ATTACK,1)
                    creaturePositions.append([b.getX(),b.getY()])
    
                    if exists(resources.MESSAGE_SELECT_BREAK_ENEMY_SHIELD, 2) != None:
                        click(resources.TARGET_POSITION_FIRST_SHIELD)
                        click(resources.TARGET_POSITION_SECOND_SHIELD)
                        click(resources.BUTTON_OK2)
            except:
                Settings.MoveMouseDelay = 0.1
                print "exception was occured"
                break
        wait(1)

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
            wait(3)
            break
        #   トリガー発動 
        if len(findAny(resources.BUTTON_ST)) > 0:
            print 'My ST is triggered.'
            click(resources.BUTTON_ST)
            wait(0.5)
        #   シールド確認
        if len(findAny(resources.MESSAGE_SHIELD)) > 0:
            print 'My sheild is broken.'
            click(resources.BUTTON_OK2)
            wait(0.5)
        if len(findAny(resources.MESSAGE_TAP))   > 0 or len(findAny(resources.MESSAGE_DEST))   > 0:
            print 'Tap or Dest'   
            BZ = findAny(
                    resources.ICON_ENEMY_UNTAPPED_BLOCKER, 
                    resources.ICON_ENEMY_UNTAPPED_CREATURE,
                    resources.ICON_ENEMY_TAPPED_CREATURE_1,
                    resources.ICON_ENEMY_TAPPED_CREATURE_2)
            for b in BZ:
                click(b)
                if exists(resources.BUTTON_OK2, 1) != None:
                    click(resources.BUTTON_OK2)
                    break
            wait(0.5)
            if exists(resources.MESSAGE_NO_CREATURE_SELECTED,5) != None:
                click(resources.BUTTON_OK2)
            wait(0.5)
            
        if len(findAny(resources.BUTTON_SMALL_BATTLE_START)) > 0:
            print 'Game has Finished.'
            return 0

        #レジェンドではスルーする
        if appname not in ["LEGEND"]:
            if len(findAny(resources.MESSAGE_BLOCK)) > 0 or len(findAny(resources.MESSAGE_CHOOSE_BLOCKER)) > 0:
                print 'Block?'
                if len(findAny(resources.ICON_MY_UNTAPPED_BLOCKER)) > 0:
                    click(resources.ICON_MY_UNTAPPED_BLOCKER)
                    click(resources.BUTTON_BLOCK)
                else:
                    click(resources.BUTTON_NOBLOCK)
                wait(1)
        
            if len(findAny(resources.BUTTON_RETRY)) > 0:
                #game_loopを終了する。
                click(resources.BUTTON_RETRY)
            #死の宣告、デスモーリー等
            if len(findAny(resources.MESSAGE_SELECT_OWN_CREATURE)) > 0 or len(findAny(resources.MESSAGE_SELECT_OWN_CREATURE2)) > 0:
                print 'Player need to select his creature.'                       
                BZ = findAny(
                        resources.ICON_MY_UNTAPPED_CREATURE,
                        resources.ICON_MY_TAPPED_CREATURE,
                        resources.ICON_MY_UNTAPPED_BLOCKER)
                for b in BZ:
                    click(b)
                    if exists(resources.BUTTON_OK2,1) != None:
                        click(resources.BUTTON_OK2)
                        break
                wait(0.5)
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
    for game_loop in range(50):
        print "Inside Game Loop"
        if len(findAny(resources.ICON_ENEMY_CARD_COUNT)) > 0:
            click(resources.ICON_ENEMY_CARD_COUNT)
            wait(1)
        #  手札選択
        if len(findAny(resources.AVATOR_DEFAULT_MALE)) > 0:
            click(resources.AVATOR_DEFAULT_MALE)
            wait(1)
        #  マナチャージ
        if strategy == 100:
            currentMana = ChargeManaBasic(resources)
        elif strategy == 2:
            currentMana = ChargeManaRedBlack(resources)
        wait(1)
        #  召喚
        if strategy == 100:
            SummonBasic(resources,currentMana)
        elif strategy == 2:
            SummonRedBlack(resources,currentMana)
        wait(1)
        #  攻撃
        directAttack(resources)
        wait(1)
        #  ターンエンド
        if len(findAny(resources.BUTTON_TURN_END)) > 0:          
            turnEnd(resources)
        wait(1)
        #  イレギュラーループ
        if irregularLoop(resources, appname) == 0:
            break