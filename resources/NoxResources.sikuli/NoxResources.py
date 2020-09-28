# -*- coding: utf-8 -*-
from sikuli import *
#################Constants###############
APP_ENGINE = "NOX"
#################DECKS###############
DECKIMAGE_RED_BLACK = Pattern("1598939664217.png").similar(0.85)
DECKIMAGE_ST = Pattern("1596892120520-1.png").similar(0.90)
DECKIMAGE_LARGE_CREATURE = "1599784444953.png"#Pattern("1596892035465.png").similar(0.90)
DECKIMAGE_STSPELL = "1598831170897.png"
DECKIMAGE_SPBATTLE = "MESSAGE_LAST_SP_BATTLE.png"
DECKIMAGE_MAIN = "MESSAGE_LAST_SP_BATTLE.png"
##############NoxPlayer Home#################
ICON_DMP = "ICON_DMP.png"
ICON_BROWSER = "ICON_BROWSER.png"
ICON_SETTINGS = "settingIcon.png"
BUTTON_CLOSE_DMP = Pattern("closeIconBlack.png").targetOffset(358,1)
ICON_WINDOW = "windowIcon.png"
ICON_BACK = Pattern("backIcon.png").similar(0.80)
IMG_NO_TASKS = "noTasksIcon.png"
MESSAGE_FAILED_TO_START_LAUNCHER = Pattern("1600043514936.png").targetOffset(-205,56)
MESSAGE_BACKUP = Pattern("MESSAGE_BACKUP.png").targetOffset(-79,47)
MESSAGE_BACKUP_NODISP = "MESSAGE_BACKUP_NODISP.png"
BUTTON_NOX_OK = Pattern("BUTTON_NOX_OK.png").targetOffset(71,-1)
BUTTON_ALLOW = Pattern("BUTTON_ALLOW.png").targetOffset(61,1)
MESSAGE_CONFIRM_ALLOW = "MESSAGE_CONFIRM_ALLOW.png"
BUTTON_ALLOW_BLUE = "BUTTON_ALLOW_BLUE.png"
AVIRA = "AVIRA.png"
#################DMP Common###############
BUTTON_TAKEOVER = Pattern("1596765489772.png").targetOffset(-257,83)
BUTTON_SKIP = Pattern("skip.png").similar(0.91)
BUTTON_OK = Pattern("OK.png").similar(0.81)
BUTTON_RETRY = "1596901274897.png"
BUTTON_AGREE = "1597913007417.png"
BUTTON_SMALL_OK = Pattern("smallOK.png").similar(0.84)
BUTTON_CANCEL = Pattern("1596765861356.png").similar(0.84)
BUTTON_SMALL_BATTLE_START = "1596767585645.png"
BUTTON_LARGE_BATTLE_START = "1596767599082.png"
BUTTON_BACK = "1596962178461.png" 
BUTTON_BACK2 = Pattern("1596962178461.png").similar(0.85).targetOffset(-3,69) 

BUTTON_CLOSE = "1596776234501.png"
BUTTON_TAP_AND_NEXT = "TAP_AND_NEXT.png"

