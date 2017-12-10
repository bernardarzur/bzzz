#version V1 : y a le local capteur et le distant, on peut tester en local (sans lora), on enregistre sur eeprom un des deux capteurs v2 -> deux capteurs locaux et un distant; v3 -> corrige gros
#bug : il faut faire une pseudo-mesure avant de démarrer, bof, finalement on fait moyenne de 100 mesures, v4-> temperature et label, v5-> deux capteurs dans le distant (poids = somme des deux)
#v6-> on rajoute un capteur local aux deux distants (v5 ne marche plus) puis versions tx_rx_v1: on y met les deux, ainsi que la lecture; version tx_rx_v2 : config 4 capteurs 20kg;
#version tx_rx_v3 : on fait un cycle de mesures sur n points, b fois de suite en envoyant un numéro de trame sauvé sur EEPROM TX (on s'est aperçu qu'on perdait bcp de trames), tx_rx_v_4 : 6 capteurs
#version tx_rx_v_1.py : on passe en python,v_9 commence à marcher avec un capteur sauf HX711 mode degradé



print (' Choisir une config: 1er chiffre 1->config RX, 2->configTX, 3->lecture EEPROM/TX,  2eme chiffre->nb capteurs RX,  3eme chiffre->nb capteurs sur TX')
print (' configuration 101 : RX et TX, ON VA CONFIGURER LE RX; il y a 0 capteur sur le RX; il y a 0 capteurs sur le TX')
print (' configuration 106 : RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteur sur le RX; il y a 6 capteurs sur le TX')
print (' configuration 110 : RX seul, ON VA CONFIGURER LE RX; il y a 1 capteur sur le RX; il y a 0 capteurs sur le TX')
print (' configuration 130 : RX seul, ON VA CONFIGURER LE RX; il y a 3 capteurs sur le RX; il y a 0 capteurs sur le TX') 
print (' configuration 201 : RX ET TX, ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a 1 capteurs sur le TX') 
print (' configuration 206 : RX ET TX, ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a 6 capteurs sur le TX') 
print (' configuration 306 : RX: ON VA LIRE carte SD; il y a 0 capteur sur le RX; il y a 6 capteurs sur le TX')

#configuration = input ("entrez un n° de configuration :") #
#configuration=int(configuration)
configuration=110

import pycom
import os
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

def acquisitionCapteur20kg(i, tare,mesure,etalon, nombre_point) :##################ne marche pas
     capteur_20kg[i].power_up()#reveille le HX711
     time.sleep (delai_avant_acquisition)
     lecture_capteur = capteur_20kg[i].read_average(nombre_point)
     poids_en_gr=(lecture_capteur-tare)/mesure*etalon
     print("   valeur ADC _", i+1, lecture_capteur," * ", poids_en_gr,"*")
     capteur_20kg[i].power_down()# put the ADC in sleep mode
     return lecture_capteur

def acquisitionCapteur_1( tare,mesure,etalon, nombre_point) :
     capteur_1.power_up()#reveille le HX711 n°1
     time.sleep (delai_avant_acquisition)
     lecture_capteur = capteur_1.read()
     poids_en_gr=(lecture_capteur-tare)/mesure*etalon
     print("   valeur ADC _1 : ", lecture_capteur,"*",  poids_en_gr,"*")
     capteur_1.power_down()# put the ADC in sleep mode
     return lecture_capteur


def acquisitionCapteur_2( tare,mesure,etalon, nombre_point) :
     capteur_2.power_up()#reveille le HX711 n°6
     time.sleep (delai_avant_acquisition)
     lecture_capteur = capteur_2.read_average(nombre_point)
     poids_en_gr=(lecture_capteur-tare)/mesure*etalon
     print("   valeur ADC capteur_2 : ", lecture_capteur,"*",  poids_en_gr,"*")
     capteur_2.power_down()# put the ADC in sleep mode
     return lecture_capteur

def acquisitionCapteur_6( tare,mesure,etalon, nombre_point) :
     capteur_6.power_up()#reveille le HX711 n°6
     time.sleep (delai_avant_acquisition)
     lecture_capteur = capteur_6.read_average(nombre_point)
     poids_en_gr=(lecture_capteur-tare)/mesure*etalon
     print("   valeur ADC capteur_6 : ", lecture_capteur,"*",  poids_en_gr,"*")
     capteur_6.power_down()# put the ADC in sleep mode
     return lecture_capteur

