#version V1 : y a le local capteur et le distant, on peut tester en local (sans lora), on enregistre sur eeprom un des deux capteurs v2 -> deux capteurs locaux et un distant; v3 -> corrige gros
#bug : il faut faire une pseudo-mesure avant de démarrer, bof, finalement on fait moyenne de 100 mesures, v4-> temperature et label, v5-> deux capteurs dans le distant (poids = somme des deux)
#v6-> on rajoute un capteur local aux deux distants (v5 ne marche plus) puis versions tx_rx_v1: on y met les deux, ainsi que la lecture; version tx_rx_v2 : config 4 capteurs 20kg;
#version tx_rx_v3 : on fait un cycle de mesures sur n points, b fois de suite en envoyant un numéro de trame sauvé sur EEPROM TX (on s'est aperçu qu'on perdait bcp de trames), tx_rx_v_4 : 6 capteurs
#version tx_rx_v_1.py : on passe en python,v_9 commence à marcher avec un capteur sauf HX711 mode degradé; v_10 hx711 semble marcher après exclusion des valeurs 2**n-1;
#v_11 : deux capteurs conf 120



print (' Choisir une config: 1er chiffre 1->config RX, 2->configTX, 3->lecture EEPROM/TX,  2eme chiffre->nb capteurs RX,  3eme chiffre->nb capteurs sur TX')
print (' configuration 101 : RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteur sur le RX; il y a 1 capteur sur le TX')
print (' configuration 106 : RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteur sur le RX; il y a i capteurs sur le TX')
print (' configuration 110 : RX seul, ON VA CONFIGURER LE RX; il y a 1 capteur sur le RX; il y a 0 capteurs sur le TX')
print (' configuration 160 : RX seul, ON VA CONFIGURER LE RX; il y a i capteurs sur le RX; il y a 0 capteurs sur le TX') 
print (' configuration 206 : RX ET TX, ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a i capteurs sur le TX') 
print (' configuration 306 : RX: ON VA LIRE la flash; il y a x capteurs sur le RX; il y a i capteurs sur le TX')

#configuration = input ("entrez un n° de configuration :") #
#configuration=int(configuration)
configuration=106

import pycom
#import os
import errno
from hx711 import HX711
from network import LoRa
import socket 
import time
import config as c
from deepsleep  import *
#from machine import Pin


def miseEnSommeil(sleep): #commande mise en sommeil du LOPY via la carte deepsleep
     ds = DeepSleep()
     ds.go_to_sleep(sleep)  # go to sleep forsleepx seconds
     return

     
def acquisitionCapteur( capteur) :
     capteur.power_up()#reveille le HX711 n°'capteur'
     time.sleep (delai_avant_acquisition)
     lecture_capteur = capteur.read()
     capteur.power_down()# put the ADC in sleep mode
     return lecture_capteur
 
def flashWriteData(numero_trame) : #on écrit numero de trame dans fichier numero trame
     ofi=open('fichier_data', 'a')
     ofi.write(numero_trame)
     ofi.close()
     return

def flashReadData() : #on lit data dans fichier data
     ofi=open('fichier_data', 'r')
     t=ofi.read()
     ofi.close()
     return t

def flashWriteTrame(numero_trame) : #on écrit numero de trame dans fichier numero trame
     ofi=open('fichier_numero_trame', 'w')
     ofi.write(numero_trame)
     ofi.close()
     return

def flashReadTrame() : #on lit un numero de trame dans le fichier numero_trame 
     ofi=open('fichier_numero_trame', 'r')
     t=ofi.read()
     ofi.close()
     return t


def temperatureLopy(GAIN,OFFSET) :
    t=GAIN+OFFSET#***********************************************************fonction bidon
    return t


