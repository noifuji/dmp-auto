# -*- coding: utf-8 -*-
from sikuli import *
import json
import os
import sys
import urllib2
import copy
import subprocess
import shutil
from datetime import datetime
from pytz import timezone
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.JAVA_API_PATH)
from slackapis import SlackApis
from resizeimage import ResizeImage;

def createGameTradeDraft(ref):
    url = "https://w4vo2tvmdf.execute-api.ap-northeast-1.amazonaws.com/dev"
    data = json.dumps({"ref" : str(ref)})
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    print response

def checkPrepareGameTradeDraft():
    url = "https://cckbzlmsd6.execute-api.ap-northeast-1.amazonaws.com/dev"
    f = urllib2.urlopen(url)
    response = f.read()
    f.close()
    print response
    dic = json.loads(response)

    if "body" in dic:
        return dic["body"]
    else:
        return None

def isRefAvailable(sheets, argRef):
    if argRef == None:
        return False
    
    ref = str(argRef)
    #check status
    STATUS_RANGE = EnvSettings.STATUS_INFO_SHEET_NAME + "!" + EnvSettings.STATUS_INFO_REF_COL + "2:" + EnvSettings.STATUS_INFO_STATUS_COL + "3000"
    rawData = sheets.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, STATUS_RANGE, "ROWS")
    rawData = rawData if not rawData == None else []
    isExists = False
    for raw in rawData:
        if raw[0] == ref:
            isExists = True
            if len(raw) > 1 and (raw[1] == "sold" or raw[1] == "ordered" or raw[1] == "preparing"):
                print "This ref was already sold or busy. Don't open."
                return False

    if not isExists:
        print "No ref exists."
        return False

    #check working status
    RAW_RANGE = EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_END_ROW
    rawData = sheets.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, RAW_RANGE, "ROWS")
    rawData = rawData if not rawData == None else []
    isExists = False
    targetRow = int(EnvSettings.ACCOUNT_INFO_START_ROW)
    for raw in rawData:
        if raw[0] == ref:
            isExists = True
            break
        targetRow = targetRow + 1

    if not isExists:
        print "No ref exists."
        return False

    PCNAME_RANGE = EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + EnvSettings.ACCOUNT_INFO_COMPUTERNAME_COL + str(targetRow)
    rawData = sheets.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, PCNAME_RANGE, "ROWS")

    if rawData != None:
        print "ref:" + ref + "is busy"
        return False
    
    return True

def killMultiPlayerManager():
    cmd = 'taskkill /im MultiPlayerManager.exe /t /F'
    returncode = subprocess.Popen(cmd, shell=True)

def killNoxInstance():
    cmd = 'taskkill /im Nox.exe /t /F'
    returncode = subprocess.Popen(cmd, shell=True)

def restartOS():
    cmd = 'shutdown.exe -r -t 60'
    returncode = subprocess.Popen(cmd, shell=True)

def getCredentials():
    f = open(os.path.join(EnvSettings.DATA_DIR_PATH , EnvSettings.CREDENTIALS_JSON_FILE))
    strCredentials = f.read()
    f.close()
    return strCredentials

def isNewVersionAvailable():
    x = 10
    delay = 1.0
    timeout = int(x / delay)
    
    command1 = ['git', 'fetch', 'https://github.com/noifuji/dmp-auto.git']
    proc1 = subprocess.Popen(command1,stdout = subprocess.PIPE, stderr=subprocess.STDOUT, shell  = False)
    timeout = int(x / delay)
    while proc1.poll() is None and timeout > 0:
        output = proc1.stdout.readline()
        if output:
            print output.strip()
        time.sleep(delay)
        timeout -= delay
        if timeout == 0:
            raise Exception("Command Timeout")

    while True:
        output = proc1.stdout.readline()
        if output:
            print output.strip()
        else:
            break
    
    command2 = ['git', 'diff', '--quiet', 'HEAD', 'FETCH_HEAD']
    proc2 = subprocess.Popen(command2,stdout = subprocess.PIPE, stderr=subprocess.STDOUT, shell  = False)
    timeout = int(x / delay)
    while proc2.poll() is None and timeout > 0:
        output = proc2.stdout.readline()
        if output:
            print output.strip()
        time.sleep(delay)
        timeout -= delay
        if timeout == 0:
            raise Exception("Command Timeout")

    while True:
        output = proc2.stdout.readline()
        if output:
            print output.strip()
        else:
            break
    
    if proc2.returncode == 1:
        return True
    else:
        return False

def dragDropAtSpeed(fromImg, toImg, speed):

    for retryLoop in range(5):
        if retryLoop >= 4:
            raise Exception
        
        currentSpeed = Settings.MoveMouseDelay
        toImgObj = None
        if isinstance(toImg, str) or isinstance(toImg, Pattern):
            res = findAny(toImg)
            if len(res) == 0:
                continue
            toImgObj = res[0]
        else:
            toImgObj = toImg
        toImg_gx = toImgObj.getX() + toImgObj.getW()/2 + toImgObj.getTargetOffset().getX()
        toImg_gy = toImgObj.getY() + toImgObj.getH()/2 + toImgObj.getTargetOffset().getY()
    
        fromImgObj = None
        if isinstance(fromImg, str) or isinstance(fromImg, Pattern):
            res = findAny(fromImg)
            if len(res) == 0:
                continue
            fromImgObj = res[0]
        else:
            fromImgObj = fromImg
        fromImg_gx = fromImgObj.getX() + fromImgObj.getW()/2 + fromImgObj.getTargetOffset().getX()
        fromImg_gy = fromImgObj.getY() + fromImgObj.getH()/2 + fromImgObj.getTargetOffset().getY()
        
        mouseMove(fromImg)
        mouseDown(Button.LEFT)
        wait(0.2)
        Settings.MoveMouseDelay = speed
        mouseMove(toImg_gx - fromImg_gx, toImg_gy - fromImg_gy)
        mouseUp(Button.LEFT)
        Settings.MoveMouseDelay = currentSpeed
        break

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

def fetchCurrentAccountCount(spreadsheet):
    status = spreadsheet.read(EnvSettings.ACCOUNT_INFO_SHEET_ID,
            EnvSettings.STATUS_INFO_SHEET_NAME + "!" + 
            EnvSettings.STATUS_INFO_REF_COL + "2:" + 
            EnvSettings.STATUS_INFO_STATUS_COL + "3000", 
            "ROWS")

    soldAccounts = []
    for s in status:
        if len(s) == 2:
            soldAccounts.append(s)
    
    raw = spreadsheet.read(EnvSettings.ACCOUNT_INFO_SHEET_ID,
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + 
            EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + 
            EnvSettings.ACCOUNT_INFO_PLAYERID_COL + EnvSettings.ACCOUNT_INFO_END_ROW, 
            "ROWS")

    accountsWithId = []
    for r in raw:
        if len(r) == 2:
            accountsWithId.append(r)

    count = 0
    for ac in accountsWithId:
        soldFlag = False
        for sold in soldAccounts:
            if ac[0] == sold[0]:
                soldFlag = True
                break
        if not soldFlag:
            count = count + 1

    return count

