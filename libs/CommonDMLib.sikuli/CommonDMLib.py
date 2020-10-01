# -*- coding: utf-8 -*-
from sikuli import *
import json
import os
import sys
import urllib2
import copy
import subprocess
from datetime import datetime
from pytz import timezone
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.JAVA_API_PATH)
from slackapis import SlackApis
from resizeimage import ResizeImage;
from spreadsheetapis import SpreadSheetApis

def killMultiPlayerManager():
    cmd = 'taskkill /im MultiPlayerManager.exe /t'
    returncode = subprocess.Popen(cmd, shell=True)

def isNewVersionAvailable():
    command1 = 'git fetch https://github.com/noifuji/dmp-auto.git'
    proc1 = subprocess.Popen(command1, shell  = True)
    proc1.communicate()
    
    command2 = 'git diff --quiet HEAD FETCH_HEAD'
    proc2 = subprocess.Popen(command2, shell  = True)
    proc2.communicate()
    
    if proc2.returncode == 0:
        return False
    elif proc2.returncode == 1:
        return True
    else:
        raise Exception("Invalid return code")

def dragDropAtSpeed(fromImg, toImg, speed):
    currentSpeed = Settings.MoveMouseDelay

    toImgObj = None
    if isinstance(toImg, str) or isinstance(toImg, Pattern):
        res = findAny(toImg)
        if len(res) == 0:
            raise Exception
        toImgObj = res[0]
    else:
        toImgObj = toImg
    toImg_gx = toImgObj.getX() + toImgObj.getW()/2 + toImgObj.getTargetOffset().getX()
    toImg_gy = toImgObj.getY() + toImgObj.getH()/2 + toImgObj.getTargetOffset().getY()

    fromImgObj = None
    if isinstance(fromImg, str) or isinstance(fromImg, Pattern):
        res = findAny(fromImg)
        if len(res) == 0:
            raise Exception
        fromImgObj = res[0]
    else:
        fromImgObj = fromImg
    fromImg_gx = fromImgObj.getX() + fromImgObj.getW()/2 + fromImgObj.getTargetOffset().getX()
    fromImg_gy = fromImgObj.getY() + fromImgObj.getH()/2 + fromImgObj.getTargetOffset().getY()
    
    mouseMove(fromImg)
    mouseDown(Button.LEFT)
    wait(0.4)
    Settings.MoveMouseDelay = speed
    mouseMove(toImg_gx - fromImg_gx, toImg_gy - fromImg_gy)
    mouseUp(Button.LEFT)
    Settings.MoveMouseDelay = currentSpeed

def callRemoveDataBat():
    cmd_file = EnvSettings.REMOVE_DATA_BAT_PATH
    command = cmd_file + " " + '"'+ EnvSettings.NoxAdbPath + '"'
    print command
    os.system(command)

def noxCallStartDMPApp():
    cmd_file = EnvSettings.NOX_START_APP_BAT_PATH
    command = cmd_file + " " + '"'+ EnvSettings.NoxAdbPath + '"'
    print command
    os.system(command)

def noxCallKillDMPApp():
    cmd_file = EnvSettings.NOX_KILL_APP_BAT_PATH
    command = cmd_file + " " + '"'+ EnvSettings.NoxAdbPath + '"'
    print command
    os.system(command)

#url:slackのwebhookのURL
#userid:slackのmemberID
#contents:送信するメッセージ
#appname:メッセージに表示する送信元の名前
def sendMessagetoSlack(userid, contents, appname):
    slack = SlackApis(EnvSettings.TOKEN, EnvSettings.TARGET_CHANNEL)
    slack.sendMessage(userid, appname, contents)

def uploadScreenShotToSlack(userid, message,  appname):
    filename = capture(App.focusedWindow())
    print "File Size:" + str(os.path.getsize(filename))
    if os.path.getsize(filename) > 500000:
        r = ResizeImage()
        filename = r.resize(filename, 0.5)
        print "Resized File Size:" + str(os.path.getsize(filename))
    for retry_loop in range(3):
        slack = SlackApis(EnvSettings.TOKEN, EnvSettings.TARGET_CHANNEL)
        try:
            slack.uploadImage(userid, appname, message, filename)
            break
        except:
            e = sys.exc_info()
            for mes in e:
                print(mes)
            wait(1)

def updateCardCount(ref, nameCount, cardCount):
    if len(nameCount) != len(cardCount) or len(nameCount) != 5:
        raise Exception
    
    row = [[nameCount[4],cardCount[4],nameCount[3],cardCount[3],nameCount[2],cardCount[2],nameCount[1],cardCount[1],nameCount[0],cardCount[0]]]
    
    f = open(os.path.join(EnvSettings.DATA_DIR_PATH , EnvSettings.CREDENTIALS_JSON_FILE))
    strCredentials = f.read()
    f.close()
    spreadsheet = SpreadSheetApis("DMPAuto", strCredentials)
    refs = spreadsheet.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, "Accounts!B3:B300", "ROWS")
    rowIndex = None
    for i in range(len(refs)):
        if refs[i][0] == str(ref):
            rowIndex = i + 3
            break
    spreadsheet.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, "Accounts!Q" + str(rowIndex) + ":Z" + str(rowIndex), row, "ROWS")

