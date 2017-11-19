from deepsleep import *
import pycom
from network import LoRa
import socket
import time

lora = LoRa(mode=LoRa.LORA, frequency=863000000)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

pycom.heartbeat(False)
pycom.rgbled(0xaa5500)
print("jaune")   

ds = DeepSleep()
ds.go_to_sleep(3)  # go to sleep for x seconds

 
time.sleep(2)
ping=('ping'+str(2**24))*10
while True:
    s.send(ping)
    pycom.rgbled(0xff0000)
    print("paquet envoyé",  ping)
    time.sleep(.2)
    pycom.rgbled(0x000000)         
    time.sleep(4)
    
    
    
    