#PROCESSNAME
#DAILY, MAIN, LEGEND
def getNextRef(sheets, processname):
    COMPUTERNAME = os.environ["COMPUTERNAME"]
    
    col = ""
    if processname == "DAILY":
        col = EnvSettings.ACCOUNT_INFO_DAILY_COL
    elif processname == "MAIN":
        col = EnvSettings.ACCOUNT_INFO_MAIN_COL
    elif processname == "LEGEND":
        col = EnvSettings.ACCOUNT_INFO_LEGEND_COL
    elif processname == "LOGIN":
        col = EnvSettings.ACCOUNT_INFO_LOGIN_COL
    elif processname == "SP":
        col = EnvSettings.ACCOUNT_INFO_SP_END_COL
    progressRange = EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + col + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + col + EnvSettings.ACCOUNT_INFO_END_ROW

    #在庫表のステータス変更設定とrawを取得する。
    rawData = sheets.batchRead(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            [EnvSettings.ACCOUNT_INFO_SHEET_NAME + 
                "!" + EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + 
                EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_END_ROW,
                EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + EnvSettings.ACCOUNT_INFO_PLAYERID_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + 
                EnvSettings.ACCOUNT_INFO_PLAYERID_COL + EnvSettings.ACCOUNT_INFO_END_ROW, 
                EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + EnvSettings.ACCOUNT_INFO_COMPUTERNAME_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" +
                EnvSettings.ACCOUNT_INFO_COMPUTERNAME_COL + EnvSettings.ACCOUNT_INFO_END_ROW, 
                progressRange], "ROWS")
    if len(rawData) == 0:
        raise Exception("batchRead threw an error.")
    refs = rawData[0] if not rawData[0] == None else []
    ids = rawData[1] if not rawData[1] == None else []
    pcnames = rawData[2] if not rawData[2] == None else []
    status = rawData[3] if not rawData[3] == None else []
    refInfo = []
    for i in range(len(refs)):
        tmp = {}
        tmp["REF"] = refs[i][0]
        tmp["ROW_NO"] = i + 3
        if  i < len(ids) and len(ids[i]) > 0:
            tmp["ID"] = ids[i][0]
        else:
            tmp["ID"] = ""
            
        if  i < len(pcnames) and len(pcnames[i]) > 0:
            tmp["PC_NAME"] = pcnames[i][0]
        else:
            tmp["PC_NAME"] = ""
            
        if  i < len(status) and len(status[i]) > 0:
            tmp["STATUS"] = status[i][0]
        else:
            tmp["STATUS"] = ""
        refInfo.append(tmp)

    rawData = sheets.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, "status!A2:G1500", "ROWS")
    rawData = rawData if not rawData == None else []
    availableRefs = []
    for raw in rawData:
        tmp = {}
        if raw[1] == "sold" or raw[1] == "ordered":
            continue
        if processname == "DAILY":
            if raw[2] == "" or raw[2] == "skip":
                continue
        elif processname == "MAIN":
            if raw[3] == "" or raw[3] == "skip":
                continue
        elif processname == "LEGEND":
            if raw[4] == "" or raw[4] == "skip":
                continue
        elif processname == "LOGIN":
            if raw[5] == "" or raw[5] == "skip":
                continue
        elif processname == "SP":
            if raw[6] == "" or raw[6] == "skip":
                continue
        availableRefs.append(raw[0])

    
    candidates = []
    for ref in refInfo:
        if (ref["REF"] in availableRefs) and \
                (not ref["ID"] == "") and \
                (ref["PC_NAME"] == "" or ref["PC_NAME"] == COMPUTERNAME.decode('utf-8')) and \
                (ref["STATUS"] == "" or ref["STATUS"] == u"incomplete"):
            candidates.append(ref)

    if len(candidates) == 0:
        return None

    targetRef = None
    for c in candidates:
        if not c["PC_NAME"] == "":
            targetRef = c
            break
    if targetRef == None:
        targetRef = candidates[0]
        
    #空いてるrefのWORKERとSTATUSに書き込む
    sheets.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + EnvSettings.ACCOUNT_INFO_COMPUTERNAME_COL + str(targetRef["ROW_NO"]), 
            [[COMPUTERNAME]], "ROWS")

    wait(3)
    updatedPcname = sheets.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + EnvSettings.ACCOUNT_INFO_COMPUTERNAME_COL + str(targetRef["ROW_NO"]), "ROWS")
    
    if updatedPcname[0][0] == COMPUTERNAME:
        return targetRef["REF"]
    else:
        return None

def updateLastAccessDatetime(sheets):
    COMPUTERNAME = os.environ["COMPUTERNAME"]
    rawData = sheets.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, "state!A2:A100", "COLUMNS")
    rawData = rawData if not rawData == None else []
    targetRow = 2
    for p in rawData[0]:
        if p == COMPUTERNAME:
            break
        targetRow = targetRow + 1

    sheets.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            "state" + "!" + "B" + str(targetRow), 
            [[datetime.now().strftime("%Y/%m/%d %H:%M:%S")]], "ROWS")

def getRowOfRef(sheets, sheetname, refcol, ref):
    rawData = sheets.batchRead(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            [sheetname + 
                "!" + refcol + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + 
                EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_END_ROW
                ], "ROWS")

    if len(rawData) == 0:
        raise Exception("batchRead threw an error.")
    refs = rawData[0] if not rawData[0] == None else []
    refInfo = []
    for i in range(len(refs)):
        tmp = {}
        tmp["REF"] = refs[i][0]
        tmp["ROW_NO"] = i + 3
        refInfo.append(tmp)

    targetRow = ""
    for r in refInfo:
        if r["REF"] == str(ref):
            targetRow = r["ROW_NO"]
            break
    
    if targetRow == "":
        raise Exception("No working ref")

    return targetRow

def lockComputer(sheets, ref):
    COMPUTERNAME = os.environ["COMPUTERNAME"]
    targetRow = getRowOfRef(sheets, EnvSettings.ACCOUNT_INFO_SHEET_NAME, EnvSettings.ACCOUNT_INFO_REF_COL ,ref)

    sheets.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + EnvSettings.ACCOUNT_INFO_COMPUTERNAME_COL + str(targetRow), 
            [[COMPUTERNAME]], "ROWS")

def unlockComputer(sheets, ref):
    COMPUTERNAME = os.environ["COMPUTERNAME"]
    targetRow = getRowOfRef(sheets, EnvSettings.ACCOUNT_INFO_SHEET_NAME, EnvSettings.ACCOUNT_INFO_REF_COL ,ref)

    sheets.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + EnvSettings.ACCOUNT_INFO_COMPUTERNAME_COL + str(targetRow), 
            [[""]], "ROWS"
            )
    updateLastAccessDatetime(sheets)

def lockPrepare(sheets, ref):
    targetRow = getRowOfRef(sheets, EnvSettings.STATUS_INFO_SHEET_NAME, EnvSettings.STATUS_INFO_REF_COL ,ref)
    sheets.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            EnvSettings.STATUS_INFO_SHEET_NAME + "!" + EnvSettings.STATUS_INFO_STATUS_COL + str(targetRow), 
            [["preparing"]], "ROWS")
    

def unlockPrepare(sheets, ref):
    targetRow = getRowOfRef(sheets, EnvSettings.STATUS_INFO_SHEET_NAME, EnvSettings.STATUS_INFO_REF_COL ,ref)
    sheets.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            EnvSettings.STATUS_INFO_SHEET_NAME + "!" + EnvSettings.STATUS_INFO_STATUS_COL + str(targetRow), 
            [[""]], "ROWS")

def getAvailableTwitterID(sheets):
    rawData = sheets.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, "accounts!C4:G20", "ROWS")
    available = []
    for data in rawData:
        if data[3] == "available":
            available.append(data)
    return available

def lockTwitterID(sheets, acountname, ref):
    rawData = sheets.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, "accounts!C4:C20", "ROWS")
    count = 0
    for data in rawData:
        if data[0] == acountname:
            break
        count = count + 1
        
    sheets.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            "accounts!G" + str(count + 4), 
            [[ref]], "ROWS")