def downloadQuestStatus():
    print "downloadQuestStatus"
    
    f = open(os.path.join(EnvSettings.DATA_DIR_PATH , EnvSettings.CREDENTIALS_JSON_FILE))
    strCredentials = f.read()
    f.close()
    spreadsheet = SpreadSheetApis("DMPAuto", strCredentials)
    statusRaw = spreadsheet.batchRead(EnvSettings.ACCOUNT_INFO_SHEET_ID, ["Accounts!B3:C300", "Accounts!AB3:AD300"], "ROWS")

    accounts = statusRaw[0]
    statuses = statusRaw[1]
    
    status = []
    for i in range(min([len(accounts), len(statuses)])):
        if len(accounts[i]) > 1:
            status.append({"REF":accounts[i][0], "MAIN":statuses[i][0], "LEGEND":statuses[i][1], "SP":statuses[i][2]})

    return status

def completeQuestStatus(ref, questname):
    column = ""
    if questname == "MAIN":
        column = "AB"
    elif questname == "LEGEND":
        column = "AC"
    elif questname == "SP":
        column = "AD"
    else:
        raise Exception("Invalid Argument")
    
    f = open(os.path.join(EnvSettings.DATA_DIR_PATH , EnvSettings.CREDENTIALS_JSON_FILE))
    strCredentials = f.read()
    f.close()
    spreadsheet = SpreadSheetApis("DMPAuto", strCredentials)
    refs = spreadsheet.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, "Accounts!B3:B300", "ROWS")
    rowIndex = None
    for i in range(len(refs)):
        if refs[i][0] == str(ref):
            rowIndex = i + 3
            break
    if rowIndex == None:
        return
    spreadsheet.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, "Accounts!" + column + str(rowIndex), [["complete"]], "ROWS")


#return ref
def getSetupAccountRef():
    f = open(os.path.join(EnvSettings.DATA_DIR_PATH , EnvSettings.CREDENTIALS_JSON_FILE))
    strCredentials = f.read()
    f.close()
    spreadsheet = SpreadSheetApis("DMPAuto", strCredentials)
    refs = spreadsheet.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, "Accounts!B3:C300", "ROWS")
    result = ""
    for ref in refs:
        if len(ref) == 1:
            result = ref[0]
            break
    return result

STATISTICS_COMPUTERNAME = "COMPUTERNAME"
STATISTICS_REF = "REF"
STATISTICS_MISSION1 = "MISSION1"
STATISTICS_MISSION2 = "MISSION2"
STATISTICS_MISSION3 = "MISSION3"
STATISTICS_STARTTIME = "STARTTIME"
STATISTICS_ENDTIME = "ENDTIME"
STATISTICS_EXCEPTION = "EXCEPTION"
def uploadStatistics(sheetname, statistics):
    row = None
    if sheetname == "DailyMission":
        row = [[statistics[STATISTICS_COMPUTERNAME], statistics[STATISTICS_REF], statistics[STATISTICS_MISSION1], 
                statistics[STATISTICS_MISSION2], statistics[STATISTICS_MISSION3], statistics[STATISTICS_STARTTIME], 
                statistics[STATISTICS_ENDTIME], statistics[STATISTICS_EXCEPTION]]]
    elif sheetname == "MainStory":
        row = [[statistics["COMPUTERNAME"], statistics["EPISODE"], statistics["STAGE"], 
                statistics["STRATEGY"], statistics["RETRY"], statistics["STARTTIME"], 
                statistics["ENDTIME"], statistics["EXCEPTION"]]]
    else:
        raise Exception()
    
    print row
    
    f = open(os.path.join(EnvSettings.DATA_DIR_PATH , EnvSettings.CREDENTIALS_JSON_FILE))
    strCredentials = f.read()
    f.close()
    spreadsheet = SpreadSheetApis("DMPAuto", strCredentials)
    spreadsheet.append(EnvSettings.STATISTICS_SHEET_ID, sheetname + "!A1", row, "ROWS")

def updatePlayerId(ref, playerId, computername):
    f = open(os.path.join(EnvSettings.DATA_DIR_PATH , EnvSettings.CREDENTIALS_JSON_FILE))
    strCredentials = f.read()
    f.close()
    spreadsheet = SpreadSheetApis("DMPAuto", strCredentials)
    refs = spreadsheet.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, "Accounts!B3:B300", "ROWS")
    rowIndex = None
    for i in range(len(refs)):
        if refs[i][0] == str(ref):
            rowIndex = i + 3
            break
    spreadsheet.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, "Accounts!C" + str(rowIndex), [[playerId]], "ROWS")
    spreadsheet.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, "Accounts!AA" + str(rowIndex), [[computername]], "ROWS")

def updateAccountInfo(ref, lv, dmp, gold, packs, srPack):
    row = [[lv, dmp, gold]]
    row[0].extend(packs)
    row[0].append(srPack)
    
    f = open(os.path.join(EnvSettings.DATA_DIR_PATH , EnvSettings.CREDENTIALS_JSON_FILE))
    strCredentials = f.read()
    f.close()
    spreadsheet = SpreadSheetApis("DMPAuto", strCredentials)
    refs = spreadsheet.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, "Accounts!B3:B300", "ROWS")
    rowIndex = None
    for i in range(len(refs)):
        if refs[i][0] == str(ref):
            rowIndex = i + 3
            break
    spreadsheet.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, "Accounts!D" + str(rowIndex) + ":P" + str(rowIndex), row, "ROWS")

#Only for less 999,999
def isNumber(str):
    definedCharLess1000 = "0123456789"
    definedCharBigger1000 = "0123456789,"
    if len(str) <= 4:
        for s in str:
            if (s in definedCharLess1000) == False:
                return False
    else:
        for s in str:
            if (s in definedCharBigger1000) == False:
                return False
    return True

