# -*- coding: utf-8 -*-
from sikuli import *
#################Constants###############
APP_ENGINE = "ANDAPP"
#################DECKS###############
DECKIMAGE_RED_BLACK = Pattern("1598888491089.png").similar(0.85)
DECKIMAGE_ST = "MESSAGE_LAST_SP_BATTLE.png"
DECKIMAGE_LARGE_CREATURE = "MESSAGE_LAST_SP_BATTLE-1.png"
DECKIMAGE_STSPELL = "MESSAGE_LAST_SP_BATTLE-2.png"
DECKIMAGE_SPBATTLE = "1599121629375.png"
DECKIMAGE_MAIN = "DECKIMAGE_MAIN.png"
#################DMP Common###############
BUTTON_TAKEOVER = Pattern("1594988274658.png").targetOffset(-162,150)
BUTTON_OK = "1599121509243.png"
BUTTON_OK2 = "BUTTON_OK2.png"
BUTTON_CANCEL = "1595384685180.png"
BUTTON_RETRY = "1599209156392.png"
BUTTON_SMALL_BATTLE_START = "1595253571082-1.png"
BUTTON_SMALL_OK = "BUTTON_SMALL_OK.png"
BUTTON_LARGE_BATTLE_START = "1595253595048-1.png"
BUTTON_SKIP = Pattern("1595412556275.png").similar(0.90)
BUTTON_BACK = "1599470984365.png"
BUTTON_BACK2 = Pattern("1599470984365-1.png").targetOffset(0,46)
BUTTON_CLOSE = "BUTTON_CLOSE.png"
BUTTON_TAP_AND_NEXT = "MESSAGE_LAST_SP_BATTLE-5.png"

#################HOME####################
ICON_HOME = Pattern("1594989699401.png").similar(0.60).targetOffset(178,-50)
ICON_SOLO_PLAY = "ICON_SOLO_PLAY.png"
ICON_EXTRA = "1595253546948.png"
ICON_MISSION = "ICON_MISSION.png"
BUTTON_MAIN_STORY = "1595065859928.png"
BUTTON_LEGEND_BATTLE = Pattern("1595993039410.png").similar(0.90)
#################LegendBattle####################
ICON_TARGET_REWARD = "1600702754259.png"
ICON_NEXT_REWARD_OF_TARGET = "1600777270163.png"
ICON_REWARD_COMPLETED = "ICON_REWARD_COMPLETED.png"
TITLE_LEGEND_STAGE1 = "1600697998210.png"
TITLE_LEGEND_STAGE2 = "1600700956975.png" 
TITLE_LEGEND_STAGE3 = "1600700995819.png"
#################MainStory####################
BACKGROUND_EPISODE_LIST = "1600267657384.png"
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