def unlockTwitterID(sheets, acountname):
    rawData = sheets.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, "accounts!C4:C20", "ROWS")
    count = 0
    for data in rawData:
        if data[0] == acountname:
            break
        count = count + 1
        
    sheets.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            "accounts!G" + str(count + 4), 
            [[""]], "ROWS")
    

def completeRef(sheets, ref, processname):
    col = ""

    if processname == "DAILY":
        col = EnvSettings.ACCOUNT_INFO_DAILY_COL
    elif processname == "MAIN":
        col = EnvSettings.ACCOUNT_INFO_MAIN_COL
    elif processname == "LEGEND":
        col = EnvSettings.ACCOUNT_INFO_LEGEND_COL
    elif processname == "LOGIN":
        col = EnvSettings.ACCOUNT_INFO_LOGIN_COL
    elif processname == "SP":
        col = EnvSettings.ACCOUNT_INFO_SP_END_COL
    progressRange = EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + col + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + col + EnvSettings.ACCOUNT_INFO_END_ROW


    #在庫表のステータス変更設定とrawを取得する。
    rawData = sheets.batchRead(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            [EnvSettings.ACCOUNT_INFO_SHEET_NAME + 
                "!" + EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + 
                EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_END_ROW,
                EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + EnvSettings.ACCOUNT_INFO_PLAYERID_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + 
                EnvSettings.ACCOUNT_INFO_PLAYERID_COL + EnvSettings.ACCOUNT_INFO_END_ROW, 
                EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + EnvSettings.ACCOUNT_INFO_COMPUTERNAME_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" +
                EnvSettings.ACCOUNT_INFO_COMPUTERNAME_COL + EnvSettings.ACCOUNT_INFO_END_ROW, 
                progressRange], "ROWS")
    
    if len(rawData) == 0:
        raise Exception("batchRead threw an error.")
    refs = rawData[0] if not rawData[0] == None else []
    ids = rawData[1] if not rawData[1] == None else []
    pcnames = rawData[2] if not rawData[2] == None else []
    status = rawData[3] if not rawData[3] == None else []
    refInfo = []
    for i in range(len(refs)):
        tmp = {}
        tmp["REF"] = refs[i][0]
        tmp["ROW_NO"] = i + 3
        if  i < len(ids) and len(ids[i]) > 0:
            tmp["ID"] = ids[i][0]
        else:
            tmp["ID"] = ""
            
        if  i < len(pcnames) and len(pcnames[i]) > 0:
            tmp["PC_NAME"] = pcnames[i][0]
        else:
            tmp["PC_NAME"] = ""
            
        if  i < len(status) and len(status[i]) > 0:
            tmp["STATUS"] = status[i][0]
        else:
            tmp["STATUS"] = ""
        refInfo.append(tmp)

    targetRow = ""
    for r in refInfo:
        if r["REF"] == str(ref):
            targetRow = r["ROW_NO"]
            break
    
    if targetRow == "":
        raise Exception("No working ref")
    
    sheets.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + col + str(targetRow), 
            [["complete"]], "ROWS")
    sheets.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + EnvSettings.ACCOUNT_INFO_COMPUTERNAME_COL + str(targetRow), 
            [[""]], "ROWS")

    updateLastAccessDatetime(sheets)

def deleteIdentifiers():
    cmd = ["del", EnvSettings.BACKUP_DIR_PATH+"\\", "/Q"]
    subprocess.Popen(cmd, shell=True)
    wait(3)

def backupDMPIdentifier(resource, ref):
    saveDirPath = EnvSettings.BACKUP_DIR_PATH
    backupFilePath = os.path.join(saveDirPath,'dmps' + str(ref) + '.ab')

    if not os.path.exists(saveDirPath):
        os.makedirs(saveDirPath)
    else:
        if os.path.exists(backupFilePath):
            if os.path.getsize(backupFilePath) < 5000:
                os.remove(backupFilePath)
            else:
                return True
            
    changeDirnameCmd = [EnvSettings.NoxAdbPath, "shell", "mv", r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays", r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays1"]
    subprocess.call(changeDirnameCmd)
    
    cmd = [EnvSettings.NoxAdbPath, 'backup', '-f', backupFilePath, 'jp.co.takaratomy.duelmastersplays']
    subprocess.Popen(cmd, shell=True)
    
    #バックアップ開始をクリック
    exists(resource.TITLE_FULLBACKUP, 60)
    wait(5)
    click(resource.BUTTON_DO_BACKUP)
    #完了まで待機
    if waitVanish(resource.TITLE_FULLBACKUP, 60):
        restoreDirnameCmd = [EnvSettings.NoxAdbPath, "shell", "rm", "-r" ,r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays"]
        subprocess.call(restoreDirnameCmd)
        print "dir removed"
        restoreDirnameCmd = [EnvSettings.NoxAdbPath, "shell", "mv", r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays1", r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays"]
        subprocess.call(restoreDirnameCmd)
        return True
    else:
        if os.path.exists(backupFilePath):
            os.remove(backupFilePath)
        
        restoreDirnameCmd = [EnvSettings.NoxAdbPath, "shell", "mv", r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays1", r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays"]
        subprocess.call(restoreDirnameCmd)
        raise Exception("Timeout. Backup failed.")

def loadRef(resources, ref, driveInstance):
    saveDirPath = EnvSettings.BACKUP_DIR_PATH
    restoreFilename = 'dmps' + str(ref) + '.ab'
    restoreFilePath = os.path.join(saveDirPath,restoreFilename)

    if os.path.exists(restoreFilePath) and os.path.getsize(restoreFilePath) < 5000:
        os.remove(restoreFilePath)

    if not os.path.exists(restoreFilePath):
        dlResult = driveInstance.downloadIdentifierFile(restoreFilename, EnvSettings.IDENTIFIER_DRIVE_DIR_ID, EnvSettings.BACKUP_DIR_PATH)
        if not dlResult:
            raise Exception("Ref Number " + ref + " doesn't exist.")
            
    #フォルダ名変更 call
    changeDirnameCmd = [EnvSettings.NoxAdbPath, "shell", "mv", r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays", r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays1"]
    subprocess.call(changeDirnameCmd)
    #レストア popen
    restoreCmd = [EnvSettings.NoxAdbPath, "restore", restoreFilePath]
    subprocess.Popen(restoreCmd, shell=True)

    exists(resources.BUTTON_DO_RESTORE, 60)
    wait(5)
    click(resources.BUTTON_DO_RESTORE)

    #完了まで待機
    if waitVanish(resources.TITLE_FULLRESTORE, 60):
        restoreDirnameCmd = [EnvSettings.NoxAdbPath, "shell", "rm", "-r" ,r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays"]
        subprocess.call(restoreDirnameCmd)
        print "dir removed"
        restoreDirnameCmd = [EnvSettings.NoxAdbPath, "shell", "mv", r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays1", r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays"]
        subprocess.call(restoreDirnameCmd)
        print "dir restored"
        return True
    else:
        restoreDirnameCmd = [EnvSettings.NoxAdbPath, "shell", "mv", r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays1", r"/storage/emulated/0/Android/data/jp.co.takaratomy.duelmastersplays"]
        subprocess.call(restoreDirnameCmd)
        raise Exception("Timeout. Load failed.")

#level:
#url:slackのwebhookのURL
#userid:slackのmemberID
#contents:送信するメッセージ
#appname:メッセージに表示する送信元の名前
def sendMessagetoSlack(level ,userid, contents, appname):
    if level == "DEBUG" and (EnvSettings.RUN_MODE == "INFO" or EnvSettings.RUN_MODE == "ERROR"):
        return

    if level == "INFO" and EnvSettings.RUN_MODE == "ERROR":
        return
    
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

def updateCardCount(spreadsheet, ref, nameCount, cardCount):
    if len(nameCount) != len(cardCount) or len(nameCount) != 5:
        raise Exception
    
    row = [[nameCount[4],cardCount[4],nameCount[3],cardCount[3],nameCount[2],cardCount[2],nameCount[1],cardCount[1],nameCount[0],cardCount[0]]]

    refs = spreadsheet.read(EnvSettings.ACCOUNT_INFO_SHEET_ID,
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" +
            EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_START_ROW +":" +
            EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_END_ROW,
            "ROWS")
    rowIndex = None
    for i in range(len(refs)):
        if refs[i][0] == str(ref):
            rowIndex = i + 3
            break
    spreadsheet.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + 
            EnvSettings.ACCOUNT_INFO_CARDCOUNT_START_COL + str(rowIndex) + ":" + 
            EnvSettings.ACCOUNT_INFO_CARDCOUNT_END_COL + str(rowIndex), 
            row, "ROWS")

def downloadQuestStatus(spreadsheet):
    print "downloadQuestStatus"
    statusRaw = spreadsheet.batchRead(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            [
                EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + 
                EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + 
                EnvSettings.ACCOUNT_INFO_PLAYERID_COL + EnvSettings.ACCOUNT_INFO_END_ROW, 
                EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + 
                EnvSettings.ACCOUNT_INFO_MAIN_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + 
                EnvSettings.ACCOUNT_INFO_SP_END_COL + EnvSettings.ACCOUNT_INFO_END_ROW, 
                ], "ROWS")
    if len(statusRaw) == 0:
        raise Exception("batchRead threw an error.")

    accounts = statusRaw[0]
    statuses = statusRaw[1]
    
    status = []
    for i in range(min([len(accounts), len(statuses)])):
        if len(accounts[i]) > 1:
            status.append({"REF":accounts[i][0], "MAIN":statuses[i][0], "LEGEND":statuses[i][1], "SP":statuses[i][2]})

    return status

def completeQuestStatus(spreadsheet, ref, questname):
    column = ""
    if questname == "MAIN":
        column = EnvSettings.ACCOUNT_INFO_MAIN_COL
    elif questname == "LEGEND":
        column = EnvSettings.ACCOUNT_INFO_LEGEND_COL
    elif questname == "SP":
        column = EnvSettings.ACCOUNT_INFO_SP_END_COL
    else:
        raise Exception("Invalid Argument")
    refs = spreadsheet.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + 
            EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + 
            EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_END_ROW, 
            "ROWS")
    rowIndex = None
    for i in range(len(refs)):
        if refs[i][0] == str(ref):
            rowIndex = i + 3
            break
    if rowIndex == None:
        return
    spreadsheet.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, EnvSettings.ACCOUNT_INFO_SHEET_NAME +"!" + column + str(rowIndex), [["complete"]], "ROWS")


