#qe
import canakit; r = canakit.kit1104('/dev/serial/by-id/usb-CANAKIT.COM_CANA_KIT_UK1104-if00')
from random import randint
import time
class AnsiColor(object):
    """ These are ANSI color codes useful for terminal output. """
    RESET = '\033[0m';      CLEAR = '\033[0m'
    ## YOU'RE A MASTER OF KARATE.
    ## AND FRIENDSHIP.
    ## FOR EVERYONE...
    LGRAY = '\033[0;37m';   LBLUE = '\033[1;34m'
    LGREEN = '\033[1;32m';  LCYAN = '\033[1;36m'
    LRED = '\033[1;31m';    LPURPLE = '\033[1;35m'

    BLACK = '\033[0;30m';   BLUE = '\033[0;34m'
    GREEN = '\033[0;32m';   CYAN = '\033[0;36m'
    RED = '\033[0;31m';     PURPLE = '\033[0;35m'
    BROWN = '\033[0;33m';   GRAY = '\033[0;37m'
    YELLOW = '\033[1;33m';  WHITE = '\033[1;37m'




while(True):
    """ Run tests to test relay state reliablity over serial bus.
    Does a a. getstate()
           b. setstate()
           c. getstate()
           d. then verifies if set value matches secondary recieved value.

    Seems like the class interacts reasonably with the controller with the tweaked rate limiting.
    """
    RELAY=randint(1,4)
    RELAYSTATE=randint(0,1)

    STATE_BEFORE            = r.getrelay(RELAY)
    time_before             = time.time()
    r.setrelay(RELAY,RELAYSTATE)
    relaystate_after        = r.getrelay(RELAY)
    time_after              = time.time()
    timetaken = time_after - time_before
    print "RELAY ->" + str(RELAY)
    print " stateprior: " + str(STATE_BEFORE)
    print " statechange_to: " + str(RELAYSTATE)
    print " stateafter: " + str(relaystate_after)
    print " timetaken: " + str(timetaken)
    if relaystate_after == RELAYSTATE:
        print "  Determination: PASS"
    else:
        print "  Determination: FAILURE!!!!!!!!!!!!!!!"

r.disconnect()















