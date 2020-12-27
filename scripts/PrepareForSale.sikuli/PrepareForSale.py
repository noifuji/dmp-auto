import sys
import traceback
from datetime import datetime
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import GameLib
import CommonDMLib
import NoxResources
from driveapis import DriveApis
from spreadsheetapis import SpreadSheetApis

def captureImage(keyImage, offsetY, width, height):
    keyImageObj = findAny(keyImage)
    if len(keyImageObj) <= 0:
        raise Exception("failed to detect CardList")
    keyImageX = keyImageObj[0].getX()
    keyImageY = keyImageObj[0].getY()
    region = Region(keyImageX,keyImageY + offsetY,width,height)
    region.highlight(0.1)
    return SCREEN.capture(region)

def filterCardList(rarities, dmpps):
    click(Pattern("1596590519784.png").similar(0.90))
    wait(0.2)
    click("1599973746387.png")
    wait(0.2)
    for r in rarities:
        click(r["IMAGE"])
    wait(1)
    wheel(Pattern("1599973746387.png").targetOffset(227,-209), Button.WHEEL_DOWN, 10)
    wait(5)
    for dmpp in dmpps:
        click(dmpp)
    click("1596590612922.png")
    waitVanish("1596590612922.png", 60)

appname = 'PREPARE'
Settings.MoveMouseDelay = 0.1
drive = DriveApis("DMPAuto", CommonDMLib.getCredentials())
sheets = SpreadSheetApis("DMPAuto", CommonDMLib.getCredentials())
try:
    ref = input("Enter Ref")
    allDivDeckCodeRaw = input("Enter All Division Deck Code(ex>XXXXX,YYYYY,ZZZZZ)")
    newDivDeckCodeRaw = input("Enter New Division Deck Code(ex>XXXXX,YYYYY,ZZZZZ)")
    if allDivDeckCodeRaw == "":
        allDivDeckCodes = []
    else:
        allDivDeckCodes = allDivDeckCodeRaw.split(",")

    if newDivDeckCodeRaw == "":
        newDivDeckCodes = []
    else:
        newDivDeckCodes = newDivDeckCodeRaw.split(",")

    rawData = sheets.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, "status!A2:F3000", "ROWS")
    rawData = rawData if not rawData == None else []
    availableRefs = []
    for raw in rawData:
        if raw[0] == ref and raw[1] == "sold":
            print "This ref was already sold. Don't open."
            exit()
    
    if not CommonDMLib.isNoxOn():
        print "MAIN is off"
        CommonDMLib.RestartNox(NoxResources, "MAIN")
    CommonDMLib.loadRef(NoxResources, ref, drive)
    CommonDMLib.RestartApp(NoxResources)
    
    fId = drive.createFolder(str(ref), "1ApCg9taRAEmK7QH93bxmoIzMbRaC_r7m")

    for deckCodes, btnDiv in zip([allDivDeckCodes, newDivDeckCodes],[NoxResources.BUTTON_ORGANIZE_ALLDIV_DECK, NoxResources.BUTTON_ORGANIZE_NEWDIV_DECK]):
        #全てのデッキを削除
        for openCardListLoop in range(100):
            if len(findAny(NoxResources.ICON_CARD)) > 0:
                try:
                    click(NoxResources.ICON_CARD)
                except:
                    print "failed to click"
                wait(1)
            if len(findAny(NoxResources.BUTTON_ORGANIZE_DECK)) > 0:
                try:
                    click(NoxResources.BUTTON_ORGANIZE_DECK)
                except:
                    print "failed to click"
                wait(1)
            if len(findAny(btnDiv)) > 0:
                try:
                    click(btnDiv)
                except:
                    print "failed to click"
                wait(1)
            if len(findAny("1596780703269.png")) > 0:
                break
                    
        for deleteDeck in range(30):
            if exists("1597553140601.png", 1) != None:
                break
            click("1596780671063.png")
            wait(2)
            click("1596780684705.png")
            wait(5)
        exists("1596780703269.png",60)
        for deckCode in deckCodes:
            #対象のデッキを作成する。
            CommonDMLib.addNewDeckByCode(NoxResources, deckCode)
            click("1603869466863-1.png")
            exists(NoxResources.TITLE_DECK, 60)
            image = captureImage(NoxResources.TITLE_DECK, 45, 1270, 650)
            print image.getFilename()
            drive.uploadFile("DeckImage_" + deckCode + ".png", image.getFilename(), fId, "image/png")
            type(Key.ESC)
            waitVanish(NoxResources.TITLE_DECK, 60)
        
        type(Key.ESC)
    exists(NoxResources.ICON_SOLO_PLAY, 60)
    click(Pattern("1596593310453.png").targetOffset(-2,-214))
    if exists("1596593154431.png", 120) != None:
        for listTutorialLoop in range(10):
            click(Pattern("1596593154431.png").targetOffset(-2,47))
            wait(0.2)
    
    TARGET_RARITY = [{"NAME":"VR", "IMAGE":NoxResources.BUTTON_RARITY_VERYRARE}, 
            {"NAME":"SR", "IMAGE":NoxResources.BUTTON_RARITY_SUPERRARE}]
    TARGET_DMPP = [[NoxResources.BUTTON_DMPP01, NoxResources.BUTTON_DMPP02,NoxResources.BUTTON_DMPP03], 
            [NoxResources.BUTTON_DMPP04, NoxResources.BUTTON_DMPP05,NoxResources.BUTTON_DMPP06,NoxResources.BUTTON_DMPP07]]
    for rarity in TARGET_RARITY:
        filterCardList([rarity], TARGET_DMPP[0] + TARGET_DMPP[1])
        if exists(NoxResources.SCROLL1,1) == None:
            image = captureImage(NoxResources.TITLE_CARD_LIST, 47, 1340, 620)
            drive.uploadFile(rarity["NAME"] + ".png", image.getFilename(), fId, "image/png")
        else:
            for i in range(len(TARGET_DMPP)):
                filterCardList([rarity], TARGET_DMPP[i])
                image = captureImage(NoxResources.TITLE_CARD_LIST, 47, 1340, 620)
                drive.uploadFile(rarity["NAME"] + str(i+1) +  ".png", image.getFilename(), fId, "image/png")
    #PRIZE
    TARGET_RARITY = [[{"NAME":"VR", "IMAGE":NoxResources.BUTTON_RARITY_VERYRARE}], 
            [{"NAME":"C", "IMAGE":NoxResources.BUTTON_RARITY_COMMON},
                {"NAME":"UC", "IMAGE":NoxResources.BUTTON_RARITY_UNCOMMON},
                {"NAME":"R", "IMAGE":NoxResources.BUTTON_RARITY_RARE}]]
    for i in range(len(TARGET_RARITY)):
        filterCardList(TARGET_RARITY[i], ["1607823678517.png"])
        image = captureImage(NoxResources.TITLE_CARD_LIST, 47, 1340, 620)
        drive.uploadFile("PRIZE" + str(i) + ".png", image.getFilename(), fId, "image/png")
    
    cardCountResult = CommonDMLib.countAllCardsByRarity(NoxResources)
    CommonDMLib.updateCardCount(sheets, ref, cardCountResult["NAMES"], cardCountResult["CARDS"])
    type(Key.ESC)
    exists(NoxResources.ICON_SOLO_PLAY, 60)
    res = CommonDMLib.scanAccountInfo(NoxResources)
    CommonDMLib.updateAccountInfo(sheets, ref, res[0], res[1], res[2], res[3],res[4])
    type(Key.ESC)
    waitVanish(NoxResources.TITLE_ITEM, 60)
    image = captureImage(NoxResources.BUTTON_BACK, -20, 1500, 860)
    drive.uploadFile("Profile.png", image.getFilename(), fId, "image/png")
    click(NoxResources.BUTTON_ITEM)
    exists(NoxResources.TITLE_ITEM, 60)
    image = captureImage(NoxResources.TITLE_ITEM, 0, 1380, 810)
    drive.uploadFile("Packs.png", image.getFilename(), fId, "image/png")
    if len(findAny(Pattern("1605239996094.png").similar(0.93))) > 0:
        for packLoop in range(10):
            CommonDMLib.dragDropAtSpeed(Pattern("1605239781030.png").targetOffset(3,715), Pattern("1605239781030.png").targetOffset(1,233), 1.5)
            image = captureImage(NoxResources.TITLE_ITEM, 0, 1380, 810)
            drive.uploadFile("Packs" + str(packLoop + 2) + ".png", image.getFilename(), fId, "image/png")
            if len(findAny(Pattern("1605239930745.png").similar(0.90))) > 0:
                break
    
    click(NoxResources.BUTTON_OTHER)
    exists(NoxResources.TITLE_ITEM, 60)
    image = captureImage(NoxResources.TITLE_ITEM, 0, 1380, 810)
    drive.uploadFile("Others.png", image.getFilename(), fId, "image/png")
except:
    e = sys.exc_info()
    for mes in e:
        print(mes)
    CommonDMLib.sendMessagetoSlack(EnvSettings.mentionUser, 'Error occured.', appname)
    CommonDMLib.sendMessagetoSlack(EnvSettings.mentionUser,traceback.format_exc(), appname)