#return ref
def getSetupAccountRef(spreadsheet):
    refs = spreadsheet.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + 
            EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + 
            EnvSettings.ACCOUNT_INFO_PLAYERID_COL + EnvSettings.ACCOUNT_INFO_END_ROW,
            "ROWS")
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
def uploadStatistics(spreadsheet, sheetname, statistics):
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
    spreadsheet.append(EnvSettings.STATISTICS_SHEET_ID, sheetname + "!A1", row, "ROWS")

def updatePlayerId(spreadsheet, ref, playerId, computername):
    print "updatePlayerId"
    refs = spreadsheet.read(EnvSettings.ACCOUNT_INFO_SHEET_ID,
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + 
            EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + 
            EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_END_ROW, 
            "ROWS")
    rowIndex = None
    for i in range(len(refs)):
        if refs[i][0] == str(ref):
            if len(refs[i]) > 1 and refs[i][1] != "":
                return False
            rowIndex = i + 3
            break
    spreadsheet.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + 
            EnvSettings.ACCOUNT_INFO_PLAYERID_COL + str(rowIndex), [[playerId]], "ROWS")
    spreadsheet.write(EnvSettings.ACCOUNT_INFO_SHEET_ID, 
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" +
            EnvSettings.ACCOUNT_INFO_CREATEDATE_COL + str(rowIndex), [[datetime.now().strftime("%Y/%m/%d")]], "ROWS")#aaa

    return True

def updateAccountInfo(spreadsheet, ref, lv, dmp, gold, packs1, packs2):
    row = [[lv, dmp, gold]]
    row[0].extend(packs1)

    row2 = [packs2]
    
    refs = spreadsheet.read(EnvSettings.ACCOUNT_INFO_SHEET_ID,
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + 
            EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_START_ROW + ":" + 
            EnvSettings.ACCOUNT_INFO_REF_COL + EnvSettings.ACCOUNT_INFO_END_ROW, "ROWS")
    rowIndex = None
    for i in range(len(refs)):
        if refs[i][0] == str(ref):
            rowIndex = i + 3
            break
        
    if rowIndex == None:
        return
    
    spreadsheet.write(EnvSettings.ACCOUNT_INFO_SHEET_ID,
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + 
            EnvSettings.ACCOUNT_INFO_START_COL + str(rowIndex) + ":" + 
            EnvSettings.ACCOUNT_INFO_END_COL + str(rowIndex), row, "ROWS")

    if len(row2[0]) > 0:
        spreadsheet.write(EnvSettings.ACCOUNT_INFO_SHEET_ID,
            EnvSettings.ACCOUNT_INFO_SHEET_NAME + "!" + 
            EnvSettings.ACCOUNT_INFO_START_COL2 + str(rowIndex) + ":" + 
            EnvSettings.ACCOUNT_INFO_END_COL2 + str(rowIndex), row2, "ROWS")

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
    print "scanNumberChangeWidth"
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
            num = num.replace(",", "")
            if isNumber(num):
                print len(num)
                WIDTH_CONFIRM = len(num) * WIDTH_A_CHAR + MARGIN_LEFT
                break

        for num in range(1000):
            reg = None
            if RightLeft == 0:
                reg = Region(res[0].getX()+offsetX, res[0].getY()+offsetY, WIDTH_CONFIRM - dW*num, height)
            elif RightLeft == 1:
                reg = Region(res[0].getX()+offsetX + WIDTH_INIT - WIDTH_CONFIRM + dW*num, res[0].getY()+offsetY, WIDTH_CONFIRM - dW*num, height)
            else:
                raise Exception("Illegal argumant RightLeft : " + str(RightLeft))
            reg.highlight(0.1)
            num = OCR.readWord(reg)
            num = num.replace(",", "")
            if isNumber(num):
                    break
    return num

