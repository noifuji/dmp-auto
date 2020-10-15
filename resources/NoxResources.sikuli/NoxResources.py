# -*- coding: utf-8 -*-
from sikuli import *
#################Constants###############
APP_ENGINE = "NOX"
#################DECKS###############
DECKIMAGE_RED_BLACK = Pattern("1598939664217.png").similar(0.85)
DECKIMAGE_ST = Pattern("1596892120520-1.png").similar(0.90)
DECKIMAGE_LARGE_CREATURE = "1599784444953.png"#Pattern("1596892035465.png").similar(0.90)
DECKIMAGE_STSPELL = "1598831170897.png"
DECKIMAGE_SPBATTLE = "1601891857285.png"
DECKIMAGE_MAIN = "1601457706210.png"
##############NoxPlayer Home#################
TITLE_MULTI_PLAYER = Pattern("1596962591946.png").targetOffset(92,154)
BUTTON_NOX_STOP = Pattern("1596777933938.png").similar(0.90)
BUTTON_NOX_PLAY = Pattern("1601077335160.png").similar(0.95)
ICON_SEARCH = Pattern("1601532705094.png").similar(0.83).targetOffset(-84,4)
BUTTON_NOX_OK_BLUE = Pattern("1601533049989.png").similar(0.90)
ICON_BROWSER = "ICON_BROWSER.png"
MESSAGE_FAILED_TO_START_LAUNCHER = Pattern("1600043514936.png").targetOffset(-205,56)
MESSAGE_LAUNCHER_STOPPED_MANY_TIMES = Pattern("naga.png").targetOffset(-211,46)
MESSAGE_SYSTEM_UI_STOPPED = Pattern("1601454136560.png").targetOffset(-197,43)
MESSAGE_BACKUP = Pattern("MESSAGE_BACKUP.png").targetOffset(-79,47)
MESSAGE_BACKUP_NODISP = "MESSAGE_BACKUP_NODISP.png"
BUTTON_NOX_OK = Pattern("BUTTON_NOX_OK.png").targetOffset(71,-1)
BUTTON_ALLOW = Pattern("BUTTON_ALLOW.png").targetOffset(61,1)
MESSAGE_CONFIRM_ALLOW = "MESSAGE_CONFIRM_ALLOW.png"
BUTTON_ALLOW_BLUE = "BUTTON_ALLOW_BLUE.png"
AVIRA = "AVIRA.png"
#################DMP Common###############
BUTTON_TAKEOVER = Pattern("1596765489772.png").targetOffset(-257,83)
BUTTON_MENU = "1602164343414.png"
BUTTON_CLEAR_CACHE = Pattern("1602164939945.png").targetOffset(144,-66)
BUTTON_SKIP = Pattern("skip.png").similar(0.91)
BUTTON_OK = Pattern("OK.png").similar(0.81)
BUTTON_OK2 = Pattern("1601521147368.png").similar(0.81)
BUTTON_OK3 =Pattern("1601873579981.png").similar(0.88) 
BUTTON_RETRY = "1596901274897.png"
BUTTON_LATER = Pattern("1602763660816.png").similar(0.90)
BUTTON_AGREE = "1597913007417.png"
BUTTON_SMALL_OK = Pattern("1602232771756.png").similar(0.86)
BUTTON_CANCEL = Pattern("1596765861356.png").similar(0.84)
BUTTON_SMALL_BATTLE_START = "1596767585645.png"
BUTTON_LARGE_BATTLE_START = "1596767599082.png"
BUTTON_DUEL_HISTORY = Pattern("1601604956292.png").similar(0.89)
TITLE_DUEL_HISTORY = Pattern("1601604915832.png").similar(0.89)
BUTTON_RESULT = Pattern("1601604910411.png").similar(0.89)
BUTTON_BACK = "1596962178461.png" 
BUTTON_BACK2 = Pattern("1596962178461.png").similar(0.85).targetOffset(-3,69) 

BUTTON_CLOSE = "1596776234501.png"
BUTTON_TAP_AND_NEXT = "TAP_AND_NEXT.png"

