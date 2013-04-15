#/usr/bin/env python
import time
import serial
import logging
log = logging.getLogger(__name__)

class kit1104(object):
    """ Python Class interface to usb-CANAKIT.COM_CANA_KIT_UK1104-if00 micro controller.
        THIS CLASS CURRENTLY ONLY INTERACTS WITH THE RELAY PORTION OF MICROCONTROLLER
        FUNCTIONS.
        
        There is a sensor module on this board and I want to addendum this class later
        for read support for those sensors.
        
        SUPPORTED KIT OPERATIONS.
        RELx.ON
        RELx.OFF
        RELx.TOGGLE
        RELx.GET
        
        RELS.ON
        RELS.OFF
        - Jon Kelley
    """
    def __init__(self,SERIAL_PORT):
        """ Sets up our serial device and creates non-blocking read on device file descriptor.
            Usually SERIAL_PORT should be /dev/serial/by-id/usb-CANAKIT.COM_CANA_KIT_UK1104-if00 
            Only cause in debian and redhat that /dev entry exists, but I don't know which
            kernel version this practice became mainstream on. And they'll probably change it later.
        """
        try:
            self.ser = serial.Serial(
                port=SERIAL_PORT,
                baudrate=115200,
                parity=serial.PARITY_ODD,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0.01 # i have no clue what im doing #http://stackoverflow.com/questions/5373668/problem-reading-data-from-serial-port-in-python
                )
            log.debug('Initialized port=' + str(SERIAL_PORT) + ",baudrate=115200,parity=ODD,stopbits=ONE,bytesize=8,timeout=0.01")
        except serial.serialutil.SerialException,e :
            raise EnvironmentError("Canakit1104 Exception: " + str(e))
        self.ser.open()
        self.ser.write('\r\n') # CRLF wake up microcontroller
    def _index_containing_substring(self,the_list, substring):
        """ This returns the index value of a list element or tuple that matches a substring. """
        for i, s in enumerate(the_list):
            if substring in s:
                return i
        return -1
    def _delayedwrite(self,data,delay=0.3):
        """ Will write anything to the serial line with a delay.
            0.001 is stable on the serial bus, but I'm afraid of abusing the relays.
         """
        if delay < 0.2:
            raise ValueError("Canakit1104 RateLimit: May damage relays. Limit capped at <= 0.01")
        time.sleep(delay)
        self.ser.write(data)
    def setrelay(self,relay,relvalue):
        """ This sets <relay> events to control them on the microcontroller.
            args: relay [ 1 - 4 ]
                          1 = relay 1
                          2 = relay 2
                          3 = relay 3
                          4 = relay 4
            args: relvalue [ 0 - 2 ]
                             0 = off
                             1 = on
                             2 = toggle """
        relay       = str(relay)
        relvalue    = str(relvalue)
        if int(relay) > 0 and int(relay) <= 4:
            if int(relvalue) == 0:
                self._delayedwrite('REL'+relay+'.OFF\r\n')
            elif int(relvalue) == 1:
                self._delayedwrite('REL'+relay+'.ON\r\n')
            elif int(relvalue) == 2:
                self._delayedwrite('REL'+relay+'.TOGGLE\r\n')
            else: raise ValueError("Invalid relay state (no states exceed value of 2). Read this classes docs.")
        else:
            raise ValueError("Invalid relay. (Max relay value of 4) Read this classes docs.")
    def setallrelays(self,relvalue):
        """ Sets all relays on board to <relvalue>.
            args: relvalue [ 0 - 1 ]
                             0 = off
                             1 = on """
        relvalue    = str(relvalue)
        relays = [ 1,2,3,4 ]
        for relay in relays:
            if int(relvalue) == 0:  self._delayedwrite('RELS.OFF\r\n')
            elif int(relvalue) == 1: self._delayedwrite('RELS.ON\r\n')
            else: raise ValueError("Invalid relay. (Max relay value of 4) Read this classes docs.")

    def getrelay(self,relay):
        """ Returns <relay> state as integer. """
        relay   = str(relay)
        self._delayedwrite('REL'+relay+'.GET\r\n') # Acquire relay state.
        recentlist = self.ser.readlines() # A list containing recent inputs and outputs on serialstream.
        reference_index_pointer = self._index_containing_substring(recentlist,'REL'+relay+'.GET\r\n')
        indexpointer = 1 + reference_index_pointer
        return int(recentlist[indexpointer])
    def bye(self):
        """ Please properly release your serial connection, don't complain to me if you have issues """
        self.ser.close()
