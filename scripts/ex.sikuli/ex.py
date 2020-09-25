sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import NoxDMLib
import CommonDMLib
import NoxResources
import AndAppResources
import random

mentionUser = EnvSettings.mentionUser
appname = "test"

CommonDMLib.addNewDeckByCode(NoxResources, CommonDMLib.getDeckCode("DECKCODE_STSPELL"))