#################HOME####################
ICON_HOME = Pattern("1602026836624.png").similar(0.86)
ICON_EXTRA = Pattern("ICON_EXTRA.png").similar(0.76)
ICON_SHOP = "1602494935748.png"
ICON_SOLO_PLAY = Pattern("1596767681008.png").similar(0.80)
ICON_MISSION = "1596775980978.png"
ICON_PRESENT_WITH_SIGN = Pattern("ICON_PRESENT_SIGN.png").similar(0.95).targetOffset(-16,20)
ICON_OTHER = "1600519768850.png"
BUTTON_MAIN_STORY = "1596767702129.png"
BUTTON_LEGEND_BATTLE = Pattern("BUTTON_LEGEND_BATTLE.png").similar(0.78)
BUTTON_SP_BATTLE = Pattern("1601885213479.png").similar(0.84)
BUTTON_PROFILE = "BUTTON_PROFILE.png"
################PRESENT#################
TITLE_PRESENT = "TITLE_PRESENT.png"
BUTTON_RECIEVE = "BUTTON_RECIEVE.png"
MESSAGE_NO_PRESENTS = "MESSAGE_NO_PRESENTS.png"
################PROFILE#################
TITLE_PLAYER_LV = Pattern("TITLE_PLAYER_LV.png").similar(0.60)
BUTTON_ITEM = "BUTTON_ITEM.png"
TITLE_PROFILE = "TITLE_PROFILE.png"
TITLE_PACK1 = Pattern("1600523506796.png").similar(0.90)
TITLE_PACK2 = Pattern("1600523536921.png").similar(0.90)
TITLE_PACK3 = Pattern("1600523796024.png").similar(0.90)
TITLE_PACK4 =Pattern("1600523808395.png").similar(0.90)
TITLE_PACK5 =Pattern("1600523838234.png").similar(0.90)
TITLE_PACK5SR =Pattern("1600524008323.png").similar(0.85)
TICKET_BEST = Pattern("1601801798254.png").similar(0.85)
TITLE_ITEM = Pattern("1600524382930.png").targetOffset(268,239)
TITLE_ITEM_DRAG = Pattern("1601009165140.png").targetOffset(372,392)
TITLE_ITEM_DROP = Pattern("1601009179822.png").targetOffset(359,68)
BUTTON_OTHER = "1600525368575.png"
TITLE_GOLD = Pattern("1600525512184.png").similar(0.85)
TITLE_DMPOINT = "1600525496880.png"
#################LegendBattle####################
ICON_TARGET_REWARD = Pattern("1601645476931.png").similar(0.90)
ICON_SP_TARGET_REWARD = Pattern("1601973838151.png").similar(0.85)
ICON_NEXT_REWARD_OF_TARGET = "ICON_NEXT_REWARD_OF_TARGET.png"
ICON_REWARD_COMPLETED = "1601643940453.png"
TITLE_LEGEND_STAGE1 = Pattern("1601517613543.png").similar(0.80)
TITLE_LEGEND_STAGE2 = Pattern("TITLE_LEGEND_STAGE2.png").similar(0.80)
TITLE_LEGEND_STAGE3 = Pattern("TITLE_LEGEND_STAGE3.png").similar(0.80)
#################MainStory####################
BACKGROUND_EPISODE_LIST ="1601536187137.png" 
TITLE_MAIN_STORY = "1596767550917.png"
TITLE_MAIN_STORY2 = Pattern("1596767550917.png").targetOffset(-167,290)
TUTORIAL_MAIN_STORY = "1596767507281.png"
TITLE_EP1 = Pattern("1596989223358.png").similar(0.87)
TITLE_EP1_LOW_RESOLUTION = Pattern("1597203982188.png").similar(0.92)
EPISODES = [{"EPISODE":1, "IMAGE":Pattern("1601271450420.png").similar(0.90).targetOffset(36,46)},
        {"EPISODE":2, "IMAGE":Pattern("1601271478062.png").similar(0.90).targetOffset(38,42)},
        {"EPISODE":3, "IMAGE":Pattern("1601271490536.png").similar(0.90).targetOffset(50,38)},
        {"EPISODE":4, "IMAGE":Pattern("1601271503367.png").similar(0.90).targetOffset(28,39)},
        {"EPISODE":5, "IMAGE":Pattern("1601271519805.png").similar(0.90).targetOffset(9,38)}]
