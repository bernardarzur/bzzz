#version V1 : y a le local capteur et le distant, on peut tester en local (sans lora), on enregistre sur eeprom un des deux capteurs v2 -> deux capteurs locaux et un distant; v3 -> corrige gros
#bug : il faut faire une pseudo-mesure avant de démarrer, bof, finalement on fait moyenne de 100 mesures, v4-> temperature et label, v5-> deux capteurs dans le distant (poids = somme des deux)
#v6-> on rajoute un capteur local aux deux distants (v5 ne marche plus) puis versions tx_rx_v1: on y met les deux, ainsi que la lecture; version tx_rx_v2 : config 4 capteurs 20kg; 
#version tx_rx_v3 : on fait un cycle de mesures sur n points, b fois de suite en envoyant un numéro de trame sauvé sur EEPROM TX (on s'est aperçu qu'on perdait bcp de trames), tx_rx_v_4 : 6 capteurs
#version tx_rx_v_1.py : on passe en python

import os
from machine import SD
#from machine import Pin
from hx711 import HX711
from network import LoRa
import socket
import time
import config as c

def miseEnSommeil(): #commande mise en sommeil du LOPY via la carte deepsleep
     pass
     return

def acquisitionCapteur20kg(i, tare,mesure,etalon, nombre_point) :##################ne marche pas
     capteur_20kg[i].power_up()#reveille le HX711
     time.sleep (delai_avant_acquisition)          
     lecture_capteur = capteur_20kg[i].read_average(nombre_point)
     poids_en_gr=(lecture_capteur-tare)/mesure*etalon
     print("   valeur ADC 20kg_", i+1, lecture_capteur," * ", poids_en_gr,"*")
     capteur_20kg[i].power_down()# put the ADC in sleep mode
     return lecture_capteur 

def acquisitionCapteur20kg_1( tare,mesure,etalon, nombre_point) :
     capteur_20kg_1.power_up()#reveille le HX711 n°1
     time.sleep (delai_avant_acquisition)          
     lecture_capteur = capteur_20kg_1.read_average(nombre_point)
     poids_en_gr=(lecture_capteur-tare)/mesure*etalon
     print("   valeur ADC 20kg_1 : ", lecture_capteur,"*",  poids_en_gr,"*")
     capteur_20kg_1.power_down()# put the ADC in sleep mode
     return lecture_capteur 

def acquisitionCapteur20kg_2( tare,mesure,etalon, nombre_point) :
     capteur_20kg_2.power_up()#reveille le HX711 n°2
     time.sleep (delai_avant_acquisition)          
     lecture_capteur = capteur_20kg_2.read_average(nombre_point)
     poids_en_gr=(lecture_capteur-tare)/mesure*etalon
     print("   valeur ADC 20kg_2 : ", lecture_capteur,"*",  poids_en_gr,"*")
     capteur_20kg_2.power_down()# put the ADC in sleep mode
     return lecture_capteur 


def flashWriteTrame(numero_trame) : #on écrit numero de trame dans fichier numero trame 
     ofi=open('fichier_numero_trame', 'w')
     ofi.write(numero_trame)#on écrit numero de trame dans fichier numero trame
     ofi.close()
     return 
     
def flashReadTrame() : #on lit un numero de trame dans le fichier numero_trame dans le fichier 
     ofi=open('fichier_numero_trame', 'r')
     t=ofi.read()#on lit numero de trame dans fichier numero trame
     ofi.close()
     return t
     
def SdWriteData(trame):     
     f = open('/sd/data', 'a')
     f.write(trame)
     f.close()
     return
     
def SdReadData():     
     f = open('/sd/data', 'a')
     t=f.read()
     f.close()
     return t  

def temperatureLopy(GAIN,OFFSET) :
    t=GAIN+OFFSET#***********************************************************
    return t



