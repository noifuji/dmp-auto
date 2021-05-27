# -*- coding: utf-8 -*-
from sikuli import *
import os
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import UserSettings

DMP_AUTO_HOME = os.environ["DMP_AUTO_HOME"]
SLACK_UPLOAD_URL = 'https://slack.com/api/files.upload'
LIBS_DIR_PATH = os.path.join(DMP_AUTO_HOME , r"libs")
RES_DIR_PATH = os.path.join(DMP_AUTO_HOME , r"resources")
DATA_DIR_PATH = os.path.join(DMP_AUTO_HOME , r"data")
REMOVE_DATA_BAT_PATH = os.path.join(DMP_AUTO_HOME , r"libs\ThirdPartyLib\bat\noxRemovePkgData.bat")
NOX_START_APP_BAT_PATH = os.path.join(DMP_AUTO_HOME , r"libs\ThirdPartyLib\bat\startDMPApp.bat")
NOX_KILL_APP_BAT_PATH = os.path.join(DMP_AUTO_HOME , r"libs\ThirdPartyLib\bat\killDMPApp.bat")
NOX_BACKUP_APP_BAT_PATH = os.path.join(DMP_AUTO_HOME , r"libs\ThirdPartyLib\bat\backupDMPApp.bat")
RESTART_OS_BAT_PATH = os.path.join(DMP_AUTO_HOME , r"libs\ThirdPartyLib\bat\restartOS.bat")
JAVA_API_PATH = os.path.join(DMP_AUTO_HOME , r"libs\ThirdPartyLib/javaapis/build/libs/javaapis-all.jar")
COMPLETED_INSTANCES_JSON_FILE = "CompletedInstance.json"
DECK_CODE_JSON_FILE = "DMPAutoDeckCodes.json"
CREDENTIALS_JSON_FILE = "credentials.json"
BACKUP_DIR_NAME = "20201203"
BACKUP_DIR_PATH = os.path.join(DMP_AUTO_HOME , r"data\identifier")
USER_SETTINGS_SHEET_ID = UserSettings.USER_SETTINGS_SHEET_ID

RESTART_COUNT_LIMIT = 5

#account status
ACCOUNT_INFO_SHEET_NAME = "raw"
ACCOUNT_INFO_REF_COL = "B"
ACCOUNT_INFO_PLAYERID_COL = "C"

ACCOUNT_INFO_START_COL = "D"
ACCOUNT_INFO_END_COL = "V"

ACCOUNT_INFO_START_COL2 = "AR"
ACCOUNT_INFO_END_COL2 = "AR"

ACCOUNT_INFO_CARDCOUNT_START_COL = "W"
ACCOUNT_INFO_CARDCOUNT_END_COL = "AF"

ACCOUNT_INFO_COMPUTERNAME_COL = "AG"
ACCOUNT_INFO_MAIN_COL = "AH"
ACCOUNT_INFO_LEGEND_COL = "AI"
ACCOUNT_INFO_SP_END_COL = "AJ"
ACCOUNT_INFO_CREATEDATE_COL = "AK"
ACCOUNT_INFO_DAILY_COL = "AL"
ACCOUNT_INFO_LOGIN_COL = "AM"

ACCOUNT_INFO_START_ROW = "3"
ACCOUNT_INFO_END_ROW = "1500"

sys.path.append(JAVA_API_PATH)
from spreadsheetapis import SpreadSheetApis

def zip_longer(list1, list2):
    if len(list1) >= len(list2):
        result = []
        for i in range(len(list1)):
            if i > (len(list2) - 1):
                l2 = ""
            else:
                l2 = list2[i]
            result.append((list1[i], l2))
    else:
        result = []
        for i in range(len(list2)):
            if i > (len(list1) - 1):
                l1 = ""
            else:
                l1 = list1[i]
            result.append((l1, list2[i]))
            
    return result



def downloadUserSettings(computername):
    print "downloadUserSettings"
    
    f = open(os.path.join(DATA_DIR_PATH , CREDENTIALS_JSON_FILE))
    strCredentials = f.read()
    f.close()
    spreadsheet = SpreadSheetApis("DMPAuto", strCredentials)
    usersettingsRaw = spreadsheet.read(USER_SETTINGS_SHEET_ID, "UserSettings!A1:Z300", "COLUMNS")
    usersettings = []
    for i in range(len(usersettingsRaw)-1):
        usersettings.append({key: val for key, val in zip_longer(usersettingsRaw[0], usersettingsRaw[i+1])})

    for us in usersettings:
        rawStrInstances = us['NOX_INSTANCES']
        instances = rawStrInstances.split('/')
        if len(instances) == 1 and instances[0] == "":
            us['NOX_INSTANCES'] = []
        else:
            us['NOX_INSTANCES'] = [int(s) for s in instances]
        
        rawStrResetInstances = us['NOX_RESET_INSTANCES']
        resetInstances = rawStrResetInstances.split('/')
        if len(resetInstances) == 1 and resetInstances[0] == "":
            us['NOX_RESET_INSTANCES'] = []
        else:
            us['NOX_RESET_INSTANCES'] = [int(s) for s in resetInstances]

    result = {}
    for us in usersettings:
        if us["COMPUTERNAME"] == computername:
            result = us

    if result == {}:
        raise Exception("No available settings...")
    
    return result

try:
    userSettings = downloadUserSettings(os.environ["COMPUTERNAME"])

    TOKEN = userSettings["TOKEN"]
    TARGET_CHANNEL = userSettings["TARGET_CHANNEL"]
    DRIVE_DECK_CODE_JSON_URL = userSettings["DRIVE_DECK_CODE_JSON_URL"]
    ACCOUNT_INFO_SHEET_ID = userSettings["ACCOUNT_INFO_SHEET_ID"]
    STATISTICS_SHEET_ID = userSettings["STATISTICS_SHEET_ID"]
    mentionUser = userSettings["MENTION_AT"]
    AppPath = userSettings["ANDAPP_DMP_PATH"]
    AndAppPath = userSettings["ANDAPP_PATH"]
    NoxDirPath = userSettings["NOX_BIN_PATH"]
    RUN_MODE = userSettings["RUN_MODE"]
    ENGINE_FOR_MAIN = userSettings["ENGINE_FOR_MAIN"]
    ENGINE_FOR_LEGEND = userSettings["ENGINE_FOR_LEGEND"]
    ENGINE_FOR_SP = userSettings["ENGINE_FOR_SP"]
    IDENTIFIER_DRIVE_DIR_ID = userSettings["IDENTIFIER_DRIVE_DIR_ID"]
    
    
    NOX_INSTANCES = userSettings['NOX_INSTANCES']
    try:
        NOX_RESET_INSTANCES = userSettings['NOX_RESET_INSTANCES']
    except:
        NOX_RESET_INSTANCES = []
        
    
    
    
    NoxAppPath = os.path.join(NoxDirPath, r"Nox.exe")
    NoxMultiPlayerPath = os.path.join(NoxDirPath, r"MultiPlayerManager.exe")
    NoxAdbPath = os.path.join(NoxDirPath, r"adb.exe")
except:
    print "failed to access Sheet"