#FromRight 0
#FromLeft 1
def scanNumberChangeWidth(targetImage, offsetX, offsetY, width, height, RightLeft, charWidth):
    WIDTH_A_CHAR = charWidth
    MARGIN_LEFT = 20
    res = findAny(targetImage)
    num = ""
    if len(res) > 0:
        WIDTH_INIT = width
        WIDTH_CONFIRM = width
        dW = 2
        for num in range(1000):
            reg = None
            if RightLeft == 0:
                reg = Region(res[0].getX()+offsetX, res[0].getY()+offsetY, WIDTH_INIT - dW*num, height)
            elif RightLeft == 1:
                reg = Region(res[0].getX()+offsetX + dW*num, res[0].getY()+offsetY, WIDTH_INIT - dW*num, height)
            else:
                raise Exception("Illegal argumant RightLeft : " + str(RightLeft))
            reg.highlight(0.1)
            num = OCR.readWord(reg)
            if isNumber(num):
                print len(num)
                WIDTH_CONFIRM = len(num) * WIDTH_A_CHAR + MARGIN_LEFT
                break

        for num in range(1000):
            reg = None
            if RightLeft == 0:
                reg = Region(res[0].getX()+offsetX, res[0].getY()+offsetY, WIDTH_CONFIRM - dW*num, height)
            elif RightLeft == 1:
                reg = Region(res[0].getX()+offsetX + dW*num, res[0].getY()+offsetY, WIDTH_CONFIRM - dW*num, height)
            else:
                raise Exception("Illegal argumant RightLeft : " + str(RightLeft))
            reg.highlight(0.1)
            num = OCR.readWord(reg)
            if isNumber(num):
                    break
    return num

def scanAccountInfo(resource):
    ts = [resource.TITLE_PACK1,resource.TITLE_PACK2,
            resource.TITLE_PACK3,resource.TITLE_PACK4,
            resource.TITLE_PACK5,resource.TITLE_PACK5SR]

    dmp = 0
    gold = 0
    tempPacks = []
    lv = ""

    OFFSET_X = 78
    OFFSET_Y = 96
    WIDTH_INIT = 60
    HEIGHT = 27
    WIDTH_INIT_LONG = 110
    
    OFFSET_X_LV = 265
    OFFSET_Y_LV = 34
    WIDTH_INIT_LV = 85
    HEIGHT_LV = 46

    for waitProfileLoop in range(100):
        if len(findAny(resource.ICON_OTHER)) > 0:
            click(resource.ICON_OTHER)
            wait(2)
        if len(findAny(resource.BUTTON_PROFILE)) > 0:
            click(resource.BUTTON_PROFILE)
            wait(2)
        if len(findAny(resource.TITLE_PROFILE)) > 0:
            break
    
    lv = scanNumberChangeWidth(resource.TITLE_PLAYER_LV, OFFSET_X_LV, OFFSET_Y_LV, WIDTH_INIT_LV, HEIGHT_LV, 1, 35)

    
    click(resource.BUTTON_ITEM)
    wait(1)

    scanCount = 0
    for i in range(len(ts)):
        res = scanNumberChangeWidth(ts[i], OFFSET_X, OFFSET_Y, WIDTH_INIT, HEIGHT, 0, 20)
        if res == "":
            tempPacks.append("")
        else:
            tempPacks.append(res)
            scanCount += 1
            if scanCount % 2 == 0:
                Settings.MoveMouseDelay = 1
                dragDrop(resource.TITLE_ITEM_DRAG, resource.TITLE_ITEM_DROP)
                Settings.MoveMouseDelay = 0.1
                wait(1)
    
    click(resource.BUTTON_OTHER)
    wait(1)


    gold = scanNumberChangeWidth(resource.TITLE_GOLD, OFFSET_X, OFFSET_Y, WIDTH_INIT_LONG, HEIGHT, 0, 20)
    dmp = scanNumberChangeWidth(resource.TITLE_DMPOINT, OFFSET_X, OFFSET_Y, WIDTH_INIT_LONG, HEIGHT, 0, 20)

    packs = [0,0,0,0,0,0,0,0,0]
    for i in range(len(tempPacks)-1):
        packs[i] = tempPacks[i]

    srPack = tempPacks[len(tempPacks)-1]
    return [lv, dmp, gold, packs, srPack]

def downloadFile(url, dest):
    print "downloadFile"
    filedata = urllib2.urlopen(url)
    datatowrite = filedata.read()
    f = open(dest, 'wb')
    f.write(datatowrite)
    f.close()

def getJsonFromDisk(path):
    f = open(path, 'r')
    json_data = json.load(f)
    f.close()
    return json_data

def downloadDeckCodes():
    print "downloadDeckCodes"
    saveFilePath = os.path.join(EnvSettings.DATA_DIR_PATH, EnvSettings.DECK_CODE_JSON_FILE)
    downloadFile(EnvSettings.DRIVE_DECK_CODE_JSON_URL, saveFilePath)

def getDeckCode(DeckName):
    deckCodesJsonPath = os.path.join(EnvSettings.DATA_DIR_PATH, EnvSettings.DECK_CODE_JSON_FILE)
    if os.path.exists(deckCodesJsonPath) == False:
        downloadDeckCodes()

    json_data = getJsonFromDisk(deckCodesJsonPath)
    if DeckName in json_data["deck_codes"].keys():
        return json_data["deck_codes"][DeckName]
    else:
        print "no deck name was matched."
        return ""
            
