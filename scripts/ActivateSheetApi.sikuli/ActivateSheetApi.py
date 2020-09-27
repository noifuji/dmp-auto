sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.JAVA_API_PATH)
from spreadsheetapis import SpreadSheetApis

f = open(os.path.join(EnvSettings.DATA_DIR_PATH , EnvSettings.CREDENTIALS_JSON_FILE))
strCredentials = f.read()
f.close()
spreadsheet = SpreadSheetApis("DMPAuto", strCredentials)

print "success"