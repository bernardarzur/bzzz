from machine import Pin
import machine
import utime

class HX711:
    def __init__(self, dout, pd_sck, gain=128, debug=False):
        self.pSCK = Pin(pd_sck, mode=Pin.OUT)
        self.pOUT = Pin(dout, mode=Pin.IN, pull=Pin.PULL_DOWN)# la pin est forcee en pull-down, mais pas de changement de consommation veille

        self.DEBUG = debug
        self.GAIN = 1
        self.OFFSET = 0
        self.SCALE = 1
        self.lastVal = 0
        self.allTrue = False
 #       self.set_gain(gain)

    def createBoolList(size=8):
        ret = []
        for i in range(8):
            ret.append(False)
        return ret

    def is_ready(self):
        return self.pOUT() == 0

    def set_gain(self, gain):
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

        self.pSCK.value(False)
        self.read()
        print('Gain set to {}'.format(self.GAIN))

    def read(self):
        #First wait for data ready, DOUT will be low when ready
        while not self.is_ready():
            pass
        #disable interrupts to avoid problems during reading
        #If SCK goes high longer than 65µs the chip enter power down state.
        #So we must avoid interruots during reading
        interrupt_status = machine.disable_irq()

        dataBits = 0

        for i in range(0, 24):
            self.pSCK.value(True)
            dataBits <<= 1
            utime.sleep_us(1)            #Minimum waiting time
            self.pSCK.value(False)
            bitLu = self.pOUT()
            if bitLu: dataBits += 1
            utime.sleep_us(1)            #Minimum waiting time

        # set channel and gain factor for next reading
        for i in range(self.GAIN):
            self.pSCK.value(True)
            utime.sleep_us(1)            #Minimum waiting time
            self.pSCK.value(False)
            utime.sleep_us(1)            #Minimum waiting time

        #
        machine.enable_irq(interrupt_status)        #Re enable interrupts
        if dataBits >= 8388608:                 #negative value
            dataBits = dataBits - 16777216
        return dataBits
    """
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
        return sum / i

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
    """
    def power_down(self):
        #First force SCK down (but should be already DOWN
        self.pSCK.value(False)
        #Then force SCK up, power down state will occur after 60µs
        self.pSCK.value(True)

    def power_up(self):
        self.pSCK.value(False)