#Init constantes, selon fichier config.py
tempo_lora_demarrage = c.tempo_lora_demarrage    #le temps que la carte lora soit opérationnelle
tempo_lora_emission = c.tempo_lora_emission           #le temps que la carte lora finisse l'émission
nombre_point=c.nombre_point                                    #c'est le nombre d'acquisitions faites par le HX711, qui en fait une moyenne appelée mesure
b_mesure_par_cycle = c.b_mesure_par_cycle              #on fait "b_mesure_par_cycle"  mesures et on envoie "b_mesure_par_cycle" trames avec le même n° "numero de trame" sur le champ numero_trame
label=c.label                                                                 #controle expéditeur sur label
delimiteur=c.delimiteur                                                #delimiteur entre champs de la trame
numero_trame=c.numero_trame                                  #controle expéditeur sur n° trame
a_max=c.a_max                                                           #affichage port serie a est le nb max de mesures par ligne,
a=c.a                                                                            #affichage port serie a est le nb  de mesures par ligne,
b=c.b                                                                            #b est le nombre total de mesures
delai_avant_acquisition=c.delai_avant_acquisition       #on attend delai avant de lancer les mesures par le HX
delai_local=c.delai_local #on attend delai local avant de lancer une mesure
# Init HX711 module, hx.tare(c.HX_TARE), hx.set_scale(c.HX_SCALE)#cf fichier config capteur_i= HX711(DOUT,SCK)
capteur_0 = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur 10kg
capteur_7 = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur 30kg
capteur_8 = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur 50kg
capteur_1 = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur 20kg_i     
capteur_2 = HX711(c.HX_DT_2, c.HX_SCK_2)     #capteur 20kg_i  
capteur_3 = HX711(c.HX_DT_3, c.HX_SCK_3)     #capteur 20kg_i  
capteur_4 = HX711(c.HX_DT_4, c.HX_SCK_4)     #capteur 20kg_i  
capteur_5 = HX711(c.HX_DT_5, c.HX_SCK_5)     #capteur 20kg_i  
capteur_6 = HX711(c.HX_DT_6, c.HX_SCK_6)     #capteur 20kg_i  

capteurs=[capteur_0, capteur_1, capteur_2,capteur_3,capteur_4,capteur_5,capteur_6,capteur_7, capteur_8 ]

#Init paramètres capteurs
nombre_capteurs=c.nombre_capteurs      #nombre de capteurs sur la balance
tare =c.tare                                               # tare_i : valeur ADC sans rien sur le capteur
valeur =c.valeur                                        # etalonnage _i: valeur ADC avec l'étalon sur le capteur
etalon =c.etalon                                        # etalonnage _i :  poids de l'étalon en grammes
mesure=c.mesure                                     #on corrige la mesure en soustrayant la valeur de la tare
i=0
while i  <=  8:
     mesure[i] = valeur[i] -tare[i]               #  mesure corrigée de la tare ADC, avec l'étalon sur le capteur
     i=i+1



#init deepsleep
sleep=c.sleep


#init temperature********************************************
GAIN_distant=c.GAIN_distant                                          #paramètres de mesure de la température : à régler pour chaque Lopy
OFFSET_distant=c.OFFSET_distant                                  #paramètres de mesure de la température : à régler pour chaque Lopy
GAIN_local=c.GAIN_local                                                 #paramètres de mesure de la température : à régler pour chaque Lopy
OFFSET_local=c.OFFSET_local                                         #paramètres de mesure de la température : à régler pour chaque Lopy


#Init variables locales
temperature_distant=0
temperature_local=0
poids_en_grammes=0
poids_en_gr_distant_total=0
poids_en_gr_local_total=0
lecture_capteur=[0]*9
lecture=0                                                                      #mode sans lecture par défaut, sauf config en 3xx où on force à 1

liste=[0]*24# liste des valeurs HX711 déclarées "fausses"
for i in range (24):
    liste[i]=2**i-1


#DEBUT programme

pycom.heartbeat(False)#arrete clignotement led bleue

if  configuration  in (101, 106, 110, 160, 206, 306):
     print ('ok configuration : ', configuration)


