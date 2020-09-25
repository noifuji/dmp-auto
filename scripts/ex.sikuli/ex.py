sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import NoxDMLib
import CommonDMLib
import NoxResources
import random

for num in range(5):
    if len(findAny(Pattern("1600991582416.png").similar(0.90))) > 0:
        if len(findAny("1600992206988.png")) > 0:
            click("1600992218014.png")
            exists("1600991713407.png",60)
            if len(findAny(Pattern("1600991811657.png").similar(0.90))) > 0:
                CommonDMLib.sendMessagetoSlack(mentionUser, 'All stories are cleared!', appname)
                entire_loop_flag = False
                break
            click("1600991856403.png")