def scanAccountInfo(resource):
    ts = resource.TITLE_PACK_ARRAY

    dmp = 0
    gold = 0
    tempPacks = {}
    lv = ""

    OFFSET_X = 80
    OFFSET_Y = 96
    WIDTH_INIT = 60
    HEIGHT = 27
    WIDTH_INIT_LONG = 110
    
    OFFSET_X_LV = 270
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
            wait(2)
            break

    lv = scanNumberChangeWidth(resource.TITLE_PLAYER_LV, OFFSET_X_LV, OFFSET_Y_LV, WIDTH_INIT_LV, HEIGHT_LV, 1, 35)

    
    click(resource.BUTTON_ITEM)
    wait(1)

    scanCount = 0
    for i in range(len(ts)):
        res = scanNumberChangeWidth(ts[i]["IMAGE"], OFFSET_X, OFFSET_Y, WIDTH_INIT, HEIGHT, 0, 20)
        if res == "":
            tempPacks[ts[i]["NAME"]] = "0"
        else:
            tempPacks[ts[i]["NAME"]] = res
            scanCount += 1
            if scanCount % 2 == 0:
                Settings.MoveMouseDelay = 3
                dragDrop(resource.TITLE_ITEM_DRAG, resource.TITLE_ITEM_DROP)
                Settings.MoveMouseDelay = 0.1
                wait(1)
    
    click(resource.BUTTON_OTHER)
    wait(1)


    gold = scanNumberChangeWidth(resource.TITLE_GOLD, OFFSET_X, OFFSET_Y, WIDTH_INIT_LONG, HEIGHT, 0, 20)
    dmp = scanNumberChangeWidth(resource.TITLE_DMPOINT, OFFSET_X, OFFSET_Y, WIDTH_INIT_LONG, HEIGHT, 0, 20)

    packs1 = []
    for name in resource.PACK_NAME_ARRAY1:
        packs1.append(int(tempPacks[name]))

    packs2 = []
    for name in resource.PACK_NAME_ARRAY2:
        packs2.append(int(tempPacks[name]))
    
    return [lv, dmp, gold, packs1, packs2]

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

def countAllCardsByRarity(resource):
    names = []
    cards = []

    #カードリストリージョンを取得する。
    cardListTitle = findAny(resource.TITLE_CARD_LIST)
    if len(cardListTitle) <= 0:
        raise Exception("failed to detect CardList")
    cardListX = cardListTitle[0].getX()
    cardListY = cardListTitle[0].getY()
    if resource.APP_ENGINE == "NOX":
        cardListW = 1340
        cardListH = 620
    elif resource.APP_ENGINE == "ANDAPP":
        cardListW = 1340
        cardListH = 690
    else:
        raise Exception("Invalid App Engine")

    cardListRegion = Region(cardListX,cardListY,cardListW,cardListH)
    cardListRegionTopHalf = Region(cardListX, cardListY, cardListW, cardListH/2)
    cardListRegionBottomHalf = Region(cardListX, cardListY + cardListH/2, cardListW, cardListH/2)

    for rarity in resource.BUTTON_RARITIES:
        click(resource.BUTTON_FILTER)
        click(resource.BUTTON_RESET)
        click(rarity)
        wheel(rarity,Button.WHEEL_DOWN, 40)
        wait(3)
        click(resource.BUTTON_BASIC)
        for b in resource.BUTTON_DMPPS:
            click(b)
            wait(2)
        click(resource.BUTTON_OK)
        wait(0.5)
        
        targets = resource.ICON_CARD_COUNT
        
        count = [0,0,0,0]
        confirmedCount = [0,0,0,0]
        wheelCount = 0
    
        if exists(resource.SCROLL1, 0.5) == None:
            num = 0
            for target in targets :
                cardListRegion.highlight(0.1)
                f = Finder(SCREEN.capture(cardListRegion))
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
                cardListRegionTopHalf.highlight(0.1)
                f = Finder(SCREEN.capture(cardListRegionTopHalf))
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
            
            if exists(resource.SCROLL2,0.5) != None:
                num = 0
                for target in targets :
                    cardListRegionBottomHalf.highlight(0.1)
                    f = Finder(SCREEN.capture(cardListRegionBottomHalf))
                    f.findAll(target)
                    result = []
                    while f.hasNext():
                       result.append(f.next())
                    confirmedCount[num] += len(result)
                    num += 1
                break

            if resource.APP_ENGINE == "NOX":
                dragDropAtSpeed(Pattern("1603354588837.png").targetOffset(22,470),Pattern("1603354588837.png").targetOffset(28,163) , 2.5)
            elif resource.APP_ENGINE == "ANDAPP":
                wheel(resource.TITLE_CARD_LIST, Button.WHEEL_DOWN, 4)
            else:
                raise Exception("Invalid App Engine")
            
        names.append(sum(confirmedCount))
        cards.append(confirmedCount[0]*1 + confirmedCount[1]*2 + confirmedCount[2]*3 + confirmedCount[3]*4)

    
    print "C :" + str(names[0]) + "Card Names / " + str(cards[0]) + "Cards"
    print "UC:" + str(names[1]) + "Card Names / " + str(cards[1]) + "Cards"
    print "R :" + str(names[2]) + "Card Names / " + str(cards[2]) + "Cards"
    print "VR:" + str(names[3]) + "Card Names / " + str(cards[3]) + "Cards"
    print "SR:" + str(names[4]) + "Card Names / " + str(cards[4]) + "Cards"
    return {"NAMES" : names, "CARDS" : cards}

def chooseDeck(resource, deckImage):
    print "chooseDeck"
    print deckImage
    if exists(deckImage, 2) != None:
        print "deckImage was found"
        click(deckImage)
        return True
    else:
        wheel(resource.TITLE_DECKLIST, Button.WHEEL_DOWN, 7)
        wait(5)
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
    for okLoop in range(100):
        if len(findAny(resource.BUTTON_OK)) > 0:
            try:
                click(resource.BUTTON_OK)
            except:
                print "failed to click"
        if len(findAny(resource.TITLE_DECKLIST)) > 0:
            break
        wait(0.5)

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
    try:
        #中断されたデュエル
        if len(findAny(resource.MESSAGE_RESTART_DUEL)) > 0:
            print 'A stopped duel is detected. It will be canceled.'
            click(resource.BUTTON_CANCEL)
        #前回のリザルト表示
        if len(findAny(resource.MESSAGE_LAST_SP_BATTLE)) > 0 :
            print 'The last SP duel result detected.'
            click(resource.BUTTON_OK)
            return -1
        #前回のリザルト表示
        if len(findAny(resource.MESSAGE_LAST_BATTLE)) > 0 :
            print 'The last duel result detected.'
            click(resource.BUTTON_OK)
        
        #アカウント連携
        #if len(findAny(resource.BUTTON_LATER)) > 0 :
     #       print 'Account backup recommendation'
     #       click(resource.BUTTON_LATER)
        
     #   if len(findAny(resource.AD)) > 0:
     #       print 'Ads was skipped.'
      #      if len(findAny(resource.BUTTON_OK)) > 0:
       #         click(resource.BUTTON_OK)
        wait(1)
    except:
        print "failed to click"
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

def changeMission(resource):
    print "changeMission"
    if exists(resource.MISSION_DRAW_20["IMAGE"], 1) != None:
        click(resource.MISSION_DRAW_20["IMAGE"])
        if exists(resource.BUTTON_OK, 10) != None:
            click(resource.BUTTON_OK)
            wait(1)
        wait(5)
        return
    if exists(resource.MISSION_WIN_3["IMAGE"], 1) != None:
        click(resource.MISSION_WIN_3["IMAGE"])
        if exists(resource.BUTTON_OK, 10) != None:
            click(resource.BUTTON_OK)
            wait(1)
        wait(5)
        return

def closeMission(resource):
    print "closeMission"
    for closeMissionLoop in range(10): 
        type(Key.ESC)
        wait(10)
        if waitVanish(resource.TITLE_MISSION, 60):
            break

