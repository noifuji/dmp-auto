# -*- coding: utf-8 -*-
from sikuli import *
#################Constants###############
APP_ENGINE = "ANDAPP"
#################DECKS###############
DECKIMAGE_RED_BLACK = Pattern("1598888491089.png").similar(0.85)
DECKIMAGE_ST = "MESSAGE_LAST_SP_BATTLE.png"
DECKIMAGE_LARGE_CREATURE = "MESSAGE_LAST_SP_BATTLE-1.png"
DECKIMAGE_STSPELL = "MESSAGE_LAST_SP_BATTLE-2.png"
DECKIMAGE_SPBATTLE = "1604575374708.png"
DECKIMAGE_MAIN = "DECKIMAGE_MAIN.png"
DECKIMAGE_FATTY = "1603892435907.png"
#################DMP Common###############
MESSAGE_MAINTENANCE ="1603341203261.png"
BUTTON_TAKEOVER = Pattern("1594988274658.png").targetOffset(-162,150)
BUTTON_MENU = "1602164588516.png"
BUTTON_CLEAR_CACHE = "1602164597869.png"
BUTTON_OK = "1599121509243.png"
BUTTON_OK2 = "BUTTON_OK2.png"
BUTTON_OK3 = "1601892415582.png"
BUTTON_OK4 = Pattern("BUTTON_OK2.png").similar(0.85)
BUTTON_CANCEL = "1595384685180.png"
BUTTON_RETRY = "1599209156392.png"
BUTTON_LATER = "MESSAGE_LAST_SP_BATTLE-1.png"
BUTTON_SMALL_BATTLE_START = "1595253571082-1.png"
BUTTON_SMALL_OK = "BUTTON_SMALL_OK.png"
BUTTON_LARGE_BATTLE_START = "1595253595048-1.png"
BUTTON_DUEL_HISTORY = Pattern("1601609811737.png").similar(0.90)
TITLE_DUEL_HISTORY = Pattern("1601609821011.png").similar(0.89)
BUTTON_RESULT = Pattern("1601609826458.png").similar(0.89)
BUTTON_SKIP = Pattern("1595412556275.png").similar(0.90)
BUTTON_BACK = "1599470984365.png"
BUTTON_BACK2 = Pattern("1599470984365-1.png").targetOffset(0,46)
BUTTON_CLOSE = "BUTTON_CLOSE.png"
BUTTON_TAP_AND_NEXT = "MESSAGE_LAST_SP_BATTLE-5.png"

#################HOME####################
ICON_HOME = "1604575287169.png"
ICON_SOLO_PLAY = "1604575291742.png"
ICON_EXTRA = "1604575296220.png"
ICON_MISSION ="1604575302873.png"
BUTTON_MAIN_STORY = "1595065859928.png"
BUTTON_LEGEND_BATTLE = Pattern("1595993039410.png").similar(0.90)
BUTTON_SP_BATTLE = "1595253556265.png"
#################LegendBattle####################
ICON_TARGET_REWARD = Pattern("1600702754259.png").similar(0.90)
ICON_SP_TARGET_REWARD = "MESSAGE_LAST_SP_BATTLE-3.png"
ICON_NEXT_REWARD_OF_TARGET = "1600777270163.png"
ICON_REWARD_COMPLETED = "MESSAGE_LAST_SP_BATTLE-3.png"#"ICON_REWARD_COMPLETED.png"
TITLE_LEGEND_STAGE1 = "1600697998210.png"
TITLE_LEGEND_STAGE2 = "1600700956975.png" 
TITLE_LEGEND_STAGE3 = "1600700995819.png"
#################MainStory####################
BACKGROUND_EPISODE_LIST = "1604575347680.png"
TITLE_MAIN_STORY = "1595205824088.png"
TITLE_MAIN_STORY2 = Pattern("1595205824088.png").targetOffset(-1,190)
TUTORIAL_MAIN_STORY = Pattern("1596699277800.png").similar(0.85)
TITLE_EP1 = Pattern("TITLE_EP1.png").similar(0.90)
TITLE_EP2 = Pattern("1600993417708.png").similar(0.90).targetOffset(32,33)
TITLE_EP3 = Pattern("1600993398929.png").similar(0.90).targetOffset(40,35)
TITLE_EP4 = Pattern("1600993347115.png").similar(0.90).targetOffset(40,38)
TITLE_EP5 = Pattern("1600993226909.png").similar(0.90).targetOffset(35,35)
EPISODES = [{"EPISODE":1, "IMAGE":TITLE_EP1},
        {"EPISODE":2, "IMAGE":TITLE_EP2},
        {"EPISODE":3, "IMAGE":TITLE_EP3},
        {"EPISODE":4, "IMAGE":TITLE_EP4},
        {"EPISODE":5, "IMAGE":TITLE_EP5}]