print (' configuration 110 : RX seul, ON VA CONFIGURER LE RX; il y a 1 capteurs sur le RX; il y a 0 capteurs sur le TX; la trame reçue fait   octets : 2 [label/num trame]+1 [T]+24 [6 long]+10 délimiteurs')
print (' configuration 106 : RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteurs sur le RX; il y a 6 capteurs sur le TX; la trame reçue fait 37 octets : 2 [label/num trame]+1 [T]+24 [6 long]+10 délimiteurs')
print (' configuration 201 : RX ET TX, ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a 1 capteurs sur le TX; la trame émise fait  octets : 2 [label/num trame]+1 [T]+24 [6 long]+10 délimiteurs')
print (' configuration 206 : RX ET TX, ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a 6 capteurs sur le TX; la trame émise fait 37 octets : 2 [label/num trame]+1 [T]+24 [6 long]+10 délimiteurs')
print (' configuration 306 : RX: ON VA LIRE carte SD; il y a 0 capteur sur le RX; il y a 6 capteurs sur le TX;           la trame SD fait    37 octets ')

configuration = input ("entrez un n° de configuration :") # Choisir une config: 1er chiffre 1->config RX, 2->configTX, 3->lecture EEPROM/TX,  2eme chiffre->nb capteurs RX,  3eme chiffre->nb capteurs sur TX
configuration=int(configuration)
carte_sd=input("sauvegarde sur carte SD : ENTRER 1 pour oui ou 0 pour non    ") #1 si on veut sauvegarder sur SD du RX, 0 sinon
carte_sd=int(carte_sd)

tempo_lora_demarrage = c.tempo_lora_demarrage    #le temps que la carte lora soit opérationnelle
tempo_lora_emission = c.tempo_lora_emission           #le temps que la carte lora finisse l'émission
nombre_point=c.nombre_point                                    #c'est le nombre d'acquisitions faites par le HX711, qui en fait une moyenne appelée mesure
b_mesure_par_cycle = c.b_mesure_par_cycle              #on fait "b_mesure_par_cycle"  mesures et on envoie "b_mesure_par_cycle" trames avec le même n° "numero de trame" sur le champ numero_trame
label=c.label                                                                 #controle expéditeur sur label
delimiteur=c.delimiteur                                                #delimiteur entre champs de la trame
numero_trame=c.numero_trame                                  #controle expéditeur sur n° trame
lecture=0                                                                      #mode sans lecture par défaut, sauf config en 3xx oùon force à 1
a_max=c.a_max                                                           #affichage port serie a est le nb max de mesures par ligne, 
a=c.a                                                                            #affichage port serie a est le nb  de mesures par ligne, 
b=c.b                                                                            #b est le nombre total de mesures
# Init HX711 module, hx.tare(c.HX_TARE), hx.set_scale(c.HX_SCALE)
capteur_20kg_1 = HX711(c.HX_DT_1, c.HX_SCK_1)     #cf fichier config capteur_20kg_1= HX711('P21', 'P22')#HX711 (DOUT,SCK)           DOUT- pin #P21  et  PD_SCK-  pin #P22 
#capteur_20kg_2 = HX711(c.HX_DT_2, c.HX_SCK_2)     #capteur_20kg_2= HX711('P1', 'P2')   
capteur_20kg = ['capteur_20kg_1','capteur_20kg_2', 'capteur_20kg_3', 'capteur_20kg_4', 'capteur_20kg_5', 'capteur_20kg_6' ]
delai_avant_acquisition=c.delai_avant_acquisition        #on attend delai avant de lancer les mesures par le HX
nombre_capteurs=c.nombre_capteurs                          #nombre de capteurs sur la balance
tare_20kg =c.tare_20kg                                                 # [-44450,95900,-95950, -95950, -95950, -95950  ]           # tare 20kg_xx : valeur ADC sans rien sur le capteur le 04/04/2017 
valeur_20kg =c.valeur_20kg                                          #[478650, 613000,408200, 613500, 613500, 613500 ]   # etalonnage 20kg_1: valeur ADC avec l'étalon sur le capteur
etalon_20kg =c.etalon_20kg                                          # 5202                                                       # etalonnage 20kg_1: poids de l'étalon en grammes
mesure_20kg=[0, 0, 0, 0, 0, 0]
lecture_capteur=[0, 0, 0, 0, 0, 0,]
for i in(0,  nombre_capteurs-1):
     mesure_20kg[i] = valeur_20kg[i] -tare_20kg[i]         # etalonnage 20kg_1: mesure corrigée de la tare ADC avec l'étalon sur le capteur
     print("yessss")
