sys.path.append(os.path.join(os.environ["DMP_AUTO_HOME"] , r"settings"))
DMP_AUTO_HOME = os.environ["DMP_AUTO_HOME"]
RES_DIR_PATH = os.path.join(DMP_AUTO_HOME , r"resources")
sys.path.append(RES_DIR_PATH)
import AndAppResources

def getHandCount(resources):
    print 'getHandInfo'
    f = Finder(SCREEN.capture())
    count = 0
    f.findAll("1619246342106.png")
    while f.hasNext():
       count += 1
       f.next()
    return count


try:
    print "\007"
    from guide import *

    print getHandCount(AndAppResources)

    print "start"
    #f = Finder(SCREEN.capture())
    #f.findAll("1619246342106.png")
    #matches = []
    #while f.hasNext():
    #    matches.append(f.next())
    #    print "matches"
        
    count = 1
    for m in findAll("1619246342106.png", 0.7):
        text(m, str(count))
        print str(count)
        count += 1
    
    
    show()
    wait(5)
    
except SystemExit as e:
    exit(e)
except:
    import traceback
    print traceback.format_exc()
finally:
    print "\007"
    print "\007"