#################HOME####################
ICON_HOME = Pattern("1596765614417.png").similar(0.85)
ICON_SOLO_PLAY = Pattern("1596767681008.png").similar(0.80)
ICON_MISSION = "1596775980978.png"
ICON_PRESENT_WITH_SIGN = Pattern("ICON_PRESENT_SIGN.png").similar(0.95).targetOffset(-16,20)
ICON_OTHER = "1600519768850.png"
BUTTON_MAIN_STORY = "1596767702129.png"
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
TITLE_ITEM = Pattern("1600524382930.png").targetOffset(268,239)
TITLE_ITEM_DRAG = Pattern("1601009165140.png").targetOffset(372,392)
TITLE_ITEM_DROP = Pattern("1601009179822.png").targetOffset(359,68)
BUTTON_OTHER = "1600525368575.png"
TITLE_GOLD = Pattern("1600525512184.png").similar(0.85)
TITLE_DMPOINT = "1600525496880.png"
#################MainStory####################
TITLE_MAIN_STORY = "1596767550917.png"
TITLE_MAIN_STORY2 = Pattern("1596767550917.png").targetOffset(-167,290)
TUTORIAL_MAIN_STORY = "1596767507281.png"
TITLE_EP1 = Pattern("1596989223358.png").similar(0.87)
TITLE_EP1_LOW_RESOLUTION = Pattern("1597203982188.png").similar(0.92)
EPISODES = [{"EPISODE":1, "IMAGE":Pattern("1601271450420.png").similar(0.90)},
        {"EPISODE":2, "IMAGE":Pattern("1601271478062.png").similar(0.90)},
        {"EPISODE":3, "IMAGE":Pattern("1601271490536.png").similar(0.90)},
        {"EPISODE":4, "IMAGE":Pattern("1601271503367.png").similar(0.90)},
        {"EPISODE":5, "IMAGE":Pattern("1601271519805.png").similar(0.90)}]
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
MESSAGE_LAST_SP_BATTLE = "MESSAGE_LAST_SP_BATTLE.png"
MESSAGE_LAST_BATTLE = "1598356619089.png"
#AD = Pattern("1596767400207.png").similar(0.85)
AD = Pattern("AD2.png").similar(0.80)
MESSAGE_NO_OPPONENTS = "MESSAGE_LAST_SP_BATTLE.png"
MESSAGE_CONNECTION_LOST = "MESSAGE_LAST_SP_BATTLE.png"
MESSAGE_ERROR_9003 = "MESSAGE_LAST_SP_BATTLE.png"
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
MISSION_WIN_5={"GROUP":"SPEED","NAME":"MISSION_WIN_5","IMAGE":Pattern("Win5Times-1.png").similar(0.85)}
MISSION_CREATURE_10={"GROUP":"SPEED","NAME":"MISSION_CREATURE_10","IMAGE":Pattern("Summon10Creatures-1.png").similar(0.85)}
MISSION_CREATURE_18_LOWER5={"GROUP":"SPEED","NAME":"MISSION_CREATURE_18_LOWER5","IMAGE":Pattern("Summon18Creatures-1.png").similar(0.85)}
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
MISSION_DUEL_5={"GROUP":"RETIRE","NAME":"MISSION_DUEL_5","IMAGE":Pattern("FiveTimesBattle-1.png").similar(0.86)}