BUTTON_EP1 = Pattern("1597970568251.png").similar(0.95)
TITLE_EP1_STAGE1 = Pattern("1596861957365.png").similar(0.85)
TITLE_EP5_STAGE10 = Pattern("1600991582416.png").similar(0.90)
BUTTON_CONFIRM_REWARD = "BUTTON_CHECK_REWARD.png"
TITLE_REWARD_INFO = "1600991713407.png"
ICON_CLEARED = Pattern("1600991811657.png").similar(0.90)
STAGES = [{"STAGE":1, "IMAGE":"1601267258379.png"},
            {"STAGE":2, "IMAGE":"1601267289541.png"},
            {"STAGE":3, "IMAGE":"1601267298169.png"},
            {"STAGE":4, "IMAGE":"1601267308310.png"},
            {"STAGE":5, "IMAGE":"1601267319803.png"},
            {"STAGE":6, "IMAGE":"1601267327819.png"},
            {"STAGE":7, "IMAGE":"1601267339419.png"},
            {"STAGE":8, "IMAGE":"1601267349588.png"},
            {"STAGE":9, "IMAGE":"1601267359991.png"},
            {"STAGE":10, "IMAGE":"1601267368618.png"},
            {"STAGE":1, "IMAGE":"1601269334194.png"},
            {"STAGE":2, "IMAGE":"1601269342691.png"},
            {"STAGE":3, "IMAGE":"1601269351087.png"},
            {"STAGE":4, "IMAGE":"1601269361387.png"},
            {"STAGE":5, "IMAGE":"1601269370363.png"},
            {"STAGE":6, "IMAGE":"1601269379960.png"},
            {"STAGE":7, "IMAGE":"1601269389436.png"},
            {"STAGE":8, "IMAGE":"1601269397792.png"},
            {"STAGE":9, "IMAGE":"1601269412454.png"},
            {"STAGE":10, "IMAGE":"1601269421414.png"},
            {"STAGE":11, "IMAGE":"1601269429136.png"},
            {"STAGE":12, "IMAGE":"1601269438065.png"},
            {"STAGE":13, "IMAGE":"1601269448309.png"},
            {"STAGE":14, "IMAGE":"1601269454944.png"},
            {"STAGE":15, "IMAGE":"1601269462312.png"},
            {"STAGE":1, "IMAGE":"1601269477661.png"},
            {"STAGE":2, "IMAGE":"1601269486427.png"},
            {"STAGE":3, "IMAGE":"1601269493341.png"},
            {"STAGE":4, "IMAGE":"1601269499709.png"},
            {"STAGE":5, "IMAGE":"1601269507017.png"},
            {"STAGE":6, "IMAGE":"1601269518783.png"},
            {"STAGE":7, "IMAGE":"1601269525564.png"},
            {"STAGE":8, "IMAGE":"1601269532371.png"},
            {"STAGE":9, "IMAGE":"1601269546437.png"},
            {"STAGE":10, "IMAGE":"1601269666947.png"},
            {"STAGE":11, "IMAGE":"1601269677285.png"},
            {"STAGE":12, "IMAGE":"1601269685648.png"},
            {"STAGE":13, "IMAGE":"1601269694655.png"},
            {"STAGE":14, "IMAGE":"1601269704417.png"},
            {"STAGE":15, "IMAGE":"1601269712707.png"}]
##################Messages################
MESSAGE_RESTART_DUEL = Pattern("1596765847719.png").similar(0.86)
MESSAGE_LAST_SP_BATTLE = "1601901320202.png"
MESSAGE_LAST_BATTLE = "1598356619089.png"
#AD = Pattern("1596767400207.png").similar(0.85)
AD = Pattern("AD2.png").similar(0.80)
MESSAGE_NO_OPPONENTS = Pattern("OK.png").similar(0.67)
MESSAGE_CONNECTION_LOST = "1601976850151.png"
MESSAGE_ERROR_9003 = "1601976850151.png"
MESSAGE_DOWNLOAD = "1597923486888.png"
##################REWARDS################
TITLE_REWARD_LEVEL_UP = Pattern("1596766440880.png").similar(0.89)
TITLE_REWARD_DAILY = "1596766829387.png"
TITLE_REWARD_SECRET = Pattern("1596766584222.png").similar(0.80)
TITLE_REWARD_CLEAR = "1596766549773.png"
TITLE_REWARD_POINT = "1596768099812.png"
##################MISSION################
TITLE_MISSION =  "1596776003050.png"
#SPELL
MISSION_SPELL_10={"GROUP":"SPELL","NAME":"MISSION_SPELL_10","IMAGE":Pattern("TenTimesSpell-1.png").similar(0.85)}
MISSION_SPELL_12_LOWER5COST={"GROUP":"SPELL","NAME":"MISSION_SPELL_12_LOWER5COST","IMAGE":Pattern("TwelveTimesSmallSpell-1.png").similar(0.85)}

