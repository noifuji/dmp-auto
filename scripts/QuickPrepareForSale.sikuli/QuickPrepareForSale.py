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
    wheel(Pattern("1599973746387.png").targetOffset(227,-209), Button.WHEEL_DOWN, 4)
    wait(5)
    click(NoxResources.BUTTON_BASIC)
    wheel(Pattern("1599973746387.png").targetOffset(227,-209), Button.WHEEL_DOWN, 15)
    wait(5)
    for dmpp in dmpps:
        click(dmpp)
    click("1596590612922.png")
    waitVanish("1596590612922.png", 60)

appname = 'QUICKPREPARE'
Settings.MoveMouseDelay = 0.1
drive = DriveApis("DMPAuto", CommonDMLib.getCredentials())
sheets = SpreadSheetApis("DMPAuto", CommonDMLib.getCredentials())
try:
    ref = input("[Quick]Enter Ref")

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
    CommonDMLib.getPresent(NoxResources)
    
    fId = drive.createFolder(str(ref), "1ApCg9taRAEmK7QH93bxmoIzMbRaC_r7m")


    for openCardListLoop in range(100):
        if len(findAny(NoxResources.ICON_CARD)) > 0:
            try:
                click(NoxResources.ICON_CARD)
            except:
                print "failed to click"
            wait(1)
        if len(findAny(Pattern("1596593310453.png").targetOffset(-2,-214))) > 0:
            try:
                click(Pattern("1596593310453.png").targetOffset(-2,-214))
            except:
                print "failed to click"
            wait(1)
        if exists("1596593154431.png", 120) != None:
            for listTutorialLoop in range(10):
                click(Pattern("1596593154431.png").targetOffset(-2,47))
                wait(0.2)
            break
    
    TARGET_RARITY = [{"NAME":"VR", "IMAGE":NoxResources.BUTTON_RARITY_VERYRARE}, 
            {"NAME":"SR", "IMAGE":NoxResources.BUTTON_RARITY_SUPERRARE}]
    TARGET_DMPP = NoxResources.BUTTON_DMPPS
    for rarity in TARGET_RARITY:
        filterCardList([rarity], TARGET_DMPP)
        if exists(NoxResources.SCROLL1,1) == None:
            image = captureImage(NoxResources.TITLE_CARD_LIST, 47, 1340, 620)
            drive.uploadFile(rarity["NAME"] + ".png", image.getFilename(), fId, "image/png")
        else:
            i = 0
            while i < len(TARGET_DMPP):
                target = []
                target.append(TARGET_DMPP[i])
                if i + 1 < len(TARGET_DMPP):
                    target.append(TARGET_DMPP[i+1])

                if i + 2 < len(TARGET_DMPP):
                    target.append(TARGET_DMPP[i+2])
                
                filterCardList([rarity], target)
                image = captureImage(NoxResources.TITLE_CARD_LIST, 47, 1340, 620)
                drive.uploadFile(rarity["NAME"] + str(i+1) +  ".png", image.getFilename(), fId, "image/png")

                i = i + 3

    #PRIZE
    #TARGET_RARITY = [[{"NAME":"VR", "IMAGE":NoxResources.BUTTON_RARITY_VERYRARE}], 
    #        [{"NAME":"R", "IMAGE":NoxResources.BUTTON_RARITY_RARE}],
    #        [{"NAME":"C", "IMAGE":NoxResources.BUTTON_RARITY_COMMON},
    #         {"NAME":"UC", "IMAGE":NoxResources.BUTTON_RARITY_UNCOMMON}]]
    # for i in range(len(TARGET_RARITY)):
    #    filterCardList(TARGET_RARITY[i], [NoxResources.BUTTON_PRIZE])
    #    image = captureImage(NoxResources.TITLE_CARD_LIST, 47, 1340, 620)
    #    drive.uploadFile("PRIZE" + str(i) + ".png", image.getFilename(), fId, "image/png")

    type(Key.ESC)
    exists(NoxResources.ICON_SOLO_PLAY, 60)
    
    for waitProfileLoop in range(100):
        if len(findAny(NoxResources.ICON_OTHER)) > 0:
            click(NoxResources.ICON_OTHER)
            wait(2)
        if len(findAny(NoxResources.BUTTON_PROFILE)) > 0:
            click(NoxResources.BUTTON_PROFILE)
            wait(2)
        if len(findAny(NoxResources.TITLE_PROFILE)) > 0:
            wait(2)
            break
    
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
            if len(findAny(Pattern("1605239930745.png").similar(0.94))) > 0:
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