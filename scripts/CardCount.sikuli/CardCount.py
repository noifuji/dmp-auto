import sys
import traceback
import copy
sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
import EnvSettings
sys.path.append(EnvSettings.LIBS_DIR_PATH)
sys.path.append(EnvSettings.RES_DIR_PATH)
import DMLib
import CommonDMLib

def sum(list) :
    result = 0
    for l in list:
        result += l
    return result

def compareList(list1, list2) :
    if len(list1) != len(list2):
        return False
    
    for num in range(len(list1)):
        if list1[num] != list2[num]:
            return False
    return True

AppPath = EnvSettings.AppPath
DMApp = App(AppPath)

rarities = [Pattern("1596254755989.png").similar(0.90), Pattern("1596254891002.png").similar(0.90), Pattern("1596254900848.png").similar(0.90), Pattern("1596254909843.png").similar(0.90), Pattern("1596254916984.png").similar(0.90)]
#rarities = [Pattern("1596254900848.png").similar(0.90)]
names = []
cards = []
ref = 0
if len(sys.argv) != 2:
    raise Exception("Please enter a Ref No as an argument.")
else:
    ref = sys.argv[1]
    print "ref : " + str(ref)

for rarity in rarities:
    click("1596254734407.png")
    click("1596255093688.png")
    click(rarity)
    wheel(rarity,Button.WHEEL_DOWN, 20)
    wait(0.3)
    click("1596254801720.png")
    click("1596254811579.png")
    click("1596254821274.png")
    click("1596254831781.png")
    click("1598257201695.png")
    click("1596254863404.png")
    wait(0.5)
    
    targets = [Pattern("1596247575934.png").similar(0.95),Pattern("1596247921625.png").similar(0.95),Pattern("1596247936027.png").similar(0.95),Pattern("1596247948331.png").similar(0.95)]
    
    count = [0,0,0,0]
    prevCount = [0,0,0,0]
    confirmedCount = [0,0,0,0]
    wheelCount = 0

    if exists(Pattern("1596258239962.png").similar(0.90), 0.5) == None:
        num = 0
        for target in targets :
            region_of_DMApp = DMApp.window()
            f = Finder(SCREEN.capture(region_of_DMApp))
            f.findAll(target)
            result = []
            while f.hasNext():
               result.append(f.next())
            confirmedCount[num] += len(result)
            num += 1
        names.append(sum(confirmedCount))
        cards.append(confirmedCount[0]*1 + confirmedCount[1]*2 + confirmedCount[2]*3 + confirmedCount[3]*4)
        continue
    
    for loop in range(1000):
        num = 0
        for target in targets :
            region_of_DMApp = DMApp.window()
            region_of_DMApp.setH(region_of_DMApp.getH()*1/2)
            f = Finder(SCREEN.capture(region_of_DMApp))
            f.findAll(target)
            result = []
            while f.hasNext():
               result.append(f.next())
            count[num] = len(result)
            num += 1

        confirmedCount[0] += count[0]
        confirmedCount[1] += count[1]
        confirmedCount[2] += count[2]
        confirmedCount[3] += count[3]
        
        prevCount[0] = count[0]
        prevCount[1] = count[1]
        prevCount[2] = count[2]
        prevCount[3] = count[3]
            
        if exists(Pattern("1596257876745.png").similar(0.90),0.5) != None:
            num = 0
            for target in targets :
                region_of_DMApp = DMApp.window()
                region_of_DMApp.setY(region_of_DMApp.getY()+region_of_DMApp.getH()*1/2)
                region_of_DMApp.setH(region_of_DMApp.getH()*1/2)
                f = Finder(SCREEN.capture(region_of_DMApp))
                f.findAll(target)
                result = []
                while f.hasNext():
                   result.append(f.next())
                confirmedCount[num] += len(result)
                num += 1
            break
        
        wheel(Pattern("1596248336058.png").targetOffset(187,137), Button.WHEEL_DOWN, 4)
        wait(0.5)
    names.append(sum(confirmedCount))
    cards.append(confirmedCount[0]*1 + confirmedCount[1]*2 + confirmedCount[2]*3 + confirmedCount[3]*4)

CommonDMLib.updateCardCount(ref, names, cards)

print " C:" + str(names[0]) + "Card Names / " + str(cards[0]) + "Cards"
print "UC:" + str(names[1]) + "Card Names / " + str(cards[1]) + "Cards"
print " R:" + str(names[2]) + "Card Names / " + str(cards[2]) + "Cards"
print "VR:" + str(names[3]) + "Card Names / " + str(cards[3]) + "Cards"
print "SR:" + str(names[4]) + "Card Names / " + str(cards[4]) + "Cards"