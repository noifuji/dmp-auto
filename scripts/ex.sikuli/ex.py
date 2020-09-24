sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import NoxDMLib
import CommonDMLib
import NoxResources
import random

CommonDMLib.dragDropAtSpeed(Pattern("1600851664292.png").targetOffset(1,-21), findAny("1600848839083.png")[0], 1)