def getTargetMissions(resource):
    print "getTargetMissions"
    
    missionTitle = findAny(resource.TITLE_MISSION)
    if len(missionTitle) <= 0:
        return []
    
    offsetRBX1 = 956
    offsetRBY1 = 225
    offsetRBY2 = 339
    offsetRBY3 = 459
    RBWidth = 180
    RBHeight = 78
    RBRegs = [
            Region(missionTitle[0].getX() + offsetRBX1, missionTitle[0].getY() + offsetRBY1, RBWidth, RBHeight),
            Region(missionTitle[0].getX() + offsetRBX1, missionTitle[0].getY() + offsetRBY2, RBWidth, RBHeight),
            Region(missionTitle[0].getX() + offsetRBX1, missionTitle[0].getY() + offsetRBY3, RBWidth, RBHeight)
            ]
    isMissionCompleted = []
    for region in RBRegs:
        region.highlight(0.1)
        detected = region.findAny(resource.BUTTON_CHANGE_MISSION)
        if len(detected) > 0:
            isMissionCompleted.append(False)
        else:
            isMissionCompleted.append(True)

    offsetX1 = 325#10
    offsetY1 = 193#185
    offsetY2 = 310#355
    offsetY3 = 425#525
    width = 821
    height = 53
    missionRegs = [
            Region(missionTitle[0].getX() + offsetX1, missionTitle[0].getY() + offsetY1, width, height),
            Region(missionTitle[0].getX() + offsetX1, missionTitle[0].getY() + offsetY2, width, height),
            Region(missionTitle[0].getX() + offsetX1, missionTitle[0].getY() + offsetY3, width, height)
            ]
    missionsList = []
    for num in range(3):
        #missionsList.append([ m for m in resource.MISSIONS if m["POSITION"] == (num+1) ])
        missionsList.append([ m for m in resource.MISSIONS ])

        
    targetMissions = []
    for reg, missions, isCompleted in zip(missionRegs, missionsList, isMissionCompleted):
        if isCompleted:
            continue
        
        reg.highlight(0.1)
        scores = []
        for ms in missions:
           detected = reg.findAny(ms["IMAGE"])
           if len(detected) > 0:
               scores.append(detected[0].getScore())
               print detected[0].getScore()
           else:
               scores.append(0)
               print 0
        max_value = max(scores)
        if max_value >= 0.7:
            max_index = scores.index(max_value)
            targetMissions.append(missions[max_index])
                
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
    elif mission["GROUP"] == "DEST":
        strategyCode = 4
    elif mission["GROUP"] == "LARGE":
        strategyCode = 5
    elif mission["GROUP"] == "RETIRE":
        strategyCode = 6
    elif mission["GROUP"] == "BREAK3":
        strategyCode = 7
    elif mission["GROUP"] == "WIN4SHIELDS":
        strategyCode = 8
        
    return strategyCode

#return 0 正常にバトル開始
#return -1 異常発生
def waitStartingGame(resource):
    print 'waitStartingGame'
    WAIT_TIME = 90
    myTurnCount = 0
    for num in range(WAIT_TIME):
        print "waiting game start..." + str(num) + "/" + str(WAIT_TIME)
        #ストーリースキップ
        skipStory(resource)
        #マッチングしなかった場合
        if len(findAny(resource.MESSAGE_NO_OPPONENTS)) > 0:
            try:
                click(resource.BUTTON_OK)
                wait(resource.BUTTON_SMALL_BATTLE_START, 60)
                click(resource.BUTTON_SMALL_BATTLE_START)
                wait(resource.BUTTON_LARGE_BATTLE_START,60)
                click(resource.BUTTON_LARGE_BATTLE_START)
                return -1
            except:
                print "failed to click"
        if len(findAny(resource.BUTTON_RETRY)) > 0:
            click(resource.BUTTON_RETRY)

        if len(findAny(resource.MESSAGE_ERROR_9003)) > 0:
            raise Exception

            
        if len(findAny(resource.MESSAGE_CONNECTION_LOST)) >0 :
            click(resource.BUTTON_OK)
            exists(resource.ICON_EXTRA,120)
            return -1

        if len(findAny(resource.BUTTON_TURN_END)) > 0:
            myTurnCount += 1
            print "myTurnCount:" + str(myTurnCount)
            if myTurnCount >= 2:
                break

        if len(findAny(resource.BUTTON_SMALL_BATTLE_START)) > 0:
            break

        if num >= (WAIT_TIME-1):
            raise Exception("Too many waitStartingGame loop")
        wait(1)
    return 0

#Nox
#OFFSET_X = -240
#OFFSET_Y = 284
#WIDTH = 118
#HEIGHT = 70
def getMainStoryStage(resource):
    offsetX = resource.STAGE_REGION_OFFSETS["x"]
    offsetY = resource.STAGE_REGION_OFFSETS["y"]
    width = resource.STAGE_REGION_OFFSETS["w"] 
    height = resource.STAGE_REGION_OFFSETS["h"] 
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
    print 'openMainStory'
    breakCount = 0
    for openStoryLoop in range(100):
        if len(findAny(resource.ICON_SOLO_PLAY)) > 0:
            click(resource.ICON_SOLO_PLAY)
            wait(3)
        if len(findAny(resource.BUTTON_MAIN_STORY)) > 0:
            click(resource.BUTTON_MAIN_STORY)
        if len(findAny(resource.BUTTON_BACK)) > 0:
            click(resource.BUTTON_BACK2)
        if len(findAny(resource.BUTTON_CONFIRM_REWARD)) > 0:
            try:
                click(resource.BUTTON_CONFIRM_REWARD)
                if exists(resource.TITLE_REWARD_INFO,1) != None:
                    type(Key.ESC)
                    waitVanish(resource.TITLE_REWARD_INFO, 5)
                    break
            except:
                print "failed to click"

def openCityBattle(resource):
    print 'openCityBattle'
    breakCount = 0
    for openStoryLoop in range(100):
        if len(findAny(resource.ICON_SOLO_PLAY)) > 0:
            click(resource.ICON_SOLO_PLAY)
            wait(3)
        if len(findAny(resource.BUTTON_CITY_BATTLE)) > 0:
            click(resource.BUTTON_CITY_BATTLE)
        if len(findAny(resource.BUTTON_BACK)) > 0:
            click(resource.BUTTON_BACK2)
        if len(findAny(resource.BUTTON_CONFIRM_REWARD)) > 0:
            try:
                click(resource.BUTTON_CONFIRM_REWARD)
                if exists(resource.TITLE_REWARD_INFO,1) != None:
                    type(Key.ESC)
                    waitVanish(resource.TITLE_REWARD_INFO, 5)
                    break
            except:
                print "failed to click"
        if len(findAny(resource.TITLE_REWARD_INFO)) > 0:
            type(Key.ESC)
            waitVanish(resource.TITLE_REWARD_INFO, 5)
            break
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
    if episode == 1 and stage in [1,2,3,4,5,6,7,8,9,10,11,13,14,15]:
        strategy = 2
    elif episode == 2 and stage in [6,13]:
        strategy = 2
    elif episode == 2 and stage in [4,9]:
        strategy = 104
    elif episode == 2 and stage in [10]:
        strategy = 102
    elif episode == 2 and stage in [12,13,15]:
        strategy = 103
    elif episode == 3 and stage in [2,5,6,9,10]:
        strategy = 103
    elif episode == 4 and stage in [1,3,7,9]:
        strategy = 103
    else:
        strategy = 100
        
    return strategy

