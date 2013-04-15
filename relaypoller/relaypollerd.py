#!/usr/bin/env python
""" Relay Poller Daemon    Jon Kelley    Python 2.7    4/13/2013
      This program daemonizes and then polls an API project for events, then updates a 
      CanakitR1104 ( Docs,specs,circuit diagrams: http://www.canakit.com/Media/Manuals/UK1104.pdf )

      This is a $50 relay controller board and lets you change 4 relay inputs up to 110vac 5amps

        This little magic thing will:
            1 )  Daemonize like a bat out of HELLLL
            2 )  Run a poll to the api, set the initial API light status.
                 a)  Run a poll to the api based on the interval the API states,
                 phone-home repeatedly at that interval.
                 b)  Update the states on the serial controller and local sqlite db accordingly.

    JSON CONTRACT:
    {"canakit1104": {"light_system_project_name": "nebops", "relay": {"1": {"state": 0}, "3": {"state": 1}, "2": {"state": 1}, "4": {"state": 0}}, "lasteventchange": "n/a"}}

"""
import ConfigParser; config = ConfigParser.ConfigParser()
config.read('relaypoller.conf')

import classlog
logclass = classlog.LogClass()

from DEAMON import Daemon
import canakit
import sys, time
import requestsd0390d4 as requests


DBNAME = config.get("Poller", "project_name")
import relay; dbrelay = relay.relayobj(DBNAME)

def database_relay_state_changed(current_relay,pending_state):
    """ Returns true if the relay,state inputted differs from whats in the sqlite db class."""
    if dbrelay.get_relaystate(current_relay) != pending_state:
        return True
    else:
        return False

def database_setrelay(relay,state):
    """ Sets the relay state in the sqlite db class """
    dbrelay.set_relay(relay,state)


def return_api():
    """ This will return a dictionary of what the API is saying. """
    uri = config.get('Poller', 'project_uri')
    r = requests.get(uri)
    print uri, r.json()
    data = r.json()['canakit1104']
    logclass.logger.debug('API RESPONSE' + str(data))
    return data

def setvaluesandloop():
    data = return_api()
    #refreshinterval=float(data['refreshrate'])  # How often to phone home again..
    refreshinterval=1

    for relay in data['relay']:
        state = data['relay'][relay]['state']
        if database_relay_state_changed(relay,state):
            logclass.logger.info('SQL: Relay ' + str(relay) + ' newvalue ' + str(state))
            database_setrelay(relay,state)
            microcontrol.setrelay(relay,state)
        else:
            logclass.logger.info('SQL: Relay ' + str(relay) + ' value ' + str(state) + ' nochange')
    
    logclass.logger.info('Sleep ' + str(refreshinterval) + ' ...........................')
    time.sleep(refreshinterval)
    setvaluesandloop()

class poller(Daemon):
    def run(self):
        data = return_api() # Retrieve api data as dict
        #refreshinterval=float(data['refreshrate'])  # How often to phone home again..
        refreshinterval=1
        for relay in data['relay']:
            state = data['relay'][relay]['state']
            database_setrelay(relay,state)
            microcontrol.setrelay(relay,state)
        while True: # Loop consistently.
            """ Re-Populate values if they change... forever... """
            setvaluesandloop()


if __name__ == "__main__":
    daemon = poller('/var/run/lock/relayagent.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            microcontrol = canakit.kit1104('/dev/serial/by-id/usb-CANAKIT.COM_CANA_KIT_UK1104-if00')
            print "Starting daemon"
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'startfg' == sys.argv[1]:
            """ Populate initial values """
            microcontrol = canakit.kit1104('/dev/serial/by-id/usb-CANAKIT.COM_CANA_KIT_UK1104-if00')
            data = return_api()
            refreshinterval=1
            for relay in data['relay']:
                state = data['relay'][relay]['state']
                database_setrelay(relay,state)
                microcontrol.setrelay(relay,state)
            while True: # Loop consistently.
                """ Re-Populate values if they change... forever... """
                setvaluesandloop()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
        