GAIN_distant=c.GAIN_distant                                          #paramètres de mesure de la température : à régler pour chaque Lopy
OFFSET_distant=c.OFFSET_distant                                  #paramètres de mesure de la température : à régler pour chaque Lopy
GAIN_local=c.GAIN_local                                                  #paramètres de mesure de la température : à régler pour chaque Lopy
OFFSET_local=c.OFFSET_local                                          #paramètres de mesure de la température : à régler pour chaque Lopy

temperature_distant=0
temperature_local=0
poids_en_grammes=0
poids_en_gr_distant_total=0
poids_en_gr_local_total=0





if  configuration  in (110, 106, 206, 306):
     print ('ok configuration : ', configuration)
print ('vu et entendu')
if configuration ==  110 : # RX seul ON VA CONFIGURER LE RX il y a un capteurs sur le RX; il y a zero capteur sur le TX
     nombre_capteurs=1
     for i in (0, 0):
         lecture_capteur[i]=acquisitionCapteur20kg_1(tare_20kg[i ], mesure_20kg [i],  etalon_20kg , nombre_point )  #fait l'acquisition sur le capteur 20 kg_1 sur une moyenne de nombre_point
         poids_en_gr_distant=((lecture_capteur[i]-tare_20kg[i])/mesure_20kg[i]*etalon_20kg)
         print(" n°", i+1, poids_en_gr_distant)
         poids_en_gr_local_total=poids_en_gr_distant+poids_en_gr_local_total
     t=temperatureLopy(GAIN_local,OFFSET_local)#mesure de la température du RX***************************************************************************
     print("poids_en_gr_local_total",poids_en_gr_local_total,"Temperature ", t)
  

if configuration== 106: # ON VA CONFIGURER LE RX il y a 0 capteurs sur le RX; il y a six capteurs sur le TX; la trame reçue fait 37 octets : 1 [label] + 1 [numero_trame] +1 [T]+24 [6 long]+10 delimiteur
     octet_par_trame=37
     lora = LoRa(mode=LoRa.LORA, frequency=863000000)
     s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
     s.setblocking(False)
     if carte_sd:
         sd = SD()
         os.mount(sd, '/sd')

     while s.recv(128) == True:#********************************************
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
             if carte_sd and numero_trame - flashReadTrame() :
                 SdWriteData(trame_ch)     #on sauve la trame sur SD
                 flashWriteTrame ( numero_trame)#on écrit le nouveau numero de trame  
             else :
                 print ("erreur transmission")

 
if configuration ==  206 : #  ON VA CONFIGURER LE TX il y a x capteurs sur le RX; il y a six capteurs sur le TX; la trame émise fait 27 octets : 1 [label] + 1 n°trame +1 [T]+24 [6 long]
        while b < b_mesure_par_cycle : #on va envoyer b mesures pour fiabiliser la transmission
             b+=1
             lora = LoRa(mode=LoRa.LORA, frequency=863000000)
             s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
             s.setblocking(False)                     
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
             time.sleep(tempo_lora_emission)
             print (" T°C: ", t," numero_trame: ", numero_trame," b: ", b)       
        flashWriteTrame ( int(numero_trame) + 1)#on ecrit le numero de la prochaine trame sur la flash du TX
        b=0
        miseEnSommeil() #eteint Lopy  ******************************************
  
if  configuration == 306 : # RX: ON VA LIRE la carte SD; il y a 0 capteur sur le RX il y a six capteurs sur le TX; la trame carte_sd fait 37 octets : 1 [T]+24 [6* long]+1 label + 1 n° trame + 10 delimiteur
     lecture=lecture+1#mode lecture
     time.sleep (5)
     if (lecture==1) :         
         pass     
         #FIN DES ELIF      
print(" trame suivante ")

print("fin du programme")