if configuration== 101: # ON VA CONFIGURER LE RX il y a 0 capteurs sur le RX; il y a un capteur d'indice i sur le TX; 
    lora = LoRa(mode=LoRa.LORA, frequency=863000000)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    i=1
    z=0
    while True:   
        z+=1         
        trame_ch=s.recv(128)     
        print(trame_ch,'   ',  z)    
        pycom.rgbled(0x007700)         
        time.sleep(2)         
        if trame_ch: #      trame=label+delimiteur+str(numero_trame)+delimiteur+str(t)+trame+delimiteur+"\n"       
            pycom.rgbled(0x660000)             
            time.sleep(2)         
            trame= trame_ch.decode('utf-8')#sinon pbs compatibilité avec binaire?
            trame=trame.split(delimiteur) #on vire le delimiteur et on met les data dans une liste        
            print(trame)    
            lecture_capteur=0
            poids_en_gr_distant_total=0
            if trame[0] ==label :     #vérification champ 0  pour controle destinataire, et controle champ 1  n° trame pour prendre une seule mesure
                transmission=1 #transmission déclarée OK
                temperature_distant   =(float(trame[2])/2.5-30)
                temperature_local       =temperatureLopy(GAIN_local,OFFSET_local)/2.5-30
                lecture_capteur=float((trame)[3])
                poids_en_gr_distant_total+=(lecture_capteur-tare[i])/mesure[i]*etalon[i]
                numero_trame            =int(trame[1])
                trame_flash=(flashReadTrame())
                print(trame_flash)
                trame_flash=int(flashReadTrame())
                print("poids_en_gr_distant_total", poids_en_gr_distant_total, " Température RX: ", temperature_local, " Température TX: ", temperature_distant, " n° trame: ", numero_trame)
                if numero_trame - trame_flash>1:          #si la différence est supérieure à 1, il y a des trames perdues
                    print (" perte trames: ",  numero_trame - trame_flash)          
                if  numero_trame!=trame_flash and transmission:
                    flashWriteData(trame_ch)     #on sauve la trame sur flash
                    flashWriteTrame ( (trame[1]))#on écrit le nouveau numero de trame
            else:
                print ("erreur transmission")
            time.sleep(1)       
        pycom.rgbled(0x000022)             
        time.sleep(2)     

if configuration== 106: # ON VA CONFIGURER LE RX il y a 0 capteurs sur le RX; il y a i capteurs sur le TX;   trame=  1 [label] + 1 [numero_trame] +1 [T]+24 [6 long]+10 delimiteur
    lora = LoRa(mode=LoRa.LORA, frequency=863000000)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    premier_capteur=1
    while True:   
        trame_ch=s.recv(128)     
        pycom.rgbled(0x002200)             
        time.sleep(2)         
        if trame_ch: #      trame=label+delimiteur+str(numero_trame)+delimiteur+str(t)+trame+delimiteur+"\n"       
            pycom.rgbled(0x660000)            
            time.sleep(2)         
            trame = trame_ch.decode('utf-8')#sinon pbs compatibilité avec binaire?
            trame=trame.split(delimiteur) #on vire le delimiteur et on met les data dans une liste        
            print(trame)    
            lecture_capteur=[0]*9
            poids_en_gr_distant_total=0
            if trame[0] ==label :     #vérification champ 0  pour controle destinataire, et controle champ 1  n° trame pour prendre une seule mesure
                transmission=1 #transmission déclarée bonne           
                temperature_distant   =(float(trame[2])/2.5-30)
                temperature_local       =temperatureLopy(GAIN_local,OFFSET_local)/2.5-30
                for i in range(premier_capteur, nombre_capteurs+premier_capteur)    :                    
                    lecture_capteur[i]=float((trame)[i+2])
                    poids_en_gr=(lecture_capteur[i]-tare[i])/mesure[i]*etalon[i]
                    poids_en_gr_distant_total+=(lecture_capteur[i]-tare[i])/mesure[i]*etalon[i]
                    print(" n° ",i, ': ',  poids_en_gr)
                numero_trame  =int(trame[1])
                trame_flash=int(flashReadTrame())
                print("poids_en_gr_distant_total", poids_en_gr_distant_total, " Température RX: ", temperature_local, " Température TX: ", temperature_distant, " n° trame: ", numero_trame)
                if numero_trame - trame_flash>1:          #si la différence est supérieure à 1, il y a des trames perdues
                    print (" perte trames: ",  numero_trame - trame_flash)          
                if  numero_trame!=trame_flash and transmission:
                    flashWriteData(trame_ch)     #on sauve la trame sur flash
                    flashWriteTrame ( (trame[1]))#on écrit le nouveau numero de trame
            else:
                print ("erreur transmission")
            time.sleep(1)       
        pycom.rgbled(0x000022)             
        time.sleep(2)       
   