def removeCompletedInstances(instances):
    COMPLETED_INSTANCES_JSON_PATH = EnvSettings.DATA_DIR_PATH + "/" + EnvSettings.COMPLETED_INSTANCES_JSON_FILE
    
    #lastUpdateでjsonを参照すべきかどうかを判定する。
    #ファイル・フォルダが存在しないなら参照しない
    if os.path.exists(COMPLETED_INSTANCES_JSON_PATH) == False:
        return instances
    
    json_data = getJsonFromDisk(COMPLETED_INSTANCES_JSON_PATH)
    dt_now = datetime.now(timezone('Asia/Dubai'))
    dt_json = datetime.strptime(json_data["lastUpdate"], '%Y/%m/%d')
    #業務時刻が当日でなければそのままかえす
    if dt_now.year != dt_json.year or dt_now.day != dt_json.day or dt_now.month != dt_json.month:
        return instances
    
    #データ読み込みし、完了済みのインスタンスをターゲットから除外する。
    completedInstances = json_data["completedInstances"]

    targetInstances = []
    
    for i in instances:
        appendFlag = True
        for ci in completedInstances:
            if i == ci:
                appendFlag = False
        if appendFlag == True:
            targetInstances.append(i)

    return targetInstances

def updateCompletedInstanceJson(instanceId):
    COMPLETED_INSTANCES_JSON_PATH = os.path.join(EnvSettings.DATA_DIR_PATH , EnvSettings.COMPLETED_INSTANCES_JSON_FILE)

    dt_now = datetime.now(timezone('Asia/Dubai'))
    
    #フォルダが存在しなければ作成する。
    if os.path.exists(EnvSettings.DATA_DIR_PATH) == False:
        print "No Nox Data Dir"
        os.mkdir(EnvSettings.DATA_DIR_PATH)
    #ファイルがなければ空のを作る。
    if os.path.exists(COMPLETED_INSTANCES_JSON_PATH) == False:
        json_data = {}
        json_data["lastUpdate"] = dt_now.strftime('%Y/%m/%d')
        json_data["completedInstances"] = []
        f = open(COMPLETED_INSTANCES_JSON_PATH, mode='w')
        json.dump(json_data,f,indent=4)
        f.close()

    json_file_r = open(COMPLETED_INSTANCES_JSON_PATH, 'r')
    json_data_r = json.load(json_file_r)
    dt_json = datetime.strptime(json_data_r["lastUpdate"], '%Y/%m/%d')
    completedInstances = json_data_r["completedInstances"]
    #lastUpdateが当日なら、追記する。
    #lastUpdateが当日でなければ、新規に追加する。
    if dt_now.year == dt_json.year and dt_now.day == dt_json.day and dt_now.month == dt_json.month:
        appendFlag = True
        for ci in completedInstances:
            if ci == instanceId:
                appendFlag = False

        if appendFlag == True:
            completedInstances.append(instanceId)
    else:
        completedInstances = [instanceId]

    json_data_w = {}
    json_data_w["lastUpdate"] = dt_now.strftime('%Y/%m/%d')
    json_data_w["completedInstances"] = completedInstances
    json_file_w = open(COMPLETED_INSTANCES_JSON_PATH, mode='w')
    json.dump(json_data_w, json_file_w,indent=4)
    json_file_w.close()

def sum(list) :
    result = 0
    for l in list:
        result += l
    return result

def compareList(list1, list2) :
    if len(list1) != len(list2):
        return False
    
    for num in range(len(list1)):
        if list1[num] != list2[num]:
            return False
    return True

def countAllCardsByRarity(resource, app):
    names = []
    cards = []
    rarities = resource.BUTTON_RARITY
    for rarity in rarities:
        click(resource.BUTTON_FILTER)
        click(resource.BUTTON_RESET)
        click(rarity)
        wheel(rarity,Button.WHEEL_DOWN, 20)
        wait(0.3)
        click(resource.BUTTON_DMPP01)
        click(resource.BUTTON_DMPP02)
        click(resource.BUTTON_DMPP03)
        click(resource.BUTTON_DMPP04)
        click(resource.BUTTON_DMPP05)
        click(resource.BUTTON_OK)
        wait(0.5)
        
        targets = resource.ICON_CARD_COUNT
        
        count = [0,0,0,0]
        prevCount = [0,0,0,0]
        confirmedCount = [0,0,0,0]
        wheelCount = 0
    
        if exists(resource.SCROLL1, 0.5) == None:
            num = 0
            for target in targets :
                region_of_DMApp = app.window()
                f = Finder(SCREEN.capture())
                f.findAll(target)
                result = []
                while f.hasNext():
                   result.append(f.next())
                confirmedCount[num] += len(result)
                num += 1
            names.append(sum(confirmedCount))
            cards.append(confirmedCount[0]*1 + confirmedCount[1]*2 + confirmedCount[2]*3 + confirmedCount[3]*4)
            continue
        
        for loop in range(1000):
            num = 0
            for target in targets :
                region_of_DMApp = app.window()
                region_of_DMApp.setH(region_of_DMApp.getH()*1/2)
                f = Finder(SCREEN.capture(region_of_DMApp))
                f.findAll(target)
                result = []
                while f.hasNext():
                   result.append(f.next())
                count[num] = len(result)
                num += 1
    
            confirmedCount[0] += count[0]
            confirmedCount[1] += count[1]
            confirmedCount[2] += count[2]
            confirmedCount[3] += count[3]
            
            prevCount[0] = count[0]
            prevCount[1] = count[1]
            prevCount[2] = count[2]
            prevCount[3] = count[3]
                
            if exists(resource.SCROLL2,0.5) != None:
                num = 0
                for target in targets :
                    region_of_DMApp = app.window()
                    region_of_DMApp.setY(region_of_DMApp.getY()+region_of_DMApp.getH()*1/2)
                    region_of_DMApp.setH(region_of_DMApp.getH()*1/2)
                    f = Finder(SCREEN.capture(region_of_DMApp))
                    f.findAll(target)
                    result = []
                    while f.hasNext():
                       result.append(f.next())
                    confirmedCount[num] += len(result)
                    num += 1
                break
            
            wheel(resource.TITLE_CARD_LIST, Button.WHEEL_DOWN, 4)
            wait(0.5)
        names.append(sum(confirmedCount))
        cards.append(confirmedCount[0]*1 + confirmedCount[1]*2 + confirmedCount[2]*3 + confirmedCount[3]*4)
    
    print "VR:" + str(names[0]) + "Card Names / " + str(cards[0]) + "Cards"
    print "SR:" + str(names[1]) + "Card Names / " + str(cards[1]) + "Cards"
    return {"VR" : cards[0], "SR" : cards[1]}

