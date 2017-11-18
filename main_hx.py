""" OTAA Node example compatible with the LoPy Nano Gateway """

from network import WLAN
import pycom
import time
import config as c
from hx711 import HX711


# Disable wifi or let default SSID
if c.DIS_WIFI:
    wlan = WLAN()
    wlan.deinit()

# Set heartbeat
pycom.heartbeat(c.HEARTBEAT)

time.sleep(5.0)

# Init HX711 module
hx = HX711(c.HX_DT, c.HX_SCK)
hx.set_scale(c.HX_SCALE)
hx.tare(c.HX_TARE)

while True:
    # Read the HX value
    val = hx.get_units(5)
    if c.DEBUG_CON:
        print('hx711.read >> ', val)
    # Sleep
time.sleep(15)