#SPEED
MISSION_WIN_7TURNS={"GROUP":"SPEED","NAME":"MISSION_WIN_7TURNS","IMAGE":Pattern("WinIn7Turns.png").similar(0.85)}
MISSION_WIN_10TURNS={"GROUP":"SPEED","NAME":"MISSION_WIN_10TURNS","IMAGE":Pattern("WinIn10Turns.png").similar(0.85)}
MISSION_WIN_4SHIELD={"GROUP":"SPEED","NAME":"MISSION_WIN_4SHIELD","IMAGE":Pattern("WinWith4ShieldsRemained-1.png").similar(0.85)}
MISSION_WIN_2SHIELD={"GROUP":"SPEED","NAME":"MISSION_WIN_2SHIELD","IMAGE":Pattern("WinWith2ShieldsRemained.png").similar(0.85)}
MISSION_WIN_5={"GROUP":"SPEED","NAME":"MISSION_WIN_5","IMAGE":Pattern("Win5Times-2.png").similar(0.85).targetOffset(514,73)}
MISSION_CREATURE_10={"GROUP":"SPEED","NAME":"MISSION_CREATURE_10","IMAGE":Pattern("Summon10Creatures-1.png").similar(0.85)}
MISSION_CREATURE_18_LOWER5={"GROUP":"SPEED","NAME":"MISSION_CREATURE_18_LOWER5","IMAGE":Pattern("Summon18Creatures-1.png").similar(0.85)}
MISSION_CREATURE_18_LOWER5000={"GROUP":"SPEED","NAME":"MISSION_CREATURE_18_LOWER5000","IMAGE":Pattern("1601359075431.png").similar(0.85)}
MISSION_PLAY_50={"GROUP":"SPEED","NAME":"MISSION_PLAY_50","IMAGE":Pattern("Play50CostCards-1.png").similar(0.85)}
MISSION_BREAK_10={"GROUP":"SPEED","NAME":"MISSION_BREAK_10","IMAGE":Pattern("1601262959306.png").similar(0.85)}
MISSION_DRAW_20={"GROUP":"SPEED","NAME":"MISSION_DRAW_20","IMAGE":Pattern("Draw20Cards.png").similar(0.85)}
MISSION_CHARGE_10={"GROUP":"SPEED","NAME":"MISSION_CHARGE_10","IMAGE":Pattern("Charge10Manas.png").similar(0.85)}

#LARGE_CREATURE
MISSION_CREATURE_6_HIGHER5={"GROUP":"LARGE","NAME":"MISSION_CREATURE_6_HIGHER5","IMAGE":Pattern("Summon6BigCreaturesCost5-1.png").similar(0.80)}
MISSION_CREATURE_6_HIGHER5000={"GROUP":"LARGE","NAME":"MISSION_CREATURE_6_HIGHER5000","IMAGE":Pattern("1601302284203.png").similar(0.85)}
MISSION_BREAK_3={"GROUP":"LARGE","NAME":"MISSION_BREAK_3","IMAGE":Pattern("Break3ShieldsInOneTurn-1.png").similar(0.86)}

#BATTLE
MISSION_DEST_4={"GROUP":"BATTLE","NAME":"MISSION_DEST_4","IMAGE":Pattern("1596881282876-1.png").similar(0.85)}
MISSION_BATTLE_5={"GROUP":"BATTLE","NAME":"MISSION_BATTLE_5","IMAGE":Pattern("FiveTimesBattleWithCreatures-1.png").similar(0.85)}

#ST
MISSION_ST_5={"GROUP":"ST","NAME":"MISSION_ST_5","IMAGE":Pattern("FiveTimesST-1.png").similar(0.85)}

#RETIRE
MISSION_DUEL_3={"GROUP":"RETIRE","NAME":"MISSION_DUEL_3","IMAGE":Pattern("1601865228012.png").similar(0.86)}
MISSION_DUEL_5={"GROUP":"RETIRE","NAME":"MISSION_DUEL_5","IMAGE":Pattern("FiveTimesBattle-1.png").similar(0.86)}