def chooseDeck(resource, deckImage):
    print "chooseDeck"
    print deckImage
    if len(findAny(deckImage)) > 0:
        print "deckImage was found"
        click(deckImage)
        return True
    else:
        wheel(resource.TITLE_DECKLIST, Button.WHEEL_DOWN, 10)
        if exists(deckImage, 3) != None:
            print "deckImage was found"
            click(deckImage)
            return True
        else:
            print "No deckImage"
            return False

def addNewDeckByCode(resource, code):
    wheel(resource.TITLE_DECKLIST, Button.WHEEL_UP, 10)
    wait(1)
    click(resource.BUTTON_CREATE_NEW_DECK)
    wait(0.5)
    click(resource.BUTTON_CREATE_BY_CODE)
    wait(0.5)
    click(resource.INPUT_DECK_CODE1)
    wait(2)
    type(code)
    wait(0.5)
    click(resource.INPUT_DECK_CODE2)
    wait(0.5)
    click(resource.BUTTON_OK)
    wait(0.5)
    exists(resource.BUTTON_SAVE_DECK,120)
    for skipTutorialLoop in range(6):
        if len(findAny(resource.BUTTON_BACK2)) > 0:
            click(resource.BUTTON_BACK2)
        wait(1)
    exists(resource.BUTTON_SAVE_DECK, 60)
    click(resource.BUTTON_SAVE_DECK)
    exists(resource.BUTTON_OK, 60)
    click(resource.BUTTON_OK)
    exists(resource.TITLE_DECKLIST, 30)

def skipStory(resource):
    print 'skipStory'
    if len(findAny(resource.BUTTON_SKIP)) > 0:
        try:
            click(resource.BUTTON_SKIP)
            wait(2)
            click(resource.BUTTON_OK)
        except:
            print "failed to click"

def skipRewards(resource):
    print 'skipRewards'
    dailyReward = 0
    results = {"levelup" : 0, "daily" : 0, "secret":0, "clear":0, "point" : 0}
    print "checking rewards...."
    if len(findAny(resource.TITLE_REWARD_LEVEL_UP)) > 0:
        print 'Level up reward'
        try:
            click(resource.BUTTON_OK)
        except:
            print "failed to click"
        results["levelup"] += 1
    #デイリー報酬スキップ
    if len(findAny(resource.TITLE_REWARD_DAILY)) > 0:
        print 'Daily reward'
        results["daily"] += 1
        try:
            click(resource.BUTTON_OK)
        except:
            print "failed to click"
    #シークレットミッション報酬
    if len(findAny(resource.TITLE_REWARD_SECRET)) > 0:
        print 'Secret Mission reward'
        try:
            click(resource.BUTTON_OK)
        except:
            print "failed to click"
        results["secret"] += 1
    #初回クリア
    if len(findAny(resource.TITLE_REWARD_CLEAR)) > 0:
        print 'The first clear reward'
        try:
            click(resource.BUTTON_OK)
        except:
            print "failed to click"
        results["clear"] += 1
    #ポイント報酬
    if len(findAny(resource.TITLE_REWARD_POINT)) > 0:
        print 'Point reward'
        try:
            click(resource.BUTTON_OK)
        except:
            print "failed to click"
        results["point"] += 1
    wait(1)
    return results


#return 0:正常終了
#return -1:リザルト画面へ遷移
def skipNotifications(resource):
    print 'skipNotifications'
    print "checking notifications...."
    #中断されたデュエル
    if len(findAny(resource.MESSAGE_RESTART_DUEL)) > 0:
        print 'A stopped duel is detected. It will be canceled.'
        click(resource.BUTTON_CANCEL)
    #前回のリザルト表示
    if len(findAny(resource.MESSAGE_LAST_SP_BATTLE)) > 0 :
        print 'The last duel result detected.'
        click(resource.BUTTON_OK)
        return -1
    #前回のリザルト表示
    if len(findAny(resource.MESSAGE_LAST_BATTLE)) > 0 :
        print 'The last duel result detected.'
        click(resource.BUTTON_OK)
    
    if len(findAny(resource.AD)) > 0:
        print 'Ads was skipped.'
        if len(findAny(resource.BUTTON_OK)) > 0:
            click(resource.BUTTON_OK)
    wait(1)
    return 0

def openMission(resource):
    print "openMission"
    for openLoop in range(100):
        print "opening mission..." + str(openLoop)
        if len(findAny(resource.ICON_MISSION)) > 0:
            click(resource.ICON_MISSION)
            wait(1)
        if len(findAny(resource.TITLE_MISSION)) > 0:
            break

