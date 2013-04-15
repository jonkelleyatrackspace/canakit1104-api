import logging
import sys

from party import Config    # Gives us classes.party.Config.location, so we can centrally control config location.
from party import AnsiColor # Lets us decorate with ANSI colors.
import ConfigParser                 # Allows us to parse config.
config = ConfigParser.ConfigParser()
try:
    config.read(Config.location) # This is where we use the party config.

    # Set output verbosity for stdout
    stdout_threshold = config.get('Logging', 'threshold_stdout')
    if stdout_threshold.lower() == "debug":
        LOG_LEVEL_CONSOLE    = logging.DEBUG
    elif stdout_threshold.lower() == "info":
        LOG_LEVEL_CONSOLE    = logging.INFO
    elif stdout_threshold.lower() == "warn":
        LOG_LEVEL_CONSOLE    = logging.WARN
    elif stdout_threshold.lower() == "error":
        LOG_LEVEL_CONSOLE    = logging.ERROR
    elif stdout_threshold.lower() == "critical":
        LOG_LEVEL_CONSOLE    = logging.CRITICAL
    elif stdout_threshold.lower() == "fatal":
        LOG_LEVEL_CONSOLE    = logging.FATAL
    else: # WHY DONT YOU WANT LOGGING?????????????????????????
        LOG_LEVEL_FILEHANDLE    = logging.NOTSET

    # Set output verbosity for files
    general_threshold = config.get('Logging', 'threshold_file')
    if general_threshold.lower() == "debug":
        LOG_LEVEL_FILEHANDLE    = logging.DEBUG
    elif general_threshold.lower() == "info":
        LOG_LEVEL_FILEHANDLE    = logging.INFO
    elif general_threshold.lower() == "warn":
        LOG_LEVEL_FILEHANDLE    = logging.WARN
    elif general_threshold.lower() == "error":
        LOG_LEVEL_FILEHANDLE    = logging.ERROR
    elif general_threshold.lower() == "critical":
        LOG_LEVEL_FILEHANDLE    = logging.CRITICAL
    elif general_threshold.lower() == "fatal":
        LOG_LEVEL_FILEHANDLE    = logging.FATAL
    else: # WHY DONT YOU WANT LOGGING?????????????????????????
        LOG_LEVEL_FILEHANDLE    = logging.NOTSET

    # Set app name
    LOG_APPNAME            = config.get('Logging', 'appname')

    # Set output destination
    LOG_FILE                = config.get('Logging', 'filelocation')

    # Less dynamic way of doing things I suppose:
    #LOG_LEVEL_CONSOLE    = logging.INFO
    #LOG_LEVEL_FILEHANDLE = logging.DEBUG
    #LOG_APPNAME          = "moduloapi"
    #LOG_FILE             = sys.path[0] + "/moduloapi.log"
except ConfigParser.NoSectionError:
    print (AnsiColor.GREEN  + "CRITICAL!!!!!!!!!!!")
    print (AnsiColor.YELLOW + "WARNING!!!!!!!!!!!")
    print (AnsiColor.RED    + "FATAL!!!!!!!!!!!")
    print (AnsiColor.BLUE   + "I can't even log this properly, I'm using print()")
    print ("Check config file for " + AnsiColor.RED + "[logging]" + AnsiColor.BLUE + "  section with valid values\nThis applications future stability at this point is uncertain." + AnsiColor.RESET)

class LogClass():
    def __init__(self):
        # Logger.
        self.logger = logging.getLogger(LOG_APPNAME)
        self.logger.setLevel(logging.DEBUG)
        # File handle.
        fh = logging.FileHandler(LOG_FILE)
        fh.setLevel(LOG_LEVEL_FILEHANDLE) # threshold
        # Console handle.
        ch = logging.StreamHandler()
        ch.setLevel(LOG_LEVEL_CONSOLE) # treshold
        # Apply logformat.
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s' )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # Add handdler to logger instance.
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

if __name__ == '__main__':
    """ Pretty much how to use this from a module """
    logclass = LogClass()
    print("You found the secret cow level.")
    logclass.logger.debug('DEBUG.TEST.MESSAGE')
    logclass.logger.info('INFO.TEST.MESSAGE')
    logclass.logger.warn('WARN.TEST.MESSAGE')
    logclass.logger.error('ERROR.TEST.MESSAGE')
    logclass.logger.critical('CRITICAL.TEST.MESSAGE')

