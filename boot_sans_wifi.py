from network import WLAN
from network import Bluetooth
from machine import UART
import os

uart = UART(0, 115200)
os.dupterm(uart)
wlan = WLAN()
wlan.init(mode=WLAN.STA)
wlan.deinit()
bt = Bluetooth()
bt.deinit()
