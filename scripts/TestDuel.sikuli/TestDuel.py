sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import GameLib
import CommonDMLib
import NoxResources
import AndAppResources
appname = "test"
Settings.MoveMouseDelay = 0.1

def chargeMana(resources):
    print "ChargeMana"

def summon(resources, currentMana):
    print "summon"

def gameLoop(resources, appname):
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
        currentMana = chargeMana(resources)
        wait(1)
        
        #  召喚
        summon(resources,currentMana)
        wait(1)
        
        #  攻撃
        GameLib.directAttack(resources)
        
        wait(1)
        #  ターンエンド
        if len(findAny(resources.BUTTON_TURN_END)) > 0:          
            GameLib.turnEnd(resources)
        wait(1)
        #  イレギュラーループ
        if GameLib.irregularLoop(resources, appname) == 0:
            break
        
resources = NoxResources
totalDuelCount = 0
winCount = 0

for battleLoop in range(100):
    CommonDMLib.waitStartingGame(resources)
    wait(10)
    gameLoop(resources, "MAIN")
    for battleResultLoop in range(200):
        print "battleResultLoop..." + str(battleResultLoop)
        CommonDMLib.skipRewards(resources)
        if len(findAny(resources.BUTTON_DUEL_HISTORY)) > 0:
            try:
                click(resources.BUTTON_DUEL_HISTORY)
            except:
                print "failed to click"
        if len(findAny(resources.TITLE_DUEL_HISTORY)) > 0:
            try:
                click(resources.BUTTON_RESULT)
                wait(2)
                break
            except:
                print "failed to click"
        if battleResultLoop >= 199:
            raise Exception("Too many battleResultLoop")
    #battleResultLoop End
    totalDuelCount += 1
    if len(findAny(resources.ICON_WIN)) > 0:
        winCount += 1
        
    click(resources.BUTTON_SMALL_BATTLE_START)