#SKIP
MISSION_SUMMON_3_SHINKA={"GROUP":"SKIP","NAME":"MISSION_SUMMON_3_SHINKA","IMAGE":Pattern("1596776105685.png").similar(0.85)}
MISSION_SPELL_3_HIGHER5={"GROUP":"SKIP","NAME":"MISSION_SPELL_3_HIGHER5","IMAGE":Pattern("FourTimesBigSpell-1.png").similar(0.85)}


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
        MISSION_DUEL_5,
        MISSION_SUMMON_3_SHINKA,
        MISSION_SPELL_3_HIGHER5
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
ICON_MANA_0 = Pattern("mana0_beforeCharge.png").similar(0.95)
ICON_MANA_1 = Pattern("mana1.png").similar(0.95)
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
MANA_ICONS = [ICON_MANA_0, ICON_MANA_1, ICON_MANA_2, ICON_MANA_3, ICON_MANA_4, ICON_MANA_5, ICON_MANA_6, ICON_MANA_7, ICON_MANA_8, ICON_MANA_9, ICON_MANA_10, ICON_MANA_11]
ICON_COST_WHITE_1 = Pattern("wcost1.png").similar(0.85).targetOffset(81,51)
ICON_COST_WHITE_2 = Pattern("wcost2.png").similar(0.85).targetOffset(74,55)
ICON_COST_WHITE_3 = Pattern("wcost3.png").similar(0.95).targetOffset(51,50)
ICON_COST_WHITE_4 = Pattern("wcost4.png").similar(0.90).targetOffset(89,77)
ICON_COST_WHITE_6 = Pattern("wcost6.png").similar(0.95).targetOffset(48,53)
ICON_COST_GREEN_2 = Pattern("gcost2.png").similar(0.90).targetOffset(83,55)
ICON_COST_GREEN_3 = Pattern("gcost3.png").similar(0.90).targetOffset(70,67)
ICON_COST_GREEN_4 = Pattern("gcost4.png").similar(0.90).targetOffset(75,72)
ICON_COST_GREEN_5 = Pattern("gcost5.png").similar(0.90).targetOffset(92,56)
ICON_COST_GREEN_7 = Pattern("gcost7.png").similar(0.90).targetOffset(89,63)
ICON_COST_BLUE_1 = Pattern("bcost1.png").similar(0.90).targetOffset(56,50)
ICON_COST_BLUE_2 = Pattern("bcost2.png").similar(0.90).targetOffset(85,58)
ICON_COST_BLUE_3 = Pattern("bcost3.png").similar(0.90).targetOffset(87,71)
ICON_COST_BLUE_4 = Pattern("bcost4.png").similar(0.90).targetOffset(81,54)
ICON_COST_RED_2 = Pattern("rcost2.png").similar(0.90).targetOffset(69,63)
ICON_COST_RED_3 = Pattern("rcost3.png").similar(0.90).targetOffset(74,66)
ICON_COST_RED_4 = Pattern("rcost4.png").similar(0.90).targetOffset(76,74)
ICON_COST_BLACK_2 = Pattern("kcost2.png").similar(0.90).targetOffset(75,64)
ICON_COST_BLACK_3 = Pattern("kcost3.png").similar(0.90).targetOffset(64,74)
ICON_COST_BLACK_4 = Pattern("kcost4.png").similar(0.90).targetOffset(71,67)
ALL_ICONS_OF_COST = [ICON_COST_WHITE_1,ICON_COST_WHITE_2,ICON_COST_WHITE_3,ICON_COST_WHITE_4,
        ICON_COST_WHITE_6,ICON_COST_GREEN_2,ICON_COST_GREEN_3,ICON_COST_GREEN_4,
        ICON_COST_GREEN_5,ICON_COST_GREEN_7,ICON_COST_BLUE_1,ICON_COST_BLUE_2,
        ICON_COST_BLUE_3,ICON_COST_BLUE_4,ICON_COST_RED_2,ICON_COST_RED_3,
        ICON_COST_RED_4,ICON_COST_BLACK_2,ICON_COST_BLACK_3,ICON_COST_BLACK_4]
ICON_MY_UNTAPPED_CREATURE = Pattern("creature.png").similar(0.90).targetOffset(5,77)
ICON_MY_UNTAPPED_BLOCKER = Pattern("1596903270708.png").similar(0.80).targetOffset(-4,74)
ICON_ENEMY_UNTAPPED_CREATURE = Pattern("1596934367665.png").similar(0.90).targetOffset(10,59) 
ICON_ENEMY_TAPPED_CREATURE_1 = Pattern("1596934765015.png").similar(0.85).targetOffset(0,56)
ICON_ENEMY_TAPPED_CREATURE_2 = Pattern("1596935014118.png").similar(0.90).targetOffset(-1,54)
TARGET_POSITION_SUMMON = Pattern("1596771916374.png").targetOffset(-430,221)
TARGET_POSITION_CHARGE = Pattern("1596771322109.png").targetOffset(25,-78)
TARGET_POSITION_DIRECT_ATTACK = Pattern("1596770245448.png").targetOffset(-419,68)
TARGET_POSITION_FIRST_SHIELD = Pattern("1596770307126.png").targetOffset(-244,-376)
TARGET_POSITION_SECOND_SHIELD = Pattern("1596770307126-1.png").targetOffset(241,-386)

MESSAGE_EFFECT = Pattern("1596934235569.png").similar(0.88)
MESSAGE_BOUNCE = Pattern("1596934544674.png").similar(0.88)
MESSAGE_RETIRE = "1598228582187.png"
MESSAGE_BLOCK = "1596775378272.png"
MESSAGE_ST = "1596770856485.png"
MESSAGE_SHIELD = "1596770897993.png"
BUTTON_BLOCK = "1596903354174.png"
BUTTON_NOBLOCK = "1596775410348.png"
BUTTON_ST = Pattern("1596770865154.png").targetOffset(221,-1)
