#/usr/bin/env python
""" This provides the object relational mappings for the SQLITE relay tracking database. """
import logging
log = logging.getLogger(__name__)

from classes.party import Config
import ConfigParser                     # Allows us to parse config.
config = ConfigParser.ConfigParser()
try:
    config.read(Config.location) # This is where we use the party config.
except:
    log.critical('Could not load configs for relay system.')

import sqlite3, os, datetime
class relayobj(object):
    def __init__(self,file):
        DATABASE_NAME  = file + ".sqlite"
        DATABASE_DIR = config.get('SqliteDatabase', 'dirlocation')
        DATABASE_PATH = DATABASE_DIR + DATABASE_NAME
        if os.path.isfile(DATABASE_PATH):
            log.info('Loading database ' + DATABASE_PATH )
            self.conn = sqlite3.connect(DATABASE_PATH)
            self.c = self.conn.cursor()
        else:
            log.info('Missing database ' + DATABASE_PATH + ' ... inflate blank schema..')
            self.conn = sqlite3.connect(DATABASE_PATH)
            self.c = self.conn.cursor()
            self.c.execute('''CREATE TABLE relay
                 (lastupdated text, relaynum integer, relaystate integer)''')

            dt = str(datetime.datetime.now()) # datetime.datetime.utcnow() if you want global-ness

            newvalue = (dt,'1','0',)
            self.c.execute('INSERT INTO relay VALUES (?,?,?)', newvalue)
            newvalue = (dt,'2','0',)
            self.c.execute('INSERT INTO relay VALUES (?,?,?)', newvalue)
            newvalue = (dt,'3','0',)
            self.c.execute('INSERT INTO relay VALUES (?,?,?)', newvalue)
            newvalue = (dt,'4','0',)
            self.c.execute('INSERT INTO relay VALUES (?,?,?)', newvalue)
            self.conn.commit()
    def _relayexists(self,relay):
        try:
            vars = (relay,)
            self.c.execute('SELECT * FROM relay WHERE relaynum=?', vars)
            if self.c.fetchone():
                return True
            else:
                return False
        except:
            log.critical('Exception while seeing if relay exists... ', exc_info=True)
    def set_relay(self,relay,setting):
        """ Sets relay to a new value. """
        if self._relayexists(relay):
            try:
                vars = (setting,relay,)
                self.c.execute('UPDATE relay SET relaystate=? WHERE relaynum=?', vars)
                                
                dt = str(datetime.datetime.now()) # datetime.datetime.utcnow() if you want global-ness
                vars = (dt,relay,)
                self.c.execute('UPDATE relay SET lastupdated=? WHERE relaynum=?', vars)
                self.conn.commit()
            except:
                log.critical('Exception while updating relay state ', exc_info=True)
        else:
            try:
                dt = str(datetime.datetime.now()) # datetime.datetime.utcnow() if you want global-ness
                newvalue = (dt,relay,setting,)
                self.c.execute('INSERT INTO relay VALUES (?,?,?)', newvalue)
                self.conn.commit()

            except:
                log.critical('Exception while inserting new state ', exc_info=True)
    def get_relayupdated(self,relay):
        """ Gets relay last updated and returns it as a datetime object. """
        try:
            relay = tuple(str(relay))
            self.c.execute('SELECT * FROM relay WHERE relaynum=?', relay)
            row = self.c.fetchone()
            return row[0]
        except:
            log.critical('Exception while retrieving last updated ', exc_info=True)
    def get_relaystate(self,relay):
        """ Gets relays current state (0-2) """
        try:
            relay = tuple(str(relay))
            self.c.execute('SELECT * FROM relay WHERE relaynum=?', relay)
            row = self.c.fetchone()
            return row[2]
        except:
            log.critical('Exception while retrieving relaystate ', exc_info=True)
        
