#version V1 : y a le local capteur et le distant, on peut tester en local (sans lora), on enregistre sur eeprom un des deux capteurs v2 -> deux capteurs locaux et un distant; v3 -> corrige gros
#bug : il faut faire une pseudo-mesure avant de démarrer, bof, finalement on fait moyenne de 100 mesures, v4-> temperature et label, v5-> deux capteurs dans le distant (poids = somme des deux)
#v6-> on rajoute un capteur local aux deux distants (v5 ne marche plus) puis versions tx_rx_v1: on y met les deux, ainsi que la lecture; version tx_rx_v2 : config 4 capteurs 20kg;
#version tx_rx_v3 : on fait un cycle de mesures sur n points, b fois de suite en envoyant un numéro de trame sauvé sur EEPROM TX (on s'est aperçu qu'on perdait bcp de trames), tx_rx_v_4 : 6 capteurs
#version tx_rx_v_1.py : on passe en python,v_9 commence à marcher avec un capteur sauf HX711 mode degradé; v_10 hx711 semble marcher après exclusion des valeurs 2**n-1;
#v_11 : deux capteurs conf 120, v_12 : 6 capteurs RX et TX; 
#v_13 : mauvaise précision sur v_12, on va tester la mesure par rapport à la dernière archivée sur flash TX avec un paramètre de précision;
#v_14 : on allege conf 206 ->conf 2, un cycle dure 12 secondes pour pouvoir émettre 20 000 trames avec 2600 mAh *2 (on vise 50000) , on passe au Lopy 4 (suppression du shield deepsleep et donc de deepsleep.py
#v_15 : on rajoute un chien de garde pour éviter les plantages réguliers (tous les 2/3 jours pour TX, un peu mieux pour RX), on passe tous les paramètres à config
#v_16 : on transmet le poids ou bien la valeur brute ADC, selon le choix des capteurs
#v_17 : on passe aux modes lora APB et RAW, (OTAA en test), on modifie hx711, on supprime toute écriture sur flash, on écarte valeur min et valeur max du calcul de la mesure, on mesure Tension batterie
#v_18 : on fait trois mains, un RX, un TX et un RX_TX. Celui-ci est le main_RX
import pycom
import os
from network import LoRa
import socket 
import time
import config as c
from machine import WDT
from machine import RTC
 
def flashWriteData(trame) : #on écrit trame dans fichier data
    ofi=open('fichier_data', 'a')
    dispo=os.getfree('/flash')# vérifie si y a de la place sur flash
    if dispo > 100:
        ofi.write(trame)
    else:
        print ("memoire saturee")
        pycom.rgbled(c.jaune_pale)
        time.sleep(2)
    ofi.close()
    return

pycom.heartbeat(False)
pycom.rgbled(c.violet)                                             # flash violet            
time.sleep (c.delai_flash_mise_en_route)
label=c.label                                                                #controle expéditeur sur label, en mode RAW seulement
delimiteur=c.delimiteur                                               #delimiteur entre champs de la trame
w=c.w                                                                          #champ identification (nom de la ruche, ...)
poids_en_grammes=poids_en_gr_distant_total=numero_trame=0
rtc = RTC()
rtc.init(c.date)                                                             #mise à l'heure du récepteur selon fichier config
pycom.rgbled(c.BLACK)
wdt = WDT(timeout=c.timeout)                                 # enable  watchgdog with a timeout of c.timeout milliseconds    
print ('date: ',   rtc.now(), "récepteur RAW : ",  c.w)
   
#trame enregistrée=label+delimiteur+str(t)+delimiteur+w+{delimiteur+str(lecture_capteur[i])}*nb_capteurs+delimiteur+time_stamp+delimiteur+"\n"        
lora = LoRa(mode=LoRa.LORA, frequency=c.LORA_FREQUENCY)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
t0=time.time()
while True:   
    trame_ch=s.recv(128)              
    if trame_ch:      
        pycom.rgbled(c.rouge_pale)  
        time.sleep(c.delai_local)         
        trame = trame_ch.decode('utf-8')                      #sinon pbs compatibilité avec binaire?
        trame=trame.split(delimiteur)                               #on vire le delimiteur et on met les data dans une liste            
        poids_en_gr_distant_total=0
        i=0
        if trame[0] ==label :                                             #vérification champ 0  pour controle destinataire, mode RAW
            v   =int(trame[1]) #tension_Batterie
            for g in trame:
                if i >=3:
                    if g!='':
                        poids_en_gr_distant_total+=float(g)
                        print ("i ", i-2,"   g ", g, "    poids_en_gr_distant_total ", poids_en_gr_distant_total)
                i+=1          
            t=rtc.now()                                                      #on fait un timestamp, le temps  est initialisé dans la config
            t0=time.time()
            ts=''
            for g in t: 
                ts+=str(g)+delimiteur
            trame_ch+=ts+'\n'                                       #on ajoute le timestamp à la trame reçue
            flashWriteData(trame_ch)                               #on sauve la trame sur flash
            numero_trame+=1
        else:
            print ("erreur transmission")                
        print(trame_ch," poids_total: ", poids_en_gr_distant_total,  " N_T: ", numero_trame)      
    deltaT=time.time()-t0       #si pas de transmission pendant 2 fois le temps de deepsleep, on allume en rouge
    if deltaT> c.sleep*2/1000:
        pycom.rgbled(c.RED)
    else:
        pycom.rgbled(c.BLACK)            
    time.sleep(c.delai_local)  
    print (" ", deltaT, end="")
    wdt.feed() # feeds  watchgdog

print('FIN')