def flashWriteData(numero_trame) : #on écrit numero de trame dans fichier numero trame
     ofi=open('fichier_data', 'a')
     ofi.write(numero_trame)
     ofi.close()
     return

def flashReadData() : #on écrit data dans fichier data
     ofi=open('fichier_data', 'r')
     t=ofi.read()
     ofi.close()
     return t

def flashWriteTrame(numero_trame) : #on écrit numero de trame dans fichier numero trame
     ofi=open('fichier_numero_trame', 'w')
     ofi.write(numero_trame)
     ofi.close()
     return

def flashReadTrame() : #on lit un numero de trame dans le fichier numero_trame dans le fichier
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
# Init HX711 module, hx.tare(c.HX_TARE), hx.set_scale(c.HX_SCALE)
capteur_1 = HX711(c.HX_DT_1, c.HX_SCK_1)     #cf fichier config capteur_20kg_1= HX711('DOUT,SCK)
#capteur_2 = HX711(c.HX_DT_2, c.HX_SCK_2)
#capteur_3 = HX711(c.HX_DT_3, c.HX_SCK_3)
#capteur_4 = HX711(c.HX_DT_4, c.HX_SCK_4)
#capteur_5 = HX711(c.HX_DT_5, c.HX_SCK_5)
#capteur_6 = HX711(c.HX_DT_6, c.HX_SCK_6)

#Init paramètres capteurs
capteur_20kg = ['capteur_20kg_1','capteur_20kg_2', 'capteur_20kg_3', 'capteur_20kg_4', 'capteur_20kg_5', 'capteur_20kg_6' ]
nombre_capteurs=c.nombre_capteurs                          #nombre de capteurs sur la balance
tare_20kg =c.tare_20kg                                                # [-44450,95900,-95950, -95950, -95950, -95950  ]           # tare 20kg_i : valeur ADC sans rien sur le capteur le 04/04/2017
valeur_20kg =c.valeur_20kg                                         #[478650, 613000,408200, 613500, 613500, 613500 ]     # etalonnage 20kg_i: valeur ADC avec l'étalon sur le capteur
etalon_20kg =c.etalon_20kg                                         # 5202                                                                                 # etalonnage 20kg_i :  poids de l'étalon en grammes
mesure_20kg=c.mesure_20kg                                      #on corrige la mesure en enlevant la tare
i=0
while i  <  6:
     mesure_20kg[i] = valeur_20kg[i] -tare_20kg[i]       #  mesure corrigée de la tare ADC, avec l'étalon sur le capteur
     i=i+1
tare_10kg = 279600                                                     #lecture du capteur 10kg_leny sans rien dessus le 23/01/2017
etalon_10kg = 5202                                                      #poids de l'étalon 10kg_leny en grammes
mesure_10kg = 1886000-tare_10kg                             #mesure du poids de l'étalon 10kg_leny en tenant compte de la tare, = lecture - tare
tare_30kg = 1.647569e+07#188850                                                     # tare 30kg: valeur ADC sans rien le 15/04/2017
etalon_30kg = 1550                                                      # etalonnage 30kg: poids de l'étalon en grammes
mesure_30kg = 1.660751e+07-tare_30kg#723000-tare_30kg                               # etalonnage 30kg: valeur ADC avec l'étalon sur la balance moins la tare
tare_50kg = 72500#420000                                                     #lecture du capteur pedale sans rien dessus le 23/01/2017
etalon_50kg = 5202                                                     #poids de l'étalon pedale en grammes
mesure_50kg = 103000-tare_50kg                              #mesure du poids de l'étalon pedale en tenant compte de la tare


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
lecture_capteur=[0, 0, 0, 0, 0, 0,]
lecture=0                                                                      #mode sans lecture par défaut, sauf config en 3xx oùon force à 1

liste=[0]*24# liste des valeurs HX711 déclarées "fausses"
for i in range (24):
    liste[i]=2**i-1


#DEBUT programme

pycom.heartbeat(False)#arrete clignotement led bleue


if  configuration  in (101, 106, 110, 120, 130,  201, 206, 306):
     print ('ok configuration : ', configuration)


