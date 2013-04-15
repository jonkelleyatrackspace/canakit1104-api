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


class poller(Daemon):
    def run(self):
        while True: # Loop consistently.
            logclass.logger.error('SPAM')


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
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
        

