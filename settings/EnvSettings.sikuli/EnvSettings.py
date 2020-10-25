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
REMOVE_DATA_BAT_PATH = os.path.join(DMP_AUTO_HOME , r"libs\ThirdPartyLib\noxRemoveDMData\noxRemovePkgData.bat")
NOX_START_APP_BAT_PATH = os.path.join(DMP_AUTO_HOME , r"libs\ThirdPartyLib\noxRemoveDMData\startDMPApp.bat")
NOX_KILL_APP_BAT_PATH = os.path.join(DMP_AUTO_HOME , r"libs\ThirdPartyLib\noxRemoveDMData\killDMPApp.bat")
JAVA_API_PATH = os.path.join(DMP_AUTO_HOME , r"libs\ThirdPartyLib/javaapis/build/libs/javaapis-all.jar")
COMPLETED_INSTANCES_JSON_FILE = "CompletedInstance.json"
DECK_CODE_JSON_FILE = "DMPAutoDeckCodes.json"
CREDENTIALS_JSON_FILE = "credentials.json"

#account status
ACCOUNT_INFO_SHEET_NAME = "raw"
ACCOUNT_INFO_REF_COL = "B"
ACCOUNT_INFO_PLAYERID_COL = "C"
ACCOUNT_INFO_START_COL = "D"
ACCOUNT_INFO_END_COL = "Q"
ACCOUNT_INFO_CARDCOUNT_START_COL = "R"
ACCOUNT_INFO_CARDCOUNT_END_COL = "AA"
ACCOUNT_INFO_COMPUTERNAME_COL = "AB"
ACCOUNT_INFO_MAIN_COL = "AC"
ACCOUNT_INFO_LEGEND_COL = "AD"
ACCOUNT_INFO_SP_END_COL = "AE"
ACCOUNT_INFO_START_ROW = "3"
ACCOUNT_INFO_END_ROW = "300"

sys.path.append(JAVA_API_PATH)
from spreadsheetapis import SpreadSheetApis

def downloadUserSettings(computername):
    print "downloadUserSettings"
    
    f = open(os.path.join(DATA_DIR_PATH , CREDENTIALS_JSON_FILE))
    strCredentials = f.read()
    f.close()
    spreadsheet = SpreadSheetApis("DMPAuto", strCredentials)
    usersettingsRaw = spreadsheet.read(UserSettings.USER_SETTINGS_SHEET_ID, "UserSettings!A1:Z300", "COLUMNS")
    usersettings = []
    for i in range(len(usersettingsRaw)-1):
        if len(usersettingsRaw[0]) != len(usersettingsRaw[i+1]):
            print "Usersettings must have all attributes."
            continue
        usersettings.append({key: val for key, val in zip(usersettingsRaw[0], usersettingsRaw[i+1])})

    for us in usersettings:
        rawStrInstances = us['NOX_INSTANCES']
        instances = rawStrInstances.split('/')
        us['NOX_INSTANCES'] = [int(s) for s in instances]
        
        rawStrResetInstances = us['NOX_RESET_INSTANCES']
        resetInstances = rawStrResetInstances.split('/')
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