TITLE_EP1_LOW_RESOLUTION = "MESSAGE_LAST_SP_BATTLE-5.png"
BUTTON_EP1 = "MESSAGE_LAST_SP_BATTLE-6.png"
TITLE_EP2_STAGE21 = Pattern("1598845360896.png").similar(0.95)
TITLE_EP2_STAGE22 = Pattern("1598845370560.png").similar(0.95)
TITLE_EP2_STAGE28 = Pattern("1598845444240.png").similar(0.95)
TITLE_EP2_STAGE29 = Pattern("1598845457074.png").similar(0.95)
TITLE_EP3_STAGE2 = Pattern("TITLE_EP3_STAGE2.png").similar(0.95)
TITLE_EP3_STAGE3 = Pattern("TITLE_EP3_STAGE3.png").similar(0.95)
TITLE_EP4_STAGE3 = Pattern("1598845041551.png").similar(0.95)
TITLE_EP4_STAGE4 = Pattern("1598845082765.png").similar(0.95)
TITLE_EP4_STAGE9 = Pattern("1598845320451.png").similar(0.95)
TITLE_EP4_STAGE10 = Pattern("1598845329738.png").similar(0.95)
TITLE_EP5_STAGE10 = Pattern("TITLE_EP5_STAGE10.png").similar(0.90)
BUTTON_CONFIRM_REWARD = "BUTTON_CONFIRM_REWARD.png"
TITLE_REWARD_INFO = "TITLE_REWARD_INFO.png"
ICON_CLEARED = Pattern("ICON_CLEARED.png").similar(0.85)

STAGE_REGION_OFFSETS = {"x":-200,"y": 240, "w":200, "h":50}
STAGES = [{"STAGE":1, "IMAGE":"1601273304749.png"},
            {"STAGE":2, "IMAGE":"1601273322817.png"},
            {"STAGE":3, "IMAGE":"1603187970895.png"},
            {"STAGE":4, "IMAGE":"1601273363595.png"},
            {"STAGE":5, "IMAGE":"1603188734460.png"},
            {"STAGE":5, "IMAGE":"1603188822771.png"},
            {"STAGE":5, "IMAGE":"1603187805700.png"},
            {"STAGE":6, "IMAGE":"1603188768017.png"},
            {"STAGE":6, "IMAGE":"1603188836979.png"},
            {"STAGE":6, "IMAGE":"1603187784409.png"},
            {"STAGE":7, "IMAGE":"1603188783164.png"},
            {"STAGE":7, "IMAGE":"1603188852776.png"},
            {"STAGE":7, "IMAGE":"1603187564243.png"},
            {"STAGE":8, "IMAGE":"1603188798521.png"},
            {"STAGE":8, "IMAGE":"1603188867410.png"},
            {"STAGE":8, "IMAGE":"1603188485226.png"},
            {"STAGE":9, "IMAGE":"1601273419500.png"},
            {"STAGE":10, "IMAGE":"1601273431022.png"},
            {"STAGE":1, "IMAGE":"1601273455215.png"},
            {"STAGE":2, "IMAGE":"1601273466864.png"},
            {"STAGE":3, "IMAGE":"1601273476533.png"},
            {"STAGE":4, "IMAGE":"1601273485649.png"},
            {"STAGE":5, "IMAGE":"1601273496066.png"},
            {"STAGE":6, "IMAGE":"1601273509144.png"},
            {"STAGE":7, "IMAGE":"1601273518963.png"},
            {"STAGE":8, "IMAGE":"1601273529028.png"},
            {"STAGE":9, "IMAGE":"1601273538343.png"},
            {"STAGE":10, "IMAGE":"1601273560551.png"},
            {"STAGE":11, "IMAGE":"1601273574274.png"},
            {"STAGE":12, "IMAGE":"1601273585081.png"},
            {"STAGE":13, "IMAGE":"1601273593564.png"},
            {"STAGE":14, "IMAGE":"1601273604202.png"},
            {"STAGE":15, "IMAGE":"1601273613114.png"},
            {"STAGE":1, "IMAGE":"1601273627960.png"},
            {"STAGE":2, "IMAGE":"1601273639025.png"},
            {"STAGE":3, "IMAGE":"1601273647004.png"},
            {"STAGE":4, "IMAGE":"1601273657715.png"},
            {"STAGE":5, "IMAGE":"1601273667415.png"},
            {"STAGE":6, "IMAGE":"1601273694101.png"},
            {"STAGE":7, "IMAGE":"1601273708666.png"},
            {"STAGE":8, "IMAGE":"1601273717904.png"},
            {"STAGE":9, "IMAGE":"1601273732980.png"},
            {"STAGE":10, "IMAGE":"1601429793295.png"},
            {"STAGE":11, "IMAGE":"1601429690284.png"},
            {"STAGE":12, "IMAGE":"1601273766312.png"},
            {"STAGE":13, "IMAGE":"1601273775591.png"},
            {"STAGE":14, "IMAGE":"1601273785777.png"},
            {"STAGE":15, "IMAGE":"1601273797588.png"}]
