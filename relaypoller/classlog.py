import logging

# ------------------------------------------------------------------------
# If you plan to change these ever, you should probably config it.
LOG_LEVEL_FILEHANDLE = logging.INFO
LOG_APPNAME          = "relaypoller"
LOG_FILE             = "/var/log/relaypoller.log"

class LogClass():
    def __init__(self):
        # Logger.
        self.logger = logging.getLogger(LOG_APPNAME)
        self.logger.setLevel(logging.DEBUG)
        # File handle.
        fh = logging.FileHandler(LOG_FILE)
        fh.setLevel(LOG_LEVEL_FILEHANDLE) # Eveeryyyyything.

        # Apply logformat.
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s - PID: %(process)d  ' )
        fh.setFormatter(formatter)

        # Add handdler to logger instance.
        self.logger.addHandler(fh)


if __name__ == '__main__':
    """ Pretty much how to use this from a module """
    logclass = LogClass()
    print("You found the secret cow level.")
    logclass.logger.debug('DEBUG.TEST.MESSAGE')
    logclass.logger.info('INFO.TEST.MESSAGE')
    logclass.logger.warn('WARN.TEST.MESSAGE')
    logclass.logger.error('ERROR.TEST.MESSAGE')
    logclass.logger.critical('CRITICAL.TEST.MESSAGE')

