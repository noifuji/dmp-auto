sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import CommonDMLib
import NoxResources


ref = input()
CommonDMLib.backupDMPIdentifier(NoxResources, ref)