if configuration== 206: # ON VA CONFIGURER LE TX il y a 0 capteur sur le RX; il y a i capteurs sur le TX; trame=label+delimiteur+str(numero_trame)+delimiteur+str(t)+trame+delimiteur+"\n"
    lora = LoRa(mode=LoRa.LORA, frequency=863000000)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    while True:
        pycom.rgbled(0x002200)                  
        time.sleep(2)         
        poids_en_gr_total=b=0
        trame=''
        while b < b_mesure_par_cycle : #on peut faire b mesures pour fiabiliser la mesure et envoyer b mesures par trame
            b+=1
            poids_en_gr=poids_en_gr_total=0
            nombre_capteurs=6
            premier_capteur=1
            for i in range(premier_capteur, nombre_capteurs+1):#on fait la mesure sur les 6 capteur_i de 1 à 6
                capteur=capteurs[i]
                lecture_capteur[i]=j=n= moyenne=0
                while j < nombre_point and n< nombre_point:
                    lecture_capteur[i]=acquisitionCapteur(capteur)  #fait l'acquisition sur le capteur _i 
                    print('capteur n°', i, ' ', lecture_capteur[i], 'poids ',  (lecture_capteur[i]-tare[i])/mesure[i]*etalon[i])
                    moyenne+=lecture_capteur[i]
                    if lecture_capteur[i] in liste:
                         moyenne-=lecture_capteur[i]                     
                         print("liste")
                         j-=1
                         n+=1
                    j+=1
                if n>=nombre_point:                     print ('beaucoup d\'erreurs capteur n°', i)
                if j:                                                 lecture_capteur[i]=moyenne/j
                poids_en_gr=((lecture_capteur[i]-tare[i])/mesure[i]*etalon[i])
                print(" n°", i, "b ", b,  poids_en_gr,"  ", lecture_capteur[i] )
                poids_en_gr_total=poids_en_gr+poids_en_gr_total
                trame+=delimiteur+str(lecture_capteur[i])
        numero_trame= int(flashReadTrame() )#on lit le n° trame sur flash du TX
        t=temperatureLopy(GAIN_distant,OFFSET_distant)#mesure de la température du TX
        trame=label+delimiteur+str(numero_trame)+delimiteur+str(t)+trame+delimiteur+"\n"
        print("poids_en_gr_total", poids_en_gr_total, " Température TX: ", t,  " n° trame: ", numero_trame, '****', trame)
        try:            
            s.send (trame) 
            print (trame)
            pycom.rgbled(0x001100)         
            time.sleep(2)          
            pycom.rgbled(0x110000)         
            time.sleep(tempo_lora_emission)               
            print(b)
            b=b+1 
        except Exception as e:
            if e.errno == errno.EAGAIN:
                print('cannot send just yet, waiting...  ', b)           
                pycom.rgbled(0x000011)         
                time.sleep(0.5)
        flashWriteTrame (str( numero_trame+1))    #on ecrit le numero de la prochaine trame sur la flash du TX
        flashWriteData(trame)
        miseEnSommeil(sleep) #eteint Lopy  