def closeMission(resource):
    print "closeMission"
    if len(findAny(resource.BUTTON_CLOSE)) > 0:
        click(resource.BUTTON_CLOSE)
        waitVanish(resource.TITLE_MISSION, 30)

def getTargetMissions(resource):
    print "getTargetMissions"
    offsetX1 = 180
    offsetY1 = 190
    offsetY2 = 360
    offsetY3 = 530
    width = 1065
    height = 65
    
    missionTitle = findAny(resource.TITLE_MISSION)
    if len(missionTitle) <= 0:
        return
    
    missionRegs = [
            Region(missionTitle[0].getX() + offsetX1, missionTitle[0].getY() + offsetY1, width, height),
            Region(missionTitle[0].getX() + offsetX1, missionTitle[0].getY() + offsetY2, width, height),
            Region(missionTitle[0].getX() + offsetX1, missionTitle[0].getY() + offsetY3, width, height)
            ]

    targetMissions = []
    for reg in missionRegs:
        reg.highlight(0.5)
        best = reg.findBestList([d.get("IMAGE") for d in resource.MISSIONS])
        if best != None:
            print resource.MISSIONS[best.getIndex()]["NAME"] + " : " + str(best.getScore())
            if best.getScore() > 0.9:
                targetMissions.append(resource.MISSIONS[best.getIndex()])
                
    results = []
    #sort by mission group
    for g in resource.GROUPS:
        for t in targetMissions:
            if t["GROUP"] == g:
                results.append(t)

    return results

def getMissionStrategy(resource, mission):
    print "getMissionStrategy"
    strategyCode = 0
    
    if mission["GROUP"] == "SPELL":
        strategyCode = 1
    elif mission["GROUP"] == "SPEED":
        strategyCode = 2
    elif mission["GROUP"] == "BATTLE":
        strategyCode = 3
    elif mission["GROUP"] == "ST":
        strategyCode = 4
    elif mission["GROUP"] == "LARGE":
        strategyCode = 5
    elif mission["GROUP"] == "RETIRE":
        strategyCode = 6
        
    return strategyCode

#return 0 正常にバトル開始
#return -1 異常発生
def waitStartingGame(resource):
    print 'waitStartingGame'
    for num in range(200):
        #ストーリースキップ
        skipStory(resource)
        #マッチングしなかった場合
        if len(findAny(resource.MESSAGE_NO_OPPONENTS)) > 0:
            click(resource.BUTTON_OK)
            wait(resource.BUTTON_SMALL_BATTLE_START, 60)
            click(resource.BUTTON_SMALL_BATTLE_START)
            wait(resource.BUTTON_LARGE_BATTLE_START,60)
            click(resource.BUTTON_LARGE_BATTLE_START)
            return -1
        if len(findAny(resource.BUTTON_RETRY)) > 0:
            click(resource.BUTTON_RETRY)
        if len(findAny(resource.MESSAGE_ERROR_9003)) > 0:
            raise Exception
            
        if len(findAny(resource.MESSAGE_CONNECTION_LOST)) >0 :
            click(resource.BUTTON_OK)
            exists(resource.ICON_EXTRA,120)
            openAndStartSPBattle(resource, getDeckCode("DECKCODE_SPBATTLE"))
            return -1
        if len(findAny(resource.BUTTON_TURN_END)) > 0:
            break
        wait(1)
    return 0

#Nox
#OFFSET_X = -240
#OFFSET_Y = 284
#WIDTH = 118
#HEIGHT = 70
def getMainStoryStage(resource, offsetX, offsetY, width, height):
    stage = 0
    res = findAny(resource.TITLE_MAIN_STORY)
    if len(res) > 0:
        reg = Region(res[0].getX() + offsetX, res[0].getY()+offsetY, width, height)
        reg.highlight(3)
        scores = []
        for image in [d.get("IMAGE") for d in resource.STAGES]:
           detected = reg.findAny(image)
           if len(detected) > 0:
               scores.append(detected[0].getScore())
               print detected[0].getScore()
           else:
               scores.append(0)
               print 0
               
        max_value = max(scores)
        max_index = scores.index(max_value)
               
        stage = resource.STAGES[max_index]["STAGE"]

    return stage

def getMainStoryEpisode(resource):
    episode = 0
    res = findAny(resource.TITLE_MAIN_STORY)
    if len(res) > 0:
        result = findBestList([d.get("IMAGE") for d in resource.EPISODES])
        if result != None:
            episode = resource.EPISODES[result.getIndex()]["EPISODE"]
        else:
            episode = 0
    return episode

def openMainStory(resource):
    print 'openAndStartMainStory'
    breakCount = 0
    for openStoryLoop in range(100):
        if exists(resource.ICON_SOLO_PLAY, 1) != None:
            click(resource.ICON_SOLO_PLAY)
            wait(3)
        if exists(resource.BUTTON_MAIN_STORY, 1) != None:
            click(resource.BUTTON_MAIN_STORY)
        if exists(resource.BUTTON_BACK, 1) != None:
            click(resource.BUTTON_BACK2)
        if len(findAny(resource.TITLE_MAIN_STORY2)) > 0:
            breakCount += 1
        if breakCount > 5:
            break
        wait(0.5)

