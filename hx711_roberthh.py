#write your program:
# -*- coding: utf-8 -*-
"""An implementation of the HX711 board reading load cell(s)."""

import utime
#import ustruct as struct # pylint: disable=import-error
from machine import Pin # pylint: disable=import-error
from machine import freq
freq(160000000)

class HX711:
    """ Reading from a HX711 board by s simple serial protocol."""

def __init__(self, pd_sck, dout, gain):
    self.gain = gain #unused, todo: 128 = 3 times sck high->low
    self.dataPin = Pin(dout, Pin.IN)
    self.pdsckPin = Pin(pd_sck, Pin.OUT, value=0)
    self.pdsckPin.value(0)


def isready(self):
    """When output data is not ready for retrieval,    digital output pin DOUT is high.    """
    #print("<waiting> dataPin: {}, sckPin: {}".format(self.dataPin.value(), self.pdsckPin.value()))
    return self.dataPin.value() == 0

def read(self):
    """Reading from the board."""
    self.powerUp()
    while not self.isready():
        pass
        print("<waiting finished> dataPin: {}, sckPin: {}".format(self.dataPin.value(), self.pdsckPin.value()))
        my = 0
        myus = ""
        mydata = ""
        now = utime.ticks_us()        #now = time.ticks_us()
        for i in range(24):
            #data = ""
            now = utime.ticks_us()
            self.pdsckPin.value(1)
            self.pdsckPin.value(0)
            data = self.dataPin.value()
            myus += ", " + str(utime.ticks_diff(utime.ticks_us(), now))
            mydata += str(data)
            my = ( my << 1) | data
            print("bitbanged: ", my)
            print("us: ", myus)
            print("data: ", mydata)        
        for i in range(3):
            self.pdsckPin.value(1)
            utime.sleep_us(2)
            self.pdsckPin.value(0)    
    self.powerDown()

def powerDown(self):
    """Power the HX711 down as per datasheet: Setting high longer than 60 microseconds.    """
    self.pdsckPin.value(0)
    self.pdsckPin.value(1)
    utime.sleep_us(80)

def powerUp(self):
    self.pdsckPin.value(0)
