import pycom
from network import LoRa
import socket
import time
import math

lora = LoRa(mode=LoRa.LORA, frequency=863000000)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

#while True:
#   if s.recv(64) == b'Ping':
#        s.send('Pong')
#    time.sleep(5)
pycom.heartbeat(False)
pycom.rgbled(0xaa5500)
print("jaune")    
time.sleep(2)
while True:
    trame=s.recv(128)
    if trame :
        pycom.rgbled(0xff0000)
        trame = trame.decode('utf-8')
        print('paquet recu      ', trame)
        trame=trame.split('ping')
        for i in trame:
            print(i)
        time.sleep(0.2)
    
        print("attente paquet")  
        led=0
        for i in range(0, 10, 1):
            led=led+i
            time.sleep(0.1)
            pycom.rgbled(led)
        for i in range(0, 10, 1):
            led=led+i
            time.sleep(0.1)
            pycom.rgbled(led*16*16)
        for i in range(0, 10, 1):
            led=led+i
            time.sleep(0.1)
            pycom.rgbled(led*16**4)    
    trame=s.recv(128)
        