#SKIP
MISSION_SUMMON_3_SHINKA={"GROUP":"SKIP","NAME":"MISSION_SUMMON_3_SHINKA","IMAGE":Pattern("1596776105685-1.png").similar(0.91).targetOffset(414,63)}
MISSION_SPELL_4_HIGHER5={"GROUP":"SKIP","NAME":"MISSION_SPELL_4_HIGHER5","IMAGE":Pattern("FourTimesBigSpell-2.png").similar(0.85).targetOffset(464,66)}


GROUPS = ["SPELL","BATTLE","ST","LARGE","SPEED","RETIRE","SKIP"]
MISSIONS = [
        MISSION_SPELL_10,
        MISSION_SPELL_12_LOWER5COST,
        MISSION_WIN_7TURNS,
        MISSION_WIN_10TURNS,
        MISSION_WIN_4SHIELD,
        MISSION_WIN_2SHIELD,
        MISSION_WIN_5,
        MISSION_CREATURE_10,
        MISSION_CREATURE_18_LOWER5,
        MISSION_CREATURE_18_LOWER5000,
        MISSION_PLAY_50,
        MISSION_BREAK_10,
        MISSION_DRAW_20,
        MISSION_CHARGE_10,
        MISSION_CREATURE_6_HIGHER5,
        MISSION_CREATURE_6_HIGHER5000,
        MISSION_BREAK_3,
        MISSION_DEST_4,
        MISSION_BATTLE_5,
        MISSION_ST_5,
        MISSION_DUEL_3,
        MISSION_DUEL_5,
        MISSION_SUMMON_3_SHINKA,
        MISSION_SPELL_4_HIGHER5
        ]

SPELL_MISSIONS = [MISSION_SPELL_10,MISSION_SPELL_12_LOWER5COST]
SPEED_MISSIONS = [MISSION_WIN_7TURNS, MISSION_WIN_10TURNS,
        MISSION_WIN_2SHIELD, MISSION_WIN_5, MISSION_CREATURE_10,
        MISSION_CREATURE_18_LOWER5, MISSION_PLAY_50, MISSION_BREAK_10,
        MISSION_DRAW_20, MISSION_CHARGE_10]
BATTLE_MISSIONS = [MISSION_DEST_4,MISSION_BATTLE_5]
SHIELDTRRIGER_MISSIONS = [MISSION_ST_5]
LARGE_CREATURES = [MISSION_CREATURE_6_HIGHER5,MISSION_CREATURE_6_HIGHER5000,MISSION_BREAK_3,MISSION_WIN_4SHIELD]
RETIRE = [MISSION_DUEL_5]

