# -*- coding: utf-8 -*-
from sikuli import *
import os
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import UserSettings


DMP_AUTO_HOME = os.environ["DMP_AUTO_HOME"]

mentionUser = UserSettings.mentionUser
AppPath = UserSettings.AppPath
AndAppPath = UserSettings.AndAppPath
NoxDirPath = UserSettings.NoxDirPath
RUN_MODE = UserSettings.RUN_MODE
TARGET_CHANNEL = UserSettings.TARGET_CHANNEL
NOX_INSTANCES = UserSettings.NOX_INSTANCES2

TOKEN = UserSettings.TOKEN
DRIVE_DECK_CODE_JSON_URL = UserSettings.DRIVE_DECK_CODE_JSON_URL
ACCOUNT_INFO_SHEET_ID = UserSettings.ACCOUNT_INFO_SHEET_ID
STATISTICS_SHEET_ID = UserSettings.STATISTICS_SHEET_ID

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
NoxAppPath = os.path.join(NoxDirPath, r"Nox.exe")
NoxMultiPlayerPath = os.path.join(NoxDirPath, r"MultiPlayerManager.exe")
NoxAdbPath = os.path.join(NoxDirPath, r"adb.exe")