##################Messages################
MESSAGE_RESTART_DUEL = Pattern("1595384665194.png").similar(0.95)
MESSAGE_LAST_SP_BATTLE = Pattern("1595284653487.png").similar(0.89)
MESSAGE_LAST_BATTLE = Pattern("1597678517843.png").similar(0.91)
AD = Pattern("1595422978334.png").similar(0.95)
MESSAGE_NO_OPPONENTS = Pattern("1595392375667.png").similar(0.90)
MESSAGE_CONNECTION_LOST = "1595641536565.png"
MESSAGE_ERROR_9003 = "1599209212713.png"
MESSAGE_DOWNLOAD = "MESSAGE_LAST_SP_BATTLE-5.png"
MESSAGE_BACK_TO_TITLE = "1604620154911.png"
##################REWARDS################
TITLE_REWARD_LEVEL_UP = "1595208660245.png"
TITLE_REWARD_DAILY = "1595216271069-1.png"
TITLE_REWARD_SECRET = "1595619705813.png"
TITLE_REWARD_CLEAR = "1595404189524.png"
TITLE_REWARD_POINT = "1595390207786.png"

#################DeckList####################
TITLE_DECKLIST = Pattern("1599122323759.png").targetOffset(151,162)
BUTTON_CREATE_NEW_DECK = "1599121451139.png"
BUTTON_CREATE_BY_CODE = "1599121459235.png"
INPUT_DECK_CODE1 = Pattern("1599121466913.png").targetOffset(1,26)
INPUT_DECK_CODE2 = "1599121484948.png"
BUTTON_SAVE_DECK = "1599121566385.png"
################DUEL#################
BUTTON_TURN_END = Pattern("1594954855862-1.png").similar(0.84)
BUTTON_TURN_END_RED = "1603869174742.png"
BUTTON_ENEMY_TURN = "1599193822994.png"
AVATOR_DEFAULT_MALE = Pattern("Avator.png").similar(0.90).targetOffset(315,1)
ICON_MANA_0 = Pattern("mana0.png").similar(0.90)
ICON_MANA_1 = Pattern("mana1.png").similar(0.90)
ICON_MANA_2 = Pattern("mana2.png").similar(0.90)
ICON_MANA_3 = Pattern("mana3.png").similar(0.90)
ICON_MANA_4 = Pattern("mana4.png").similar(0.90)
ICON_MANA_5 = Pattern("mana5.png").similar(0.94)
ICON_MANA_6 = Pattern("mana6.png").similar(0.95)
ICON_MANA_7 = Pattern("mana7.png").similar(0.91)
ICON_MANA_8 = Pattern("mana8.png").similar(0.90)
ICON_MANA_9 = Pattern("mana9.png").similar(0.95)
ICON_MANA_10 = Pattern("mana10.png").similar(0.91)
ICON_MANA_11 = Pattern("mana11.png").similar(0.90)
MANA_ICONS = [ICON_MANA_0, ICON_MANA_1, ICON_MANA_2, ICON_MANA_3, ICON_MANA_4, ICON_MANA_5, ICON_MANA_6, ICON_MANA_7]
ICON_CARD_SQUARE = Pattern("1601513510353.png").similar(0.75)#"ICON_CARD_SQUARE.png"
ICON_COST_WHITE_1 = Pattern("ICON_COST_WHITE_1.png").similar(0.90).targetOffset(64,43)
ICON_COST_WHITE_2 = Pattern("wcost2-1.png").similar(0.85).targetOffset(68,61)
ICON_COST_WHITE_3 = "MESSAGE_LAST_SP_BATTLE.png"
ICON_COST_WHITE_4 = Pattern("wcost4-1.png").similar(0.90).targetOffset(72,61)
ICON_COST_WHITE_6 = Pattern("ICON_COST_WHITE_6.png").similar(0.87).targetOffset(63,55)
ICON_COST_WHITE_7 = Pattern("ICON_COST_WHITE_7.png").similar(0.91).targetOffset(73,48)
ICON_COST_GREEN_2 = Pattern("1594950595616-1.png").similar(0.85).targetOffset(79,55)
ICON_COST_GREEN_3 = Pattern("1595029444929-1.png").similar(0.90).targetOffset(67,55)
ICON_COST_GREEN_4 = Pattern("1594949422218-1.png").similar(0.83).targetOffset(69,54)
ICON_COST_GREEN_5 = Pattern("1595030120503-1.png").similar(0.90).targetOffset(75,56)
ICON_COST_GREEN_7 = Pattern("1596192523218.png").similar(0.90).targetOffset(55,41)
ICON_COST_BLUE_1 = "MESSAGE_LAST_SP_BATTLE.png"
ICON_COST_BLUE_2 = "MESSAGE_LAST_SP_BATTLE.png"
ICON_COST_BLUE_3 = "MESSAGE_LAST_SP_BATTLE.png"
ICON_COST_BLUE_4 = "MESSAGE_LAST_SP_BATTLE.png"
ICON_COST_RED_2 = Pattern("1601810200586.png").similar(0.90).targetOffset(65,60)
ICON_COST_RED_3 = Pattern("rcost3-1.png").similar(0.90).targetOffset(67,54)
ICON_COST_RED_4 = Pattern("1601810366219.png").similar(0.90).targetOffset(70,69)
ICON_COST_RED_5 = Pattern("1601596117607.png").similar(0.90).targetOffset(62,65)