#################DeckList####################
TITLE_DECKLIST = Pattern("1599376417408.png").targetOffset(192,218)
BUTTON_CREATE_NEW_DECK = "1598254360955.png"
BUTTON_CREATE_BY_CODE = "1598254370300.png"
INPUT_DECK_CODE1 = Pattern("1596780800323.png").targetOffset(-2,35)
INPUT_DECK_CODE2 = "1596792937212.png"
BUTTON_SAVE_DECK = Pattern("1596780884368.png").similar(0.85)
BUTTON_RARITY = [Pattern("1599967498096.png").similar(0.90),Pattern("1599967504642.png").similar(0.90)]#Pattern("1599967482462.png").similar(0.90),Pattern("1599967487478.png").similar(0.90),Pattern("1599967492513.png").similar(0.90),
BUTTON_FILTER = "BUTTON_FILTER.png"
SCROLL1 = Pattern("SCROLL1.png").similar(0.95)
SCROLL2 = Pattern("SCROLL2.png").similar(0.90)
BUTTON_RESET = "BUTTON_RESET.png"
BUTTON_DMPP01 = "BUTTON_DMPP01.png"
BUTTON_DMPP02 = "BUTTON_DMPP02.png"
BUTTON_DMPP03 = "BUTTON_DMPP03.png"
BUTTON_DMPP04 = "BUTTON_DMPP04.png"
BUTTON_DMPP05 = "BUTTON_DMPP05.png"
ICON_CARD_COUNT = [Pattern("x1.png").similar(0.85),Pattern("x2.png").similar(0.92),Pattern("x3.png").similar(0.91),Pattern("x4.png").similar(0.90)]
TITLE_CARD_LIST = Pattern("TITLE_CARD_LIST.png").targetOffset(44,164)
################DUEL#################
BUTTON_TURN_END = "turnEnd.png"
BUTTON_ENEMY_TURN = Pattern("1601886511079.png").similar(0.82)
AVATOR_DEFAULT_MALE = Pattern("Avator-1.png").targetOffset(376,-12)
ICON_MANA_0 = Pattern("mana0_beforeCharge.png").similar(0.95)
ICON_MANA_1 = Pattern("1601507068495.png").similar(0.90)#Pattern("mana1.png").similar(0.95)
ICON_MANA_2 = Pattern("mana2_beforeCharge.png").similar(0.95)
ICON_MANA_3 = Pattern("mana3_beforeCharge.png").similar(0.95)
ICON_MANA_4 = Pattern("mana4_beforeCharge.png").similar(0.95)
ICON_MANA_5 = Pattern("mana5_beforeCharge.png").similar(0.95)
ICON_MANA_6 = Pattern("mana6_beforeCharge.png").similar(0.95)
ICON_MANA_7 = Pattern("mana7_beforeCharge.png").similar(0.95)
ICON_MANA_8 = Pattern("mana8_beforeCharge.png").similar(0.95)
ICON_MANA_9 = Pattern("mana9_beforeCharge.png").similar(0.95)
ICON_MANA_10 = Pattern("mana10_beforeCharge.png").similar(0.95)
ICON_MANA_11 = Pattern("mana11.png").similar(0.95)
MANA_ICONS = [ICON_MANA_0, ICON_MANA_1, ICON_MANA_2, ICON_MANA_3, ICON_MANA_4, ICON_MANA_5, ICON_MANA_6, ICON_MANA_7]
ICON_CARD_SQUARE = Pattern("1601473911812.png").similar(0.84)
ICON_COST_WHITE_1 = Pattern("wcost1.png").similar(0.85).targetOffset(81,51)
ICON_COST_WHITE_2 = Pattern("1601509713697.png").similar(0.87).targetOffset(69,62)#Pattern("wcost2.png").similar(0.85).targetOffset(74,55)
ICON_COST_WHITE_3 = Pattern("wcost3.png").similar(0.95).targetOffset(51,50)
ICON_COST_WHITE_4 = Pattern("ICON_COST_WHITE_4.png").similar(0.90).targetOffset(67,73)
ICON_COST_WHITE_6 = Pattern("1601540414332.png").similar(0.87).targetOffset(76,69)
ICON_COST_WHITE_7 = Pattern("1601878254557.png").similar(0.91).targetOffset(81,72)
ICON_COST_GREEN_2 = Pattern("gcost2-1.png").similar(0.90).targetOffset(68,68)
ICON_COST_GREEN_3 = Pattern("gcost3.png").similar(0.90).targetOffset(70,67)
ICON_COST_GREEN_4 = Pattern("gcost4.png").similar(0.90).targetOffset(75,72)
ICON_COST_GREEN_5 = Pattern("gcost5.png").similar(0.90).targetOffset(92,56)
ICON_COST_GREEN_7 = Pattern("gcost7.png").similar(0.90).targetOffset(89,63)
ICON_COST_BLUE_1 = Pattern("bcost1.png").similar(0.90).targetOffset(56,50)
ICON_COST_BLUE_2 = Pattern("bcost2.png").similar(0.90).targetOffset(85,58)
ICON_COST_BLUE_3 = Pattern("bcost3.png").similar(0.90).targetOffset(87,71)
ICON_COST_BLUE_4 = Pattern("bcost4.png").similar(0.90).targetOffset(81,54)
ICON_COST_RED_2 = Pattern("1601522026475.png").similar(0.88).targetOffset(57,55)
ICON_COST_RED_3 = Pattern("rcost3.png").similar(0.90).targetOffset(74,66)
ICON_COST_RED_4 = Pattern("1601522019796.png").similar(0.87).targetOffset(73,88)
ICON_COST_RED_5 = Pattern("ICON_COST_RED_5.png").similar(0.89).targetOffset(75,67)
ICON_COST_BLACK_2 = Pattern("1601522592435.png").similar(0.88).targetOffset(83,63)
ICON_COST_BLACK_3 = Pattern("1601522894471.png").similar(0.88).targetOffset(73,66)
ICON_COST_BLACK_4 = Pattern("1601522482434.png").similar(0.86).targetOffset(80,67)
ALL_ICONS_OF_COST = [ICON_COST_WHITE_1,ICON_COST_WHITE_2,ICON_COST_WHITE_3,ICON_COST_WHITE_4,
        ICON_COST_WHITE_6,ICON_COST_GREEN_2,ICON_COST_GREEN_3,ICON_COST_GREEN_4,
        ICON_COST_GREEN_5,ICON_COST_GREEN_7,ICON_COST_BLUE_1,ICON_COST_BLUE_2,
        ICON_COST_BLUE_3,ICON_COST_BLUE_4,ICON_COST_RED_2,ICON_COST_RED_3,
        ICON_COST_RED_4,ICON_COST_BLACK_2,ICON_COST_BLACK_3,ICON_COST_BLACK_4]
