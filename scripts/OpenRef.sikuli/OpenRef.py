sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import CommonDMLib
import NoxResources
from driveapis import DriveApis
from spreadsheetapis import SpreadSheetApis

sheets = SpreadSheetApis("DMPAuto", CommonDMLib.getCredentials())
drive = DriveApis("DMPAuto", CommonDMLib.getCredentials())
ref = input()

rawData = sheets.read(EnvSettings.ACCOUNT_INFO_SHEET_ID, "status!A2:F3000", "ROWS")
rawData = rawData if not rawData == None else []
availableRefs = []
for raw in rawData:
    if raw[0] == ref and raw[1] == "sold":
        print "This ref was already sold. Don't open."
        exit()

if not CommonDMLib.isNoxOn():
    print "restarting Nox..."
    CommonDMLib.RestartNox(NoxResources, "MAIN")
CommonDMLib.loadRef(NoxResources, ref, drive)
CommonDMLib.RestartApp(NoxResources)