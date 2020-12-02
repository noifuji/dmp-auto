import sys
import traceback
import random
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import NoxDMLib
import CommonDMLib
import NoxResources

####################Settings####################
instances = EnvSettings.NOX_INSTANCES
####################Settings####################

mentionUser = EnvSettings.mentionUser
appname = 'LOGIN'
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
mode = EnvSettings.RUN_MODE

#Pre-processing Start        
App(EnvSettings.AppPath).close()
App(EnvSettings.AndAppPath).close()

if CommonDMLib.isNewVersionAvailable():
    exit(50)
#Pre-processing End

instanceIndex = 0
retryCount = 0
while instanceIndex < len(instances):
    try:
        CommonDMLib.RestartNox(NoxResources, instances[instanceIndex])
        CommonDMLib.backupDMPdata(NoxResources, EnvSettings.BACKUP_DIRECTORY, instances[instanceIndex])
        CommonDMLib.rotateBackupDirs(EnvSettings.BACKUP_DIRECTORY)
        
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Instance ' + str(instances[instanceIndex]) + 'was completed.', appname)
        instanceIndex += 1
    except:
        Settings.MoveMouseDelay = 0.1
        e = sys.exc_info()
        for mes in e:
            print(mes)
        CommonDMLib.sendMessagetoSlack(mentionUser, 'Error occured in ' + str(instances[instanceIndex]) + '. This instance was skipped.', appname)
        CommonDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        CommonDMLib.sendMessagetoSlack(mentionUser, "Screenshot" ,appname)
        if retryCount >= 4:
            instanceIndex += 1
            retryCount = 0
        else:
            retryCount += 1