ICON_MY_UNTAPPED_CREATURE = Pattern("creature.png").similar(0.90).targetOffset(5,77)
ICON_MY_UNTAPPED_CREATURE2 =Pattern("1601703910457.png").similar(0.95).targetOffset(-6,70) 
ICON_MY_UNTAPPED_BLOCKER = Pattern("1596903270708.png").similar(0.80).targetOffset(-4,74)
ICON_MY_TAPPED_CREATURE = Pattern("ICON_MY_TAPPED_CREATURE.png").similar(0.93).targetOffset(-3,67)
ICON_ENEMY_UNTAPPED_CREATURE = Pattern("1596934367665.png").similar(0.90).targetOffset(10,59) 
ICON_ENEMY_UNTAPPED_BLOCKER = "1601976850151.png"
ICON_ENEMY_TAPPED_CREATURE_1 = Pattern("1596934765015.png").similar(0.85).targetOffset(0,56)
ICON_ENEMY_TAPPED_CREATURE_2 = Pattern("1601607576805.png").similar(0.80).targetOffset(-13,-41)
ICON_W_BREAKER = Pattern("ICON_W_BREAKER.png").similar(0.90).targetOffset(-65,39)
MESSAGE_SELECT_OWN_CREATURE = Pattern("MESSAGE_SELECT_OWN_CREATURE.png").similar(0.91)
MESSAGE_SELECT_OWN_CREATURE2 = Pattern("1601552601695.png").similar(0.87)
ICON_ENEMY_CARD_COUNT = Pattern("1596771916374.png").targetOffset(-4,-2)
TARGET_POSITION_SUMMON = Pattern("1596771916374.png").targetOffset(-430,221)
TARGET_POSITION_CHARGE = Pattern("1596771322109.png").targetOffset(25,-78)
TARGET_POSITION_DIRECT_ATTACK = Pattern("1596770245448.png").targetOffset(-419,68)
TARGET_POSITION_FIRST_SHIELD = Pattern("1596770307126.png").targetOffset(-246,-522)
TARGET_POSITION_SECOND_SHIELD = Pattern("1596770307126-1.png").targetOffset(246,-515)
MESSAGE_NO_CREATURE_SELECTED = "MESSAGE_NO_CREATURE_SELECTED.png"

MESSAGE_EFFECT = Pattern("1596934235569.png").similar(0.88)
MESSAGE_BOUNCE = Pattern("1596934544674.png").similar(0.88)
MESSAGE_TAP = Pattern("MESSAGE_TAP.png").similar(0.85)
MESSAGE_DEST = "1601976850151.png"
MESSAGE_CHOOSE_BLOCKER = "1601976850151.png"
MESSAGE_SELECT = "MESSAGE_SELECT.png"
MESSAGE_RETIRE = "1598228582187.png"
MESSAGE_BLOCK = "1596775378272.png"
MESSAGE_ST = "1596770856485.png"
MESSAGE_SHIELD = "1596770897993.png"
MESSAGE_SELECT_BREAK_ENEMY_SHIELD = Pattern("1601881682724.png").similar(0.85)
BUTTON_BLOCK = "1596903354174.png"
BUTTON_NOBLOCK = "1596775410348.png"
BUTTON_ST = Pattern("1596770865154.png").targetOffset(221,-1)
BUTTON_NOST = Pattern("1596770865154.png").targetOffset(-213,0)
TITLE_HAND1 = Pattern("1601545045624.png").similar(0.90).targetOffset(224,213)
TITLE_HAND2 = Pattern("1601545045624.png").similar(0.90).targetOffset(438,217)
################BATTLE RESULT#################
ICON_WIN = "ICON_WIN.png"
ICON_LOSE = "ICON_LOSE.png"