if configuration== 101: # ON VA CONFIGURER LE RX il y a 0 capteurs sur le RX; il y a six capteurs 20 kg sur le TX;   PAS TESTE                  la trame reçue fait 37 octets : 1 [label] + 1 [numero_trame] +1 [T]+24 [6 long]+10 delimiteur
     lora = LoRa(mode=LoRa.LORA, frequency=863000000)
     s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
     s.setblocking(False)
     i=0
     while True:   
        i=i+1         
        trame_ch=s.recv(128)     
        print(trame_ch,'   ',  i)    
        time.sleep(2)         
        pycom.rgbled(0x007700)                   
        if trame_ch: #      trame=label+delimiteur+str(numero_trame)+delimiteur+str(t)+trame+delimiteur+"\n"       
            time.sleep(2)         
            pycom.rgbled(0x660000)               
            trame_ch = trame_ch.decode('utf-8')#sinon pbs compatibilité avec binaire?
            trame=trame_ch.split(delimiteur) #on vire le delimiteur et on met les data dans une liste        
            print(trame)    
            lecture_capteur=0
            poids_en_gr_distant_total=0
            if trame[0] ==label :     #vérification champ 0  pour controle destinataire, et controle champ 1  n° trame pour prendre une seule mesure
                transmission=1 #transmission déclarée OK
                temperature_distant   =(float(trame[2])/2.5-30)
                temperature_local       =temperatureLopy(GAIN_local,OFFSET_local)/2.5-30
                lecture_capteur=float((trame)[3])
                poids_en_gr_distant=((lecture_capteur-tare_50kg)/mesure_50kg*etalon_50kg)
                print(" n°  1 ", poids_en_gr_distant)
                numero_trame            =int(trame[1])
                trame_flash=(flashReadTrame())
                print(trame_flash)
                trame_flash=int(flashReadTrame())
                print("poids_en_gr_distant_total", poids_en_gr_distant, " Température RX: ", temperature_local, " Température TX: ", temperature_distant, " n° trame: ", numero_trame)
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
        

if configuration== 201: # ON VA CONFIGURER LE TX il y a 0 capteurs sur le RX; il y a un capteur sur le TX; trame=label+delimiteur+str(numero_trame)+delimiteur+str(t)+trame+delimiteur+"\n"
    lora = LoRa(mode=LoRa.LORA, frequency=863000000)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    b=0     
    while b < b_mesure_par_cycle : #on va envoyer b mesures pour fiabiliser la transmission
        time.sleep(tempo_lora_demarrage)#le temps que la carte LoRa se mette en marche
        trame=delimiteur
        lecture_capteur=acquisitionCapteur_6(tare_50kg, mesure_50kg,   etalon_50kg , nombre_point )  #fait l'acquisition sur le capteur 6 sur une moyenne de nombre_point points
        trame=trame+str(lecture_capteur)
        numero_trame= flashReadTrame() #on lit le n° trame sur flash du TX, attention initialisation fichier flash********************************************************************          
        t=temperatureLopy(GAIN_distant,OFFSET_distant)#mesure de la température du TX***************************************************************************
        trame=label+delimiteur+str(numero_trame)+delimiteur+str(t)+trame+delimiteur+"\n"
        print(trame)
        try:            
            s.send(trame)            
            pycom.rgbled(0x001100)         
            time.sleep(2)          
            pycom.rgbled(0x110000)         
            time.sleep(tempo_lora_emission)               
            b=b+1 
            print(b)
        except Exception as e:
            if e.errno == errno.EAGAIN:
                print('cannot send just yet, waiting...  ', b)           
                pycom.rgbled(0x000011)         
                time.sleep(0.5)
    numero_trame=int(numero_trame)+1
    flashWriteTrame (str( numero_trame))    #on ecrit le numero de la prochaine trame sur la flash du TX
    miseEnSommeil(sleep) #eteint Lopy  