STAGES = [{"STAGE":1, "IMAGE":"1601273304749.png"},
            {"STAGE":2, "IMAGE":"1601273322817.png"},
            {"STAGE":3, "IMAGE":"1601273332295.png"},
            {"STAGE":4, "IMAGE":"1601273363595.png"},
            {"STAGE":5, "IMAGE":"1601273374501.png"},
            {"STAGE":6, "IMAGE":"1601273384379.png"},
            {"STAGE":7, "IMAGE":"1601273397340.png"},
            {"STAGE":8, "IMAGE":"1601273410662.png"},
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
ICON_COST_WHITE_1 = "ICON_COST_WHITE_1.png"
ICON_COST_WHITE_2 = Pattern("wcost2-1.png").similar(0.85).targetOffset(68,61)
ICON_COST_WHITE_3 = "ICON_COST_WHITE_1.png"
ICON_COST_WHITE_4 = Pattern("wcost4-1.png").similar(0.90).targetOffset(72,61)
ICON_COST_WHITE_6 = Pattern("ICON_COST_WHITE_6.png").similar(0.87).targetOffset(63,55)
ICON_COST_GREEN_2 = Pattern("1594950595616-1.png").similar(0.85).targetOffset(79,55)
ICON_COST_GREEN_3 = Pattern("1595029444929-1.png").similar(0.90).targetOffset(67,55)
ICON_COST_GREEN_4 = Pattern("1594949422218-1.png").similar(0.83).targetOffset(69,54)
ICON_COST_GREEN_5 = Pattern("1595030120503-1.png").similar(0.90).targetOffset(75,56)
ICON_COST_GREEN_7 = Pattern("1596192523218.png").similar(0.90).targetOffset(55,41)
ICON_COST_BLUE_1 = "ICON_COST_WHITE_1.png"
ICON_COST_BLUE_2 = "ICON_COST_WHITE_1.png"
ICON_COST_BLUE_3 = "ICON_COST_WHITE_1.png"
ICON_COST_BLUE_4 = "ICON_COST_WHITE_1.png"
ICON_COST_RED_2 = Pattern("rcost2-1.png").similar(0.90).targetOffset(64,59)
ICON_COST_RED_3 = Pattern("rcost3-1.png").similar(0.90).targetOffset(67,54)
ICON_COST_RED_4 = Pattern("rcost4-1.png").similar(0.90).targetOffset(66,56)
ICON_COST_RED_5 = Pattern("1601596117607.png").similar(0.90).targetOffset(62,65)

ICON_COST_BLACK_2 = Pattern("kcost2-1.png").similar(0.90).targetOffset(61,61)
ICON_COST_BLACK_3 = Pattern("kcost3-1.png").similar(0.90).targetOffset(64,55)
ICON_COST_BLACK_4 = Pattern("kcost4-1.png").similar(0.90).targetOffset(61,53)
ICON_ENEMY_CARD_COUNT = Pattern("1594957113274.png").targetOffset(11,1)
TARGET_POSITION_DIRECT_ATTACK = Pattern("1594957113274-1.png").targetOffset(-371,82)
DESIGN_CARD_BACKSIDE_NORMAL = Pattern("1594948414271.png").similar(0.60)
TARGET_POSITION_FIRST_SHIELD = Pattern("1594948424162.png").targetOffset(-170,-387)
TARGET_POSITION_SECOND_SHIELD = Pattern("1594948424162-1.png").targetOffset(185,-379)
ICON_W_BREAKER = Pattern("1597610313690.png").similar(0.80).targetOffset(-53,30)
ICON_MY_UNTAPPED_CREATURE = Pattern("1594978601821.png").similar(0.97).targetOffset(1,63)
ICON_MY_UNTAPPED_BLOCKER = Pattern("1597156496305.png").similar(0.80).targetOffset(0,26)
ICON_MY_TAPPED_CREATURE = Pattern("1598096217499.png").similar(0.90).targetOffset(1,64)
ICON_ENEMY_UNTAPPED_CREATURE = Pattern("1597464166732.png").similar(0.85).targetOffset(0,51)
ICON_ENEMY_UNTAPPED_BLOCKER = Pattern("1601365170781.png").similar(0.85).targetOffset(-1,50)
ICON_ENEMY_TAPPED_CREATURE_1 = Pattern("1598791717218.png").similar(0.85).targetOffset(-2,28)
ICON_ENEMY_TAPPED_CREATURE_2 = "ICON_COST_WHITE_1.png"
MESSAGE_SELECT_OWN_CREATURE = Pattern("1594952630070.png").similar(0.95).targetOffset(-20,-217)
MESSAGE_SELECT_OWN_CREATURE2 = "ICON_COST_WHITE_1.png"
MESSAGE_NO_CREATURE_SELECTED = "1597464225195.png"
MESSAGE_EFFECT = "ICON_COST_WHITE_1.png"
MESSAGE_BOUNCE = "ICON_COST_WHITE_1.png"
MESSAGE_TAP = Pattern("TAP_QUESTION.png").similar(0.90)
MESSAGE_DEST = Pattern("DES_QUESTION.png").similar(0.90)
MESSAGE_CHOOSE_BLOCKER = Pattern("BLOCK_QUESTION2.png").similar(0.90)
MESSAGE_RETIRE = "ICON_COST_WHITE_1.png"
MESSAGE_BLOCK = Pattern("Block.png").similar(0.86)
MESSAGE_ST = "ICON_COST_WHITE_1.png"
MESSAGE_SHIELD = Pattern("CheckShield.png").similar(0.88)
MESSAGE_SELECT_BREAK_ENEMY_SHIELD = "ICON_COST_WHITE_1.png"
BUTTON_BLOCK = "1597156569299.png"
BUTTON_NOBLOCK = Pattern("1597133736767.png").similar(0.89)
BUTTON_ST = Pattern("1594949527193.png").similar(0.94).targetOffset(195,5)
TITLE_HAND1 = Pattern("1595035924385.png").similar(0.92).targetOffset(363,188)
TITLE_HAND2 = Pattern("1595035924385-1.png").similar(0.92).targetOffset(174,190)
################BATTLE RESULT#################
ICON_WIN = "1595034514931.png"
ICON_LOSE = "1599561314584.png"
##################MISSION################
TITLE_MISSION =  "TITLE_MISSION.png"
