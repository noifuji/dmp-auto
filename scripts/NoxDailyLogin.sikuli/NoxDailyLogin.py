import sys
import traceback
import random
sys.path.append("NoxDMLib.sikuli")
sys.path.append("EnvSettings.sikuli")
import NoxDMLib
import EnvSettings

####################Settings####################
Avator = Pattern("Avator.png").targetOffset(376,-12)
instances = EnvSettings.NOX_INSTANCES
####################Settings####################

slack_url = EnvSettings.slack_url
mentionUser = EnvSettings.mentionUser
NoxAppPath = EnvSettings.NoxAppPath
NoxApp = App(NoxAppPath)
appname = 'NoxDailyLogin'
Settings.MoveMouseDelay = 0.1
Settings.DelayBeforeDrag = 0.5
mode = EnvSettings.RUN_MODE

for instance in instances:
    try:
        NoxDMLib.RestartNox(instance)
        NoxDMLib.RestartApp()
        click("1598940054059.png")
        wait(3)
        click("1596780592222.png")
        exists("1596780703269.png",60)
        #Delete Decks
        for d in ["1598940153267.png", "1598940248022.png"]:
            if exists(d, 1) != None:
                click(d)
                click("1598940187305.png")
                click("1598940201680.png")
                wait(10)
        #Add new Decks
        for d in [["1598940308442.png",EnvSettings.DECKCODE_RED_BLACK], ["1598940317392.png",EnvSettings.DECKCODE_STSPELL]]:
            if exists(d[0], 1) == None:
                CommonDMLib.addNewDeckByCode(NoxResources, d[1])
                wait(5)
        NoxDMLib.sendMessagetoSlack(mentionUser, 'Instance ' + str(instance[1]) + 'was completed.', appname)
    except:
        Settings.MoveMouseDelay = 0.1
        e = sys.exc_info()
        for mes in e:
            print(mes)
        NoxDMLib.sendMessagetoSlack(mentionUser, 'Error occured in ' + str(instance[1]) + '. This instance was skipped.', appname)
        NoxDMLib.sendMessagetoSlack(mentionUser,traceback.format_exc(), appname)
        NoxDMLib.uploadScreenShotToSlack(mentionUser, "Screenshot" ,appname)