if configuration ==  110 : # RX seul ON VA CONFIGURER LE RX il y a un capteur sur le RX; il y a zero capteur sur le TX;trame=timestamp+delimiteur+str(numero_trame)+delimiteur+str(t)+trame+delimiteur+"\n"       
    numero_trame=0

    while True:
        poids_en_gr_total=0
        b=0
        while b < b_mesure_par_cycle : #on peut faire b mesures pour fiabiliser la mesure
             b+=1
             poids_en_gr=poids_en_gr_total=0
             i =0#on fait la mesure sur le capteur_i (1 ici)
             lecture_capteur[i]=0
             moyenne=0
             j=0
             while j < nombre_point:
                 lecture_capteur[i]=acquisitionCapteur_1( tare_20kg[i ], mesure_20kg [i],  etalon_20kg , nombre_point )  #fait l'acquisition sur le capteur 20 kg_i fois le  nombre_point
                 moyenne+=lecture_capteur[i]
                 if lecture_capteur[i] in liste:
                     moyenne-=lecture_capteur[i]                     
                     print("liste")
                     j-=1
                 j+=1
                 print (moyenne, "   ", j)
             lecture_capteur[i]=moyenne/nombre_point#moyenne
             poids_en_gr=((lecture_capteur[i]-tare_20kg[i])/mesure_20kg[i]*etalon_20kg)
             print(" n°", i+1, poids_en_gr,"  ", lecture_capteur[i] )
             poids_en_gr_total=poids_en_gr+poids_en_gr_total
        lecture_capteur[i]=str(lecture_capteur[i])  # 
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


if  configuration == 206 : # ON VA CONFIGURER LE TX il y a x capteurs sur le RX; il y a six capteurs sur le TX; la trame émise fait 27 octets : 1 [label] + 1 n°trame +1 [T]+24 [6 long]
    lora = LoRa(mode=LoRa.LORA, frequency=863000000)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    b=0
    while b < b_mesure_par_cycle : #on va envoyer b mesures pour fiabiliser la transmission
             b+=1

             time.sleep(tempo_lora_demarrage)#le temps que la carte LoRa se mette en marche

             for i in (0,  nombre_capteurs-1):
                 lecture_capteur[i]=acquisitionCapteur20kg[i](i, tare_20kg[i ], mesure_20kg [i],  etalon_20kg , nombre_point )  #fait l'acquisition sur le capteur 20 kg_i sur une moyenne de nombre_point
                 poids_en_gr_distant=((lecture_capteur[i]-tare_20kg[i])/mesure_20kg[i]*etalon_20kg)
                 print(" n°", i+1, poids_en_gr_distant)
                 poids_en_gr_distant_total=poids_en_gr_distant+poids_en_gr_distant_total
                 lecture_capteur[i]=str(lecture_capteur[i])  # il faut coder lecture_capteur_i  en string pour les passer a LoRa

             numero_trame= flashReadTrame() #on lit le n° trame sur flash du TX
             numero_trame=str(numero_trame)
             t=temperatureLopy(GAIN_distant,OFFSET_distant)#mesure de la température du TX***************************************************************************
             t=str(t)
             trame=delimiteur+label+delimiteur+ lecture_capteur[1]+delimiteur+lecture_capteur[2]+delimiteur+lecture_capteur[3]+delimiteur+lecture_capteur[4]+delimiteur+lecture_capteur(5)+delimiteur+lecture_capteur[6]+delimiteur+t+delimiteur+numero_trame
             s.sent(trame)
             print(trame)
             time.sleep(tempo_lora_emission)
             print (" T°C: ", t," numero_trame: ", numero_trame," b: ", b)
    flashWriteTrame ( int(numero_trame) + 1)#on ecrit le numero de la prochaine trame sur la flash du TX
    b=0
  #  miseEnSommeil(sleep) #eteint Lopy  


if  configuration == 306 : # RX: ON VA LIRE la carte flash; il y a 0 capteur sur le RX il y a six capteurs sur le TX;
    lecture=lecture+1#mode lecture
    time.sleep (5)
    if lecture==1 :
         d=flashReadData ()
         print (d)