def getDeckByStrategy(resource, strategy):
    if strategy == 1:
        return [resource.DECKIMAGE_STSPELL, getDeckCode("DECKCODE_STSPELL")]
    elif strategy == 2 or strategy == 6:
         return [resource.DECKIMAGE_RED_BLACK, getDeckCode("DECKCODE_RED_BLACK")]
    elif strategy == 3:
         return [resource.DECKIMAGE_ST, getDeckCode("DECKCODE_ST")]
    elif strategy == 4:
         return [resource.DECKIMAGE_DEST, getDeckCode("DECKCODE_DEST")]
    elif strategy == 5:
        return [resource.DECKIMAGE_LARGE_CREATURE, getDeckCode("DECKCODE_LARGE_CREATURE")]
    elif strategy == 7:
         return [resource.DECKIMAGE_RED_BLACK, getDeckCode("DECKCODE_RED_BLACK")]
    elif strategy == 8:
         return [resource.DECKIMAGE_LARGE_CREATURE, getDeckCode("DECKCODE_LARGE_CREATURE")]
    elif strategy == 100:
        return [resource.DECKIMAGE_MAIN, getDeckCode("DECKCODE_MAIN")]
    elif strategy == 101:
        return [resource.DECKIMAGE_SPBATTLE, getDeckCode("DECKCODE_SP")]
    elif strategy == 102:
        return [resource.DECKIMAGE_FATTY, getDeckCode("DECKCODE_FATTY")]
    elif strategy == 103:
        return [resource.DECKIMAGE_HAKUHO, getDeckCode("DECKCODE_HAKUHO")]
    elif strategy == 104:
        return [resource.DECKIMAGE_AGRO, getDeckCode("DECKCODE_AGRO")]
    else:
        return None

#only for Nox
def getPresent(resource):
    if len(findAny(resource.ICON_PRESENT_WITH_SIGN)) > 0:
        click(resource.ICON_PRESENT_WITH_SIGN) 
        for presentLoop in range(100):
            if len(findAny(resource.TITLE_PRESENT)) > 0:
                click(resource.BUTTON_RECIEVE)
            if len(findAny(resource.BUTTON_OK)) > 0:
                click(resource.BUTTON_OK)
                wait(3)
                type(Key.ESC)
                waitVanish(resource.TITLE_PRESENT)
                break

#only for Nox
def getMissionRewards(resource):
    if len(findAny(resource.ICON_MISSION)) > 0:
        click(resource.ICON_MISSION) 
        exists(resource.TITLE_MISSION, 60)
        if len(findAny(resource.BUTTON_MISSION_WITH_SIGN)) > 0:
            if len(findAny(resource.BUTTON_DAILY_REWARD_RECEIVE_ALL)) > 0:
                click(resource.BUTTON_DAILY_REWARD_RECEIVE_ALL)
                exists(resource.BUTTON_OK, 60)
                type(Key.ESC)
                wait(3)
            #for num in range(10):
            #    if len(findAny(resource.ICON_ACHIEVED)) > 0:
            #        click(resource.ICON_ACHIEVED)
            #        exists(resource.BUTTON_OK, 60)
            #        type(Key.ESC)
            #        waitVanish(resource.TITLE_REWARD_DAILY, 5)
            #    else:
            #        break

        if len(findAny(resource.BUTON_ACHIEVEMENTS_WITH_SIGN)) > 0:
            click(resource.BUTON_ACHIEVEMENTS_WITH_SIGN)
            wait(3)
            if len(findAny(resource.BUTTON_DAILY_REWARD_RECEIVE_ALL)) > 0:
                click(resource.BUTTON_DAILY_REWARD_RECEIVE_ALL)
                exists(resource.BUTTON_OK, 60)
                click(resource.BUTTON_OK)
                waitVanish(resource.TITLE_REWARD_DAILY, 5)

        closeMission(resource)

def getBeginnerRewards(resources):
    #通知あり初心者アイコンあり
    if exists(resources.ICON_CLOVER_WITH_SIGN, 3) != None:
        try:
            click(resources.ICON_CLOVER_WITH_SIGN)
        except:
            print "failed to click"
        for num in range(100):
            type(Key.ESC)
            if exists(resources.MESSAGE_CONFIRM_BACK_TITLE,1) != None:
                wait(1)
                type(Key.ESC)
                break
    wait(1)
    packRewardFlag = False
    if exists(resources.ICON_CLOVER, 3) != None:
        try:
            click(resources.ICON_CLOVER)
        except:
            print "failed to click"
        exists(resources.BUTTON_CLOSE, 60)
        if len(findAny(resources.OPEN_CARD_PACK_REWARD)) == 0:
            packRewardFlag = False
        else:
            packRewardFlag = True
        
        for num in range(100):
            type(Key.ESC)
            if exists(resources.MESSAGE_CONFIRM_BACK_TITLE,1) != None:
                wait(1)
                type(Key.ESC)
                break
    return packRewardFlag

def openCardPack(resources):
    click(resources.ICON_SHOP)
    for shopTutorialLoop in range(5):
        click(Pattern("1604912893427.png").targetOffset(79,-49))
        wait(1)
    wait(5)
    click(Pattern("1596592864693.png").similar(0.90).targetOffset(-5,-237))
    wait(5)
    click(Pattern("1596592907696.png").similar(0.90).targetOffset(-6,-215))
    exists(resources.BUTTON_BACK, 120)
    for shopTutorialLoop in range(5):
        click(Pattern("1603247550151.png").targetOffset(3,75))
        wait(1)
        
    print 'Opening pack'
    if exists("1608821210779.png",2) != None:
        click(Pattern("1608821210779.png").targetOffset(-1,60))
    else:
        for num in range(100):
            type(Key.ESC)
            if exists(resources.MESSAGE_CONFIRM_BACK_TITLE, 1) != None:
                type(Key.ESC)
                return
    exists("1603251877777.png",30)
    click(resources.BUTTON_OK)
    wait(1)
    click(resources.BUTTON_OK)
    exists("1596593059270.png",10)
    click("1596593059270.png")

    for pack_loop in range(10):
        if exists(resources.BUTTON_OK,5) == None:
            print 'You got super rare.'
            #スーパーレア発生
            click(Pattern("1597929821232.png").targetOffset(561,167))
            continue
        else:
            break

    for pack_loop in range(10):
        if exists(resources.BUTTON_OK,1) != None:
            click(resources.BUTTON_OK)
            print 'OK is clicked to confirm pack results.'
            wait(2)
            continue
        else:
            break
    wait(1)
    exists("1596593154431.png",10)
    for num in range(100):
        type(Key.ESC)
        if exists(resources.MESSAGE_CONFIRM_BACK_TITLE, 1) != None:
            type(Key.ESC)
            break

def openOmikuji(resources):
    click(resources.ICON_SHOP)
    for shopTutorialLoop in range(5):
        click(Pattern("1604912893427.png").targetOffset(79,-49))
        wait(1)
    wait(5)
    click(Pattern("1596592864693.png").similar(0.90).targetOffset(-5,-237))
    wait(5)
    click(Pattern("1596592907696.png").similar(0.90).targetOffset(-6,-215))
    exists(resources.BUTTON_BACK, 120)
    for shopTutorialLoop in range(5):
        click(Pattern("1603247550151.png").targetOffset(3,75))
        wait(1)
    print 'Opening pack'
    if exists(Pattern("1609459748285.png").similar(0.97),2) != None:
        click(Pattern("1609459748285.png").similar(0.97))
    else:
        for num in range(100):
            type(Key.ESC)
            if exists(resources.MESSAGE_CONFIRM_BACK_TITLE, 1) != None:
                type(Key.ESC)
                return
    exists("1603251877777.png",30)
    click(resources.BUTTON_OK)
    wait(1)
    click(resources.BUTTON_OK)
    exists("1596593059270.png",10)
    click("1596593059270.png")

    for pack_loop in range(10):
        if exists(resources.BUTTON_OK,5) == None:
            print 'You got super rare.'
            #スーパーレア発生
            click(Pattern("1597929821232.png").targetOffset(561,167))
            continue
        else:
            break

    for pack_loop in range(10):
        if exists(resources.BUTTON_OK,1) != None:
            click(resources.BUTTON_OK)
            print 'OK is clicked to confirm pack results.'
            wait(2)
            continue
        else:
            break
    wait(1)
    exists("1596593154431.png",10)
    for num in range(100):
        type(Key.ESC)
        if exists(resources.MESSAGE_CONFIRM_BACK_TITLE, 1) != None:
            type(Key.ESC)
            break

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