if configuration ==  110 : # RX seul ON VA CONFIGURER LE RX il y a un capteur sur le RX; il y a zero capteur sur le TX;trame=timestamp+delimiteur+str(numero_trame)+delimiteur+str(t)+trame+delimiteur+"\n"       
    numero_trame=0

    while True:
        poids_en_gr_total=0
        b=0
        while b < b_mesure_par_cycle : #on peut faire b mesures pour fiabiliser la mesure
             b+=1
             poids_en_gr=poids_en_gr_total=0
             i =6#on fait la mesure sur le capteur_i 
             capteur=capteurs[i]
             lecture_capteur[i]=0
             moyenne=0
             j=0                 
             n=0
             while j < nombre_point and n< nombre_point:
                 lecture_capteur[i]=acquisitionCapteur(capteur)  #fait l'acquisition sur le capteur _i 
                 print('capteur n°', i, ' ', lecture_capteur[i], 'poids ',  (lecture_capteur[i]-tare[i])/mesure[i]*etalon[i])
                 moyenne+=lecture_capteur[i]
                 if lecture_capteur[i] in liste:
                     moyenne-=lecture_capteur[i]                     
                     print("liste")
                     j-=1
                     n+=1
                 j+=1
             if n>=nombre_point:
                 print ('beaucoup d\'erreurs capteur n°', i)
             if j :
                 lecture_capteur[i]=moyenne/j
             poids_en_gr=((lecture_capteur[i]-tare[i])/mesure[i]*etalon[i])
             print(" n°", i, poids_en_gr,"  ", lecture_capteur[i] )
             poids_en_gr_total=poids_en_gr+poids_en_gr_total
        lecture_capteur[i]=str(lecture_capteur[i])  
        b=0
        trame=delimiteur+lecture_capteur[i]
        numero_trame+=1 
        t=temperatureLopy(GAIN_local,OFFSET_local)#mesure de la température du TX***************************************************************************    
        print("poids_en_gr_total", poids_en_gr_total, " Température RX: ", t,  " n° trame: ", numero_trame)
        timest = time.localtime()#on met un timestamp sur la trame
        timest=str(timest)   
        trame=timest+delimiteur+str(numero_trame)+delimiteur+str(t)+trame+delimiteur+"\n"
        flashWriteData(trame)
        print(trame)
    time.sleep(delai_local)


if configuration ==  160 : # RX seul ON VA CONFIGURER LE RX il y a i capteurs sur le RX; il y a zero capteur sur le TX;trame=timestamp+delimiteur+str(numero_trame)+delimiteur+str(t)+6*trames+delimiteur+"\n"       
    numero_trame=0
    while True:
        poids_en_gr_total=b=0
        trame=''
        while b < b_mesure_par_cycle : #on peut faire b mesures pour fiabiliser la mesure et envoyer b trames
            b+=1
            poids_en_gr=poids_en_gr_total=0
            nombre_capteurs=6
            premier_capteur=1
            for i in range(premier_capteur, nombre_capteurs+1):#on fait la mesure sur les 6 capteur_i de 1 à 6
                capteur=capteurs[i]
                lecture_capteur[i]=0
                j=n= moyenne=0
                while j < nombre_point and n< nombre_point:
                    lecture_capteur[i]=acquisitionCapteur(capteur)  #fait l'acquisition sur le capteur _i 
                    print('capteur n°', i, ' ', lecture_capteur[i], 'poids ',  (lecture_capteur[i]-tare[i])/mesure[i]*etalon[i])
                    moyenne+=lecture_capteur[i]
                    if lecture_capteur[i] in liste:
                         moyenne-=lecture_capteur[i]                     
                         print("liste")
                         j-=1
                         n+=1
                    j+=1
                if n>=nombre_point:                     print ('beaucoup d\'erreurs capteur n°', i)
                if j:                                                 lecture_capteur[i]=moyenne/j
                poids_en_gr=((lecture_capteur[i]-tare[i])/mesure[i]*etalon[i])
                print(" n°", i, "b ", b,  poids_en_gr,"  ", lecture_capteur[i] )
                poids_en_gr_total=poids_en_gr+poids_en_gr_total
                trame+=delimiteur+str(lecture_capteur[i])
                i +=1
        numero_trame+=1 
        t=temperatureLopy(GAIN_local,OFFSET_local)#mesure de la température du TX***************************************************************************    
        timest = time.localtime()#on met un timestamp sur la trame
        trame=str(timest)+delimiteur+str(numero_trame)+delimiteur+str(t)+trame+delimiteur+"\n"
        flashWriteData(trame)
        print("poids_en_gr_total", poids_en_gr_total, " Température RX: ", t,  " n° trame: ", numero_trame, '****', trame)
    time.sleep(delai_local)



if  configuration == 306 : # RX: ON VA LIRE la carte flash; il y a 0 capteur sur le RX il y a six capteurs sur le TX;
    lecture=lecture+1#mode lecture
    time.sleep (5)
    if lecture==1 :
         d=flashReadData ()
         print (d)

print('FIN')
