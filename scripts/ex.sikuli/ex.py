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

def isNumber(str):
    definedChar = "0123456789,"
    for s in str:
        if (s in definedChar) == False:
            return False
    return True

def scanNumberChangeWidthFromRight(targetImage, offsetX, offsetY, width, height):
    WIDTH_A_CHAR = 25
    MARGIN_LEFT = 10
    res = findAny(targetImage)
    num = ""
    if len(res) > 0:
        WIDTH_INIT = width
        WIDTH_CONFIRM = width
        dW = 2
        for num in range(1000):
            reg = Region(res[0].getX()+offsetX, res[0].getY()+offsetY, WIDTH_INIT - dW*num, height)
            reg.highlight(0.1)
            num = OCR.readWord(reg)
            if isNumber(num):
                WIDTH_CONFIRM = len(num) * WIDTH_A_CHAR + MARGIN_LEFT
                break

        for num in range(1000):
            reg = Region(res[0].getX()+offsetX, res[0].getY()+offsetY, WIDTH_CONFIRM - dW*num, height)
            reg.highlight(0.5)
            num = OCR.readWord(reg)
            if isNumber(num):
                    break
    return num
OFFSET_X = 78
OFFSET_Y = 96
WIDTH_INIT = 60
HEIGHT = 27
WIDTH_INIT_LONG = 110
#print scanNumberChangeWidthFromRight(NoxResources.TITLE_PACK5SR, OFFSET_X, OFFSET_Y, WIDTH_INIT, HEIGHT)
#print CommonDMLib.scanNumberChangeWidthFromRight(NoxResources.TITLE_PACK5SR, OFFSET_X, OFFSET_Y, WIDTH_INIT, HEIGHT)
print CommonDMLib.scanAccountInfo(NoxResources)