def chooseMainStoryStage(resource, ep, stageImage):
    if ep == 1:
        if exists(resource.TITLE_EP1,1) == None and exists(resource.TITLE_EP1_LOW_RESOLUTION,1) == None:
            click(resource.BUTTON_BACK)
            for chooseEPLoop in range(100):
                if len(findAny(resource.BUTTON_EP1)) > 0:
                    click(resource.BUTTON_EP1)
                    wait(2)
                    break
                wheel(resource.TITLE_MAIN_STORY2, Button.WHEEL_DOWN, 10)
                wait(1)
            exists(resource.TITLE_MAIN_STORY,30)
        for wheelLoop in range(10):
            wheel(resource.TITLE_MAIN_STORY2, Button.WHEEL_DOWN, 40)
            wait(1)
            if len(findAny(stageImage)) > 0 :
                click(stageImage)
                break
    else:
        raise Exception("Not implemented yet...")

def startMainStoryBattle(resource, deckImage, deckcode):
    if len(findAny(resource.BUTTON_SMALL_BATTLE_START)) > 0:
        click(resource.BUTTON_SMALL_BATTLE_START)
    if exists(resource.BUTTON_LARGE_BATTLE_START,120) != None:
        if chooseDeck(resource, deckImage) == False:
            addNewDeckByCode(resource, deckcode)
        click(resource.BUTTON_LARGE_BATTLE_START)

def getStrategyByMainStoryStage(episode, stage):
    strategy = 100
    if episode == 4 and stage == 3:
        strategy = 2
    elif episode == 4 and stage == 9:
        strategy = 2
    elif episode == 3 and stage == 2:
        strategy = 100
    elif episode == 2 and stage == 6:
        strategy = 2
    elif episode == 2 and stage == 13:
        strategy = 2
    elif episode == 1 and stage >= 1 and stage <= 15:
        strategy = 2
    else:
        strategy = 100
        
    return strategy

def getDeckByStrategy(resource, strategy):
    if strategy == 1:
        return [resource.DECKIMAGE_STSPELL, getDeckCode("DECKCODE_STSPELL")]
    elif strategy == 2 or strategy == 6:
         return [resource.DECKIMAGE_RED_BLACK, getDeckCode("DECKCODE_RED_BLACK")]
    elif strategy == 3 or strategy == 4:
        return [resource.DECKIMAGE_ST, getDeckCode("DECKCODE_ST")]
    elif strategy == 5:
        return [resource.DECKIMAGE_LARGE_CREATURE, getDeckCode("DECKCODE_LARGE_CREATURE")]
    elif strategy == 100:
        return [resource.DECKIMAGE_MAIN, getDeckCode("DECKCODE_MAIN")]
    elif strategy == 101:
        return [resource.DECKIMAGE_SPBATTLE, getDeckCode("DECKCODE_SPBATTLE")]
    else:
        return None

def getPresent(resource):
    if len(findAny(resource.ICON_PRESENT_WITH_SIGN)) > 0:
        click(resource.ICON_PRESENT_WITH_SIGN) 
        exists(resource.TITLE_PRESENT, 30)
        click(resource.BUTTON_RECIEVE)
        exists(resource.BUTTON_OK, 60)
        click(resource.BUTTON_OK)
        wait(3)
        click(resource.BUTTON_CLOSE)

#True : On
#False : Off
def isNoxOn():
    command1 = 'tasklist'
    command2 = 'findstr Nox.exe'
    proc1 = subprocess.Popen(
        command1,
        shell  = True,
        stdin  = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)
    
    proc2 = subprocess.Popen(
        command2,
        shell  = True,
        stdin  = proc1.stdout,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)
    
    stdout_data, stderr_data = proc2.communicate()
    return stdout_data != ""

def exitNox(resources):
    if isNoxOn() == False:
        print "closing Multiplayer"
        App(EnvSettings.NoxMultiPlayerPath).close()
        return
    
    App(EnvSettings.NoxMultiPlayerPath).open()
    if exists(resources.TITLE_MULTI_PLAYER,120) == None:
        killMultiPlayerManager()
        raise Exception("MultiPlayerManager has error. Please retry to launch.")
    for num in range(10):
        if exists(resources.BUTTON_NOX_STOP, 1) == None:
            wheel(resources.TITLE_MULTI_PLAYER, Button.WHEEL_DOWN, 1)
        else:
            break
    for num in range(10):
        if exists(resources.BUTTON_NOX_STOP, 1) == None:
            wheel(resources.TITLE_MULTI_PLAYER, Button.WHEEL_UP, 2)
        else:
            break
    if len(findAny(resources.BUTTON_NOX_STOP)) > 0:
        click(resources.BUTTON_NOX_STOP)
        if exists(resources.BUTTON_NOX_OK_BLUE, 10) != None:
            click(resources.BUTTON_NOX_OK_BLUE)
        if waitVanish(resources.BUTTON_NOX_STOP, 120) == False:
            print "Nox instance stays."
            exit(1)
    App(EnvSettings.NoxMultiPlayerPath).close()

def openNoxInstance(resources, ref):
    App(EnvSettings.NoxMultiPlayerPath).open()
    if exists(resources.TITLE_MULTI_PLAYER,120) == None:
        killMultiPlayerManager()
        raise Exception("MultiPlayerManager has error. Please retry to launch.")
    exists(resources.BUTTON_NOX_PLAY, 120)
    click(resources.ICON_SEARCH)
    wait(2)
    type(str(ref))
    wait(1)
    type(Key.ENTER)
    wait(5)
    if len(findAny(resources.BUTTON_NOX_PLAY)) > 0:
        click(resources.BUTTON_NOX_PLAY)
    else:
        raise Exception("No instance : " + str(ref))
    App(EnvSettings.NoxMultiPlayerPath).close()
    