if configuration== 106: # ON VA CONFIGURER LE RX il y a 0 capteurs sur le RX; il y a six capteurs 20 kg sur le TX;   PAS TESTE                  la trame reçue fait 37 octets : 1 [label] + 1 [numero_trame] +1 [T]+24 [6 long]+10 delimiteur
     octet_par_trame=37
     lora = LoRa(mode=LoRa.LORA, frequency=863000000)
     s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
     s.setblocking(False)
     if carte_sd==2:
         sd = SD()
         os.mount(sd, '/sd')

     while s.recv(128) == True:
        trame_ch=s.recv(128) #      trame=delimiteur+label+delimiteur+ lecture_capteur_1+delimiteur+lecture_capteur_2+delimiteur+lecture_capteur_3+delimiteur+lecture_capteur_4+delimiteur+lecture_capteur_5+delimiteur+lecture_capteur_6+delimiteur+t+delimiteur+numero_trame+delimiteur
        trame_ch = trame_ch.decode('utf-8')#sinon pbs compatibilité avec binaire?
        trame=trame_ch.split(delimiteur) #on vire le delimiteur et on met les data dans une liste
        lecture_capteur=[]
        poids_en_gr_distant_total=0
        if trame[1] ==label :     #vérification octet premier  pour controle destinataire, et controle n° trame pour prendre une seule mesure
             transmission=1 #transmission déclarée OK
             for i in (0,  nombre_capteurs-1):
                 lecture_capteur[i]=trame[i+3]
                 poids_en_gr_distant=((lecture_capteur[i]-tare_20kg[i])/mesure_20kg[i]*etalon_20kg)
                 print(" n°", i, poids_en_gr_distant)
                 poids_en_gr_distant_total=poids_en_gr_distant_total+poids_en_gr_distant
             numero_trame            =trame[17]#dernier champ : 2*(un label, six capteurs, une temperature)+un champ vide delimiteur
             temperature_distant   =(trame[15]/2.5-30)
             temperature_local       =temperatureLopy(GAIN_local,OFFSET_local)/2.5-30
             print("poids_en_gr_distant_total", poids_en_gr_distant_total, " Température local: ", temperature_local, " Température distant: ", temperature_distant, " n° trame: ", numero_trame)
             if numero_trame - flashReadTrame()>1:          #si la différence est supérieure à 1, il y a des trames perdues
                 print (" perte trames: ",  numero_trame - flashReadTrame())
             if carte_sd==2 and numero_trame - flashReadTrame() :
                 sdWriteData(trame_ch)     #on sauve la trame sur SD
                 flashWriteTrame ( numero_trame)#on écrit le nouveau numero de trame
             else :
                 print ("erreur transmission")


if configuration ==  130 : # RX seul ON VA CONFIGURER LE RX il y a un capteur sur le RX; il y a zero capteur sur le TX, c'est un 110 bis pour l i,nstant
     i=0
     #     if carte_sd:
     #      sd = SD()
     #   os.mount(sd, '/sd')
     for i in range(0, 10):
          # lecture_capteur=acquisitionCapteur_6(tare_30kg, mesure_30kg,   etalon_30kg , nombre_point )  #fait l'acquisition sur le capteur 20 kg_ sur une moyenne de nombre_point
   #      poids_en_gr=(lecture_capteur-tare_30kg)/mesure_30kg*etalon_30kg
      #   t=temperatureLopy(GAIN_local,OFFSET_local)#mesure de la température du RX***************************************************************************
        # print(" capteur_30kg : ",lecture_capteur,"**", poids_en_gr,"  Temperature : ", t)
 #        trame=delimiteur+str(poids_en_gr)+delimiteur+str(lecture_capteur)
          trame=delimiteur
          lecture_capteur=acquisitionCapteur_6(tare_50kg, mesure_50kg,   etalon_50kg , nombre_point )  #fait l'acquisition sur le capteur 20 kg_ sur une moyenne de nombre_point
          poids_en_gr=(lecture_capteur-tare_50kg)/mesure_50kg*etalon_50kg
          t=temperatureLopy(GAIN_local,OFFSET_local)#mesure de la température du RX***************************************************************************
 #         print("\r capteur_50kg : ",lecture_capteur,"**", poids_en_gr,"  Temperature : ", t)
          trame=trame+str(poids_en_gr)+delimiteur+str(lecture_capteur)
          timestr = time.localtime()#on met un timestamp sur la trame
          timestr=str(timestr)
          trame=delimiteur+timestr+trame+delimiteur+"\n"
          i=i+1
          if carte_sd==1:
              flashWriteData(trame)
              print(trame)



