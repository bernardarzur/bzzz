from machine import Pin
import utime
import time


import struct

def debug_bits(v, s):#boris
    for i in range((s-1),-1,-1):
        print((1 if (v&(1<<i)) else 0), end="")
    print()

def to_value(v):#boris
    f = 0xFF if v[0] & 0x80 else 0
    return struct.unpack(">l", bytearray([f, v[0], v[1], v[2]]))[0]






"""   def read(self):#roberthh https://forum.micropython.org/viewtopic.php?f=16&t=2678&p=23338&hilit=hx711#p21268"""
"""Reading from the board.
        self.power_up()
        while not self.is_ready():
            pass
            print("<waiting finished> pOUT: {}, sckPin: {}".format(self.pOUT.value(), self.pSCK.value()))
            my = 0
            myus = ""
            mydata = ""
            now = utime.ticks_us()        #now = time.ticks_us()
            for i in range(24):
                #data = ""
                now = utime.ticks_us()
                self.pSCK.value(1)
                self.pSCK.value(0)
                data = self.pOUT.value()
                #myus += ", " + str(utime.ticks_diff(utime.ticks_us(), now))
                mydata += str(data)
                my = ( my << 1) | data
            print("bitbanged: ", my)
            #print("us: ", myus)
            print("data: ", mydata)
            for i in range(3):
                self.pSCK.value(1)
                utime.sleep_us(2)
                self.pSCK.value(0)
        self.power_down()
        time.sleep(2)
        return mydata"""

"""def read(self):#source
        dataBits = [self.createBoolList(),
                    self.createBoolList(),
                    self.createBoolList()]

        while not self.is_ready():
            pass

        for j in range(2, -1, -1):
            for i in range(7, -1, -1):
                self.pSCK.value(True)
                #time.sleep(5e-7)
                dataBits[j][i] = self.pOUT()
                #print(self.pOUT())
                #time.sleep(5e-7)
                self.pSCK.value(False)
                #time.sleep(5e-6)
                #print("Itération")
        # set channel and gain factor for next reading
        for i in range(self.GAIN):
            self.pSCK.value(True)
            self.pSCK.value(False)

        # check for all 1
        if self.DEBUG:
            print('{}'.format(dataBits))
        if all(item == 1 for item in dataBits[0]):
            if self.DEBUG:
                print('all true')
            self.allTrue = True
            return self.lastVal
        self.allTrue = False
        readbits = ""
        for j in range(2, -1, -1):
            if dataBits[j][7] == 0: #positif
                for i in range(6, -1, -1):
                    if dataBits[j][i] == 1:
                        readbits = readbits + '1'
                    else:
                        readbits = readbits + '0'
                self.lastVal = int(readbits, 2)
            elif dataBits[j][7] == 1: #négatif: complément à 2
                for i in range(6, -1, -1):
                    if dataBits[j][i] == 0:
                        readbits = readbits + '1'
                    else:
                        readbits = readbits + '0'
                self.lastVal = int(readbits, 2) + 1


        return self.lastVal"""

class HX711:
    def __init__(self, dout, pd_sck, gain=128, debug=False):
        self.pSCK = Pin(pd_sck, mode=Pin.OUT)
        self.pOUT = Pin(dout, mode=Pin.IN, pull=Pin.PULL_DOWN)
   # self.dataPin = Pin(dout, Pin.IN)
    #self.pdsckPin = Pin(pd_sck, Pin.OUT, value=0)
        self.DEBUG = debug
        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1
        self.lastVal = 0
        self.allTrue = False
       # self.set_gain(gain)
        utime.sleep(1)
        self.now = 0
        self.read()

    def read_bit(self):#boris
        self.pSCK.value(True) # pulse clock
        val = 1 if self.pOUT() else 0
        self.pSCK.value(False)
        return val

    def read_byte(self):#boris
        v = 0
        for i in range(8):
            v <<= 1
            v |= self.read_bit()
        return v

    def read_measure(self):#boris
        measure = bytearray(self.read_byte() for _ in range(3))
        # we could do endianess conversion in read_byte, but
        # this is better, it converts to native directly
        return struct.unpack('<i', measure + ('\0' if measure[2] < 128 else '\xff'))

    def set_gain(self):#boris
        # set channel and gain factor for next reading
        for _ in range(self.GAIN):
            self.pSCK.value(True)
            self.pSCK.value(False)
    """
    def set_gain(self, gain):#source
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

        self.pSCK.value(False)
        self.read()
        print('Gain setted to {}'.format(self.GAIN))
    """


    def read(self):#boris
        while not self.is_ready(): time.sleep(1e-6) #1 us

        measure = self.read_measure()
        for v in measure:
            debug_bits(v, 8)
        self.set_gain()

        # self.last = to_value(measure)
        self.last=  measure
        return self.last


    def createBoolList(size=8):
        ret = []
        for i in range(8):
            ret.append(False)
        return ret

    def is_ready(self):
        return self.pOUT() == 0



    def read_average(self, times=3):
        sum = 0
        effectiveTimes = 0
        readed = 0
        for i in range(times):
            readed = self.read()

            if self.allTrue is False:
                sum += readed
                effectiveTimes += 1

        if effectiveTimes == 0:
            return 0
        return sum / effectiveTimes

    def get_value(self, times=3):
        return self.read_average(times) - self.OFFSET

    def get_units(self, times=3):
        return self.get_value(times) / self.SCALE

    def tare(self, times=15):
        sum = self.read_average(times)
        self.set_offset(sum)

    def set_scale(self, scale):
        self.SCALE = scale

    def set_offset(self, offset):
        self.OFFSET = offset

    def power_down(self):
        self.pSCK.value(False)
        self.pSCK.value(True)

    def power_up(self):
        self.pSCK.value(False)