ICON_COST_BLACK_2 = Pattern("1601810645824.png").similar(0.90).targetOffset(64,60)
ICON_COST_BLACK_3 = Pattern("1601810827895.png").similar(0.90).targetOffset(63,62)
ICON_COST_BLACK_4 = Pattern("kcost4-1.png").similar(0.90).targetOffset(61,53)
ICON_ENEMY_CARD_COUNT = Pattern("1594957113274.png").targetOffset(11,1)
TARGET_POSITION_DIRECT_ATTACK = Pattern("1594957113274-1.png").targetOffset(-371,82)
DESIGN_CARD_BACKSIDE_NORMAL = Pattern("1594948414271.png").similar(0.60)
TARGET_POSITION_FIRST_SHIELD = Pattern("1594948424162.png").targetOffset(-170,-387)
TARGET_POSITION_SECOND_SHIELD = Pattern("1594948424162-1.png").targetOffset(185,-379)
ICON_W_BREAKER = Pattern("1597610313690.png").similar(0.80).targetOffset(-53,30)
ICON_MY_UNTAPPED_CREATURE = Pattern("1594978601821.png").similar(0.97).targetOffset(1,63)
ICON_MY_UNTAPPED_CREATURE2 =Pattern("1601704247474.png").similar(0.95).targetOffset(-1,54)
ICON_MY_UNTAPPED_BLOCKER = Pattern("1597156496305.png").similar(0.80).targetOffset(0,26)
ICON_MY_TAPPED_CREATURE = Pattern("1598096217499.png").similar(0.90).targetOffset(1,64)
ICON_ENEMY_UNTAPPED_CREATURE = Pattern("1597464166732.png").similar(0.85).targetOffset(0,51)
ICON_ENEMY_UNTAPPED_BLOCKER = Pattern("1601365170781.png").similar(0.85).targetOffset(-1,50)
ICON_ENEMY_TAPPED_CREATURE_1 = Pattern("1598791717218.png").similar(0.85).targetOffset(-2,28)
ICON_ENEMY_TAPPED_CREATURE_2 = Pattern("ICON_ENEMY_TAPPED_CREATURE_2.png").similar(0.85).targetOffset(-6,-37)
ICON_MY_CREATURE1 = Pattern("1602826706784.png").similar(0.90).targetOffset(-15,-47)
ICON_MY_CREATURE2 = Pattern("1602826713675.png").similar(0.90).targetOffset(-14,-46)
ICON_MY_CREATURE3 = Pattern("1602826721228.png").similar(0.90).targetOffset(-18,-43)
ICON_MY_CREATURE4 = Pattern("1602925353012.png").similar(0.88).targetOffset(-15,-43)
ICON_ENEMY_CREATURE1 = Pattern("1602826728881.png").similar(0.90).targetOffset(-7,-37)
ICON_ENEMY_CREATURE2 = Pattern("1602826735389.png").similar(0.90).targetOffset(-8,-38)
ICON_ENEMY_CREATURE3 = Pattern("1602826746486.png").similar(0.90).targetOffset(-13,-33)
ICON_ENEMY_CREATURE4 = "1601976850151.png"
MESSAGE_SELECT_OWN_CREATURE = Pattern("1594952630070.png").similar(0.95).targetOffset(-20,-217)
MESSAGE_SELECT_OWN_CREATURE2 = Pattern("MESSAGE_SELECT_OWN_CREATURE2.png").similar(0.95)
MESSAGE_NO_CREATURE_SELECTED = "1597464225195.png"
ICON_SELECTED = "1603808224278.png"
MESSAGE_EFFECT = "1602838906628.png"
MESSAGE_BOUNCE = "MESSAGE_BOUNCE.png"
MESSAGE_TAP = "TAP_QUESTION.png"
MESSAGE_DEST = "1602862907474.png"
MESSAGE_BOUNCE = "1602826851330.png"
MESSAGE_MANA = "1602826590510.png"
MESSAGE_CHOOSE_BLOCKER = "BLOCK_QUESTION2.png"
MESSAGE_RETIRE = "MESSAGE_RETIRE.png"
MESSAGE_BLOCK = "Block.png"
MESSAGE_ST = "MESSAGE_ST.png"
MESSAGE_SHIELD = Pattern("CheckShield.png").similar(0.88)
MESSAGE_SELECT = "1602838952232.png"
MESSAGE_SELECT_BREAK_ENEMY_SHIELD = Pattern("MESSAGE_SELECT_BREAK_ENEMY_SHIELD.png").similar(0.85)
BUTTON_BLOCK = "1597156569299.png"
BUTTON_NOBLOCK = Pattern("1597133736767.png").similar(0.89)
BUTTON_ST = Pattern("1594949527193.png").similar(0.78).targetOffset(195,5)
BUTTON_NOST = Pattern("1594949527193.png").similar(0.94).targetOffset(-182,1)
TITLE_HAND1 = Pattern("1595035924385.png").similar(0.92).targetOffset(363,188)
TITLE_HAND2 = Pattern("1595035924385-1.png").similar(0.92).targetOffset(174,190)
################BATTLE RESULT#################
ICON_WIN = "1595034514931.png"
ICON_LOSE = "1599561314584.png"
##################MISSION################
TITLE_MISSION =  "TITLE_MISSION.png"