def isMainOn(resources):
    App(EnvSettings.NoxMultiPlayerPath).open()
    if exists(resources.TITLE_MULTI_PLAYER,120) == None:
        killMultiPlayerManager()
        raise Exception("MultiPlayerManager has error. Please retry to launch.")
    exists(resources.BUTTON_NOX_PLAY, 120)
    click(resources.ICON_SEARCH)
    wait(2)
    type("MAIN")
    wait(1)
    type(Key.ENTER)
    wait(10)
    if len(findAny(resources.BUTTON_NOX_STOP)) > 0:
        result = True
    else:
        result = False
    App(EnvSettings.NoxMultiPlayerPath).close()
    wait(5)
    return result

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
        if waitVanish(resources.BUTTON_NOX_STOP, 180) == False:
            print "Nox instance stays."
            killMultiPlayerManager()
            killNoxInstance()
            raise Exception("Failed to close instance. Retrying...")
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

def renameRunningNoxInstance(resources, ref):
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
        click(resources.BUTTON_NOX_RENAME)
        for bkLoop in range(20):
            type(Key.BACKSPACE)
        type(ref)
        type(Key.ENTER)
        wait(1)
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
        if len(findAny(resources.MESSAGE_LAUNCHER_STOPPED_MANY_TIMES)) > 0:
            try:
                click(resources.MESSAGE_LAUNCHER_STOPPED_MANY_TIMES)
            except:
                print "failed to click"
        if len(findAny(resources.ICON_BROWSER)) > 0:
            break
        if len(findAny(resources.MESSAGE_ONECLICK_ERROR)) > 0:
            raise Exception("One Click Recovery Error")
        if noxLaunchLoop >= 599:
            killMultiPlayerManager()
            raise Exception("Too many noxLaunchLoops")
        wait(1)
    wait(30)
    if len(findAny(resources.MESSAGE_BACKUP)) > 0:
        click(resources.MESSAGE_BACKUP)
        click(0.2)
        click(resources.MESSAGE_BACKUP_NODISP)
        wait(1)
        click(resources.BUTTON_NOX_OK)


def RestartApp(resource):
    DOWNLOAD_TIMEOUT = 600
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
    for num in range(360):
        print "loading opening page......" + str(num)
        if resource.APP_ENGINE == "NOX":
            if len(findAny("1597912712276.png")) > 0:
                print "An update is found."
                skipUpdateFlag = False
                break

            if len(findAny(resource.MESSAGE_SYSTEM_UI_STOPPED)) > 0:
                print "UI Error is detected."
                try:
                    click(resource.MESSAGE_SYSTEM_UI_STOPPED)
                    wait(10)
                    noxCallStartDMPApp()
                except:
                    print "failed to click"
            
            if len(findAny(resource.MESSAGE_FAILED_TO_START_LAUNCHER)) > 0:
                print "Android Error is detected."
                try:
                    click(resource.MESSAGE_FAILED_TO_START_LAUNCHER)
                except:
                    print "failed to click"
                break
        if len(findAny(resource.BUTTON_ACCEPT)) > 0:
            try:
                click(resource.BUTTON_ACCEPT)
            except:
                print "failed to click"
            break
        
        if len(findAny(resource.MESSAGE_MAINTENANCE)) > 0:
            wait(1800)
            click(resource.BUTTON_OK)
        
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
    #click(resource.BUTTON_MENU)
    #exists(resource.BUTTON_CLEAR_CACHE,180)
    #click(resource.BUTTON_CLEAR_CACHE)
    #exists(resource.BUTTON_OK,180)
   #click(resource.BUTTON_OK)
    #wait(0.5)
    #exists(resource.BUTTON_OK,180)
    #click(resource.BUTTON_OK)
    #wait(0.5)
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
        if len(findAny(resource.BUTTON_SKIP)) > 0 or len(findAny(resource.ICON_HOME)) > 0 or len(findAny(resource.BUTTON_TAP_AND_NEXT)) > 0:
            print "Loading is finished."
            skipDownloadFlag = True
            break
        if num >= 179:
           raise Exception 
        wait(2)
    if skipDownloadFlag == False:
        click(resource.BUTTON_OK)
        for downloadLoop in range(DOWNLOAD_TIMEOUT):
            print "downloading..." + str(downloadLoop)
            if len(findAny(resource.BUTTON_SKIP)) > 0 or len(findAny(resource.ICON_HOME)) > 0 or len(findAny(resource.BUTTON_TAP_AND_NEXT)) > 0:
                print "finished"
                break
            if downloadLoop >= (DOWNLOAD_TIMEOUT-1):
                raise Exception
            wait(1)
    #結果発表をスキップ
    for resultLoop in range(60):
        print "checking monthly competition result...." + str(resultLoop)
        if len(findAny(resource.ICON_HOME)) > 0:
            break
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
        if len(findAny(resource.ICON_HOME)) > 0:
            break
        if len(findAny(resource.BUTTON_SKIP)) > 0: 
            click(resource.BUTTON_SKIP)
            wait(1)
        if len(findAny(resource.BUTTON_OK)) > 0:
            click(resource.BUTTON_OK)
            wait(1)
        wait(1)
    for skipLoop in range(120):
        if skipNotifications(resource) == -1:
            exists(resource.BUTTON_SMALL_OK, 60)
            for backLoop in range(60):
                print "backLoop"
                if len(findAny(resource.BUTTON_SMALL_OK)) > 0:
                    try:
                        click(resource.BUTTON_SMALL_OK)
                    except:
                        print "failed to click"
                type(Key.ESC)
                wait(1)
                if exists(resource.MESSAGE_BACK_TO_TITLE, 1) != None:
                    type(Key.ESC)
                    wait(1)
                    break
        if exists(resource.BUTTON_QUICKPICK_REWARD, 0.5) != None:
            click(resource.BUTTON_QUICKPICK_REWARD)
            wait(5)
            click(resource.BUTTON_OK)
            
        if exists(resource.MESSAGE_BACK_TO_TITLE, 0.5) != None:
            type(Key.ESC)
            wait(1)
            break
        type(Key.ESC)
        wait(1)
    #解像度設定の変更
    if resource.APP_ENGINE == "NOX":
        extra = findAny(resource.ICON_EXTRA)
        if len(extra) > 0 and extra[0].getScore() < 0.99:
            click(resource.ICON_OTHER)
            wait(3)
                            
            if exists(resource.BUTTON_SETTINGS,5) != None:
                click(resource.BUTTON_SETTINGS)

                if exists(resource.BUTTON_GAME_SETTINGS,5) != None:
                    click(resource.BUTTON_GAME_SETTINGS)
                
                exists("1603422361520.png", 60)
                dragDropAtSpeed(Pattern("1603422361520.png").targetOffset(28,548), Pattern("1603422361520.png").targetOffset(-3,-73), 2)
                click(Pattern("1604913302661.png").similar(0.86))
                wait(5)
            
            for num in range(100):
                type(Key.ESC)
                wait(5)
                if len(findAny(resource.MESSAGE_CONFIRM_BACK_TITLE)) > 0:
                    type(Key.ESC)
                    break