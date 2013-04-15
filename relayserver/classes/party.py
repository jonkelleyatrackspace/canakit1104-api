""" Class party, lots of classes in one here. """
import ConfigParser, os, sys

class Config(object):
    """ Gives you the config file path so blueprints or whatever can use configparser to easily find
    the projects config file. Ideally this could be passed as an optarg parameter to app.py eventually.
    Whatever, this works for now. """
    location = sys.path[0] + "/relayserver.conf"

class AnsiColor(object):
    """ These are ANSI color codes useful for terminal output. """
    RESET = '\033[0m'
    CLEAR = '\033[0m'

    BLACK = '\033[0;30m'
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    PURPLE = '\033[0;35m'
    BROWN = '\033[0;33m'
    GRAY = '\033[0;37m'
    YELLOW = '\033[1;33m'
    WHITE = '\033[1;37m'
    
    LGRAY = '\033[0;37m'
    LBLUE = '\033[1;34m'
    LGREEN = '\033[1;32m'
    LCYAN = '\033[1;36m'
    LRED = '\033[1;31m'
    LPURPLE = '\033[1;35m'