if configuration ==  111 : # RX et TX, ON VA CONFIGURER LE RX il y a un capteur sur le RX; il y a un capteur sur le TX

     octet_par_trame=37
     lora = LoRa(mode=LoRa.LORA, frequency=863000000)
     s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
     s.setblocking(False)
     if carte_sd==2:
         sd = SD()
         os.mount(sd, '/sd')

     while s.recv(128) == True:
        trame_ch=s.recv(128) #      trame=delimiteur+label+delimiteur+ lecture_capteur_1+delimiteur+lecture_capteur_2+delimiteur+lecture_capteur_3+delimiteur+lecture_capteur_4+delimiteur+lecture_capteur_5+delimiteur+lecture_capteur_6+delimiteur+t+delimiteur+numero_trame+delimiteur
        trame_ch = trame_ch.decode('utf-8')#sinon pbs compatibilité avec binaire?
        trame=trame_ch.split(delimiteur) #on vire le delimiteur et on met les data dans une liste
        lecture_capteur=0
        poids_en_gr_distant_total=0
        if trame[1] ==label and trame[3] ==flashReadTrame() :     #vérification  premier champ pour controle destinataire, et troisieme champ controle n° trame pour prendre une seule mesure
             transmission=1 #transmission déclarée OK             lecture_capteur=int(trame[5])#cinquieme champ
             poids_en_gr_distant=((lecture_capteur-tare_50kg)/mesure_50kg*etalon_50kg)
             print(" n°", i, poids_en_gr_distant)
             temperature_distant   =int(trame[7])/(2.5-30)
             temperature_local       =temperatureLopy(GAIN_local,OFFSET_local)/2.5-30
             print("poids_en_gr_distant_total", poids_en_gr_distant_total, " Température local: ", temperature_local, " Température distant: ", temperature_distant, " n° trame: ", numero_trame)
             if numero_trame - flashReadTrame()>1:          #si la différence est supérieure à 1, il y a des trames perdues
                 print (" perte trames: ",  numero_trame - flashReadTrame())
             if carte_sd==2 and numero_trame - flashReadTrame() :
                 sdWriteData(trame_ch)     #on sauve la trame sur SD
                 flashWriteTrame ( numero_trame)#on écrit le nouveau numero de trame
             else :
                 print ("erreur transmission")    

if configuration ==  120 : # RX seul ON VA CONFIGURER LE RX il y a deux capteurs sur le RX; il y a zero capteur sur le TX
     i=0                
     print ("erreur transmission")    

     if carte_sd==2:
         sd = SD()
         os.mount(sd, '/sd')
     for i in range (0, 10):
         indice_capteur=5#attention la liste démarre à 0, le capteur _x a un indice x-1
         lecture_capteur[indice_capteur]=acquisitionCapteur20kg_6(tare_20kg[indice_capteur ], mesure_20kg [indice_capteur],  etalon_20kg , nombre_point )  #fait l'acquisition sur le capteur 20 kg_indice_capteur sur une moyenne de nombre_point
         poids_en_gr=((lecture_capteur[indice_capteur]-tare_20kg[indice_capteur])/mesure_20kg[indice_capteur]*etalon_20kg)
         poids_en_gr_local_total=poids_en_gr+poids_en_gr_local_total
         t=temperatureLopy(GAIN_local,OFFSET_local)#mesure de la température du RX***************************************************************************
         print(" n°", indice_capteur+1,"**",lecture_capteur[indice_capteur],"**", poids_en_gr,"poids_en_gr_local_total",poids_en_gr_local_total,"Temperature ", t)
         trame=delimiteur+str(poids_en_gr)
         indice_capteur=1#attention la liste démarre à 0, le capteur _x a un indice x-1
         lecture_capteur[indice_capteur]=acquisitionCapteur20kg_2(tare_20kg[indice_capteur ], mesure_20kg [indice_capteur],  etalon_20kg , nombre_point )  #fait l'acquisition sur le capteur 20 kg_indice_capteur sur une moyenne de nombre_point
         poids_en_gr=((lecture_capteur[indice_capteur]-tare_20kg[indice_capteur])/mesure_20kg[indice_capteur]*etalon_20kg)
         poids_en_gr_local_total=poids_en_gr+poids_en_gr_local_total
         t=temperatureLopy(GAIN_local,OFFSET_local)#mesure de la température du RX***************************************************************************
         print(" n°", indice_capteur+1,"**",lecture_capteur[indice_capteur],"**", poids_en_gr,"poids_en_gr_local_total",poids_en_gr_local_total,"Temperature ", t)
         trame=trame+delimiteur+str(poids_en_gr)
         timestr = time.localtime()#on met un timestamp sur la trame
         timestr=str(timestr)
         trame=delimiteur+timestr+trame+"\n"
         i=i+1
         if carte_sd==1:
             flashWriteData(trame)
             print(trame)
         if carte_sd==2:
             sdWriteData(trame)
             print(trame)        

print('FIN')
