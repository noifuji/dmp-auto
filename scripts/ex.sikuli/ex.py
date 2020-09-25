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

CommonDMLib.updateCardCount(1077, [1,2,3,4,5], [10,20,30,40,50])