def RestartNox(resources, ref):
    print "restarting Nox player..."
    exitNox(resources)
    wait(3)
    openNoxInstance(resources, ref)

    for noxLaunchLoop in range(600):
        print "noxLaunchLoop..." + str(noxLaunchLoop)
        if len(findAny(resources.MESSAGE_FAILED_TO_START_LAUNCHER)) > 0:
            try:
                click(resources.MESSAGE_FAILED_TO_START_LAUNCHER)
            except:
                print "failed to click"
        if len(findAny(resources.ICON_BROWSER)) > 0:
            break
        wait(1)
    wait(30)
    if len(findAny(resources.MESSAGE_BACKUP)) > 0:
        click(resources.MESSAGE_BACKUP)
        click(0.2)
        click(resources.MESSAGE_BACKUP_NODISP)
        wait(1)
        click(resources.BUTTON_NOX_OK)


def RestartApp(resource):
    print 'RestartApp'
    if resource.APP_ENGINE == "NOX":
        noxCallKillDMPApp()
        wait(3)
        noxCallStartDMPApp()
    elif resource.APP_ENGINE == "ANDAPP":
        App(EnvSettings.AppPath).close()
        App(EnvSettings.AndAppPath).close()
        wait(3)
        App(EnvSettings.AndAppPath).open()
        exists("1600609176253.png",120)
        App(EnvSettings.AppPath).open()
    else:
        raise Exception

    skipUpdateFlag = True
    for num in range(180):
        print "loading opening page......" + str(num)
        if resource.APP_ENGINE == "NOX":
            if len(findAny("1597912712276.png")) > 0:
                print "An update is found."
                skipUpdateFlag = False
                break
            
            if len(findAny(resource.MESSAGE_FAILED_TO_START_LAUNCHER)) > 0:
                print "Android Error is detected."
                try:
                    click(resource.MESSAGE_FAILED_TO_START_LAUNCHER)
                except:
                    print "failed to click"
                break
        
        if len(findAny(resource.BUTTON_TAKEOVER)) > 0:
            print "The opening page is found."
            break
        
        if num >= 179:
            print 'Too many retries.'
            raise Exception
        wait(1)

    if skipUpdateFlag == False:
        click(resource.BUTTON_OK)
        wait(5)
        click("1597912784096.png")
        exists("1597912950842.png",1800)
        click("1597912950842.png")
        if exists(resource.BUTTON_AGREE, 30) != None:
            click(resource.BUTTON_AGREE)
    
    exists(resource.BUTTON_TAKEOVER,180)
    click(resource.BUTTON_TAKEOVER)
    skipDownloadFlag = False
    for num in range(180):
        print "loading game...." + str(num)
        if len(findAny(resource.MESSAGE_DOWNLOAD)) > 0:
            print "A daownload is found."
            break
        if resource.APP_ENGINE == "NOX":
            if len(findAny(resource.BUTTON_ALLOW)) > 0:
                print "The google login is found."
                click(resource.BUTTON_ALLOW)
            if len(findAny(resource.MESSAGE_CONFIRM_ALLOW)) > 0:
                print "The google login confirm is found."
                wheel(resource.MESSAGE_CONFIRM_ALLOW, Button.WHEEL_DOWN, 20)
                wait(2)
                click(resource.BUTTON_ALLOW_BLUE)
        if len(findAny(resource.BUTTON_SKIP)) > 0 or len(findAny(resource.ICON_HOME)) > 0:
            print "Loading is finished."
            skipDownloadFlag = True
            break
        if num >= 179:
           raise Exception 
    if skipDownloadFlag == False:
        click(resource.BUTTON_OK)
        for downloadLoop in range(300):
            print "downloading..." + str(downloadLoop)
            if len(findAny(resource.BUTTON_SKIP)) > 0 or len(findAny(resource.ICON_HOME)) > 0 or len(findAny(resource.BUTTON_TAP_AND_NEXT)) > 0:
                break
            if downloadLoop >= 299:
                raise Exception
            wait(1)
    #結果発表をスキップ
    for resultLoop in range(60):
        print "checking monthly competition result...." + str(resultLoop)
        if len(findAny(resource.BUTTON_TAP_AND_NEXT)) > 0:
            for resultLoop in range(10):
                click(Pattern("1598926999345.png").targetOffset(124,106))
                wait(6)
        wait(1)
        if len(findAny(resource.BUTTON_SKIP)) > 0 or len(findAny(resource.ICON_HOME)) > 0:
            break
    #ログインボーナスやらキャンペーンをスキップ
    for num in range(60):
        print "checking login bonus.." + str(num)
        if len(findAny(resource.BUTTON_SKIP)) > 0: 
            click(resource.BUTTON_SKIP)
        if exists(resource.ICON_HOME,2) != None:
            break
        wait(1)
    for skipLoop in range(120):
        if skipNotifications(resource) == -1:
            eixsts(resource.BUTTON_SMALL_OK, 60)
            for backLoop in range(60):
                if len(findAny(resource.BUTTON_SMALL_OK)) > 0:
                    click(resource.BUTTON_SMALL_OK)
                if len(findAny(resource.BUTTON_BACK)) > 0:
                    click(resource.BUTTON_BACK)
                if len(findAny(resource.ICON_HOME)) > 0:
                    break
        skipRewards(resource)
        if len(findAny(resource.ICON_MISSION)) > 0:
            click(resource.ICON_MISSION)
            if len(findAny(resource.TITLE_MISSION)) > 0:
                click(resource.BUTTON_CLOSE)
                break