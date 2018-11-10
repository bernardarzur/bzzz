#version V1 : y a le local capteur et le distant, on peut tester en local (sans lora), on enregistre sur eeprom un des deux capteurs v2 -> deux capteurs locaux et un distant; v3 -> corrige gros
#bug : il faut faire une pseudo-mesure avant de démarrer, bof, finalement on fait moyenne de 100 mesures, v4-> temperature et label, v5-> deux capteurs dans le distant (poids = somme des deux)
#v6-> on rajoute un capteur local aux deux distants (v5 ne marche plus) puis versions tx_rx_v1: on y met les deux, ainsi que la lecture; version tx_rx_v2 : config 4 capteurs 20kg;
#version tx_rx_v3 : on fait un cycle de mesures sur n points, b fois de suite en envoyant un numéro de trame sauvé sur EEPROM TX (on s'est aperçu qu'on perdait bcp de trames), tx_rx_v_4 : 6 capteurs
#version tx_rx_v_1.py : on passe en python,v_9 commence à marcher avec un capteur sauf HX711 mode degradé; v_10 hx711 semble marcher après exclusion des valeurs 2**n-1;
#v_11 : deux capteurs conf 120, v_12 : 6 capteurs RX et TX; 
#v_13 : mauvaise précision sur v_12, on va tester la mesure par rapport à la dernière archivée sur flash TX avec un paramètre de précision;
#v_14 : on allege conf 206 ->conf 2, un cycle dure 12 secondes pour pouvoir émettre 20 000 trames avec 2600 mAh *2 (on vise 50000) , on passe au Lopy 4 (suppression du shield deepsleep et donc de deepsleep.py
#v_15 : on rajoute un chien de garde pour éviter les plantages réguliers (tous les 2/3 jours pour TX, un peu mieux pour RX), on passe tous les paramètres à config
#v_16 : on transmet le poids et non plus la valeur brute ADC
import pycom
import errno
import os
from hx711 import HX711
from network import LoRa
import socket 
import time
import config as c
import machine
from machine import WDT
from machine import RTC
from machine import Pin

#############################################################################################################################
def alimCapteurs(etat) :# ferme le relais via les sorties 1 et 2
    relais_alim_1_hx711=Pin(c.sortie_relais_1,  mode=Pin.OUT)  
    relais_alim_2_hx711=Pin(c.sortie_relais_2, mode=Pin.OUT)     
    if etat:
        relais_alim_1_hx711.value(1)#mise en tension relais
        relais_alim_2_hx711.value(1)
    else:
        relais_alim_1_hx711.value(0)#mise hors tension relais
        relais_alim_2_hx711.value(0)        
    return

def acquisitionCapteur( capteur) :
     capteur.power_up()#reveille le HX711 n°'capteur'
     time.sleep (delai_avant_acquisition)
     lecture_capteur = capteur.read()
     capteur.power_down()# put the ADC in sleep mode
     return lecture_capteur
 
def flashWriteData(trame) : #on écrit trame dans fichier data
    ofi=open('fichier_data', 'a')
    dispo=os.getfree('/flash')# vérifie si y a de la place sur flash
    if dispo > 100:
        ofi.write(trame)
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

def flashWriteMeasure(mesure,) : #on écrit les mesures dernière trame dans fichier mesure
     ofi=open('fichier_derniere_mesure', 'w')
     ofi.write(mesure)
     ofi.close()
     return

def flashReadMeasure() : #on lit les mesures dernière trame dans fichier mesure
     ofi=open('fichier_derniere_mesure', 'r')
     t=ofi.read()
     ofi.close()
     return t

def temperatureLopy(GAIN,OFFSET) :
    t=GAIN+OFFSET#***********************************************************fonction bidon
    return t
######################################DEBUT PROGRAMME#########################################################################

rtc = RTC()
rtc.init(c.date)
pycom.heartbeat(False)
pycom.rgbled(c.YELLOW)                                           #arrete clignotement led bleue, fait un flash jaune
wdt = WDT(timeout=c.timeout)                                 # enable  watchgdog with a timeout of c.timeout milliseconds

#Init constantes, selon fichier config.py
configuration=c.configuration                                     #configuration   =1 on configure le RX,  configuration   =2 on configure le TX,
debug=c.debug
wake=c.wake   # pas de deepsleep wake =0, période d'émission selon delai_local,  mise en sommeil du TX entre deux mesures (deepsleep) -> wake =1, période d'émission égale à sleep + temps de mesure

tempo_lora_demarrage = c.tempo_lora_demarrage   #le temps que la carte lora soit opérationnelle
tempo_lora_emission = c.tempo_lora_emission          #le temps que la carte lora finisse l'émission
nombre_point=c.nombre_point                                   #c'est le nombre d'acquisitions faites par le HX711, qui en fait une moyenne appelée mesure
label=c.label                                                                #controle expéditeur sur label
delimiteur=c.delimiteur                                               #delimiteur entre champs de la trame
w=c.w                                                                          #champ identification (nom de la ruche, ...)
delai_avant_acquisition=c.delai_avant_acquisition      #on attend delai avant de lancer les mesures par le HX
delai_local=c.delai_local                                               #on attend delai local avant de lancer une mesure
precision=c.precision                                                   #precision souhaitée pour valider l'acquisition d'une mesure
nombre_capteurs=c.nombre_capteurs                #nombre de capteurs sur la balance TX    
premier_capteur  =c.premier_capteur                 #premier_capteur  sur la balance TX
nombre_capteurs_rx=c.nombre_capteurs_rx       #nombre de capteurs sur la balance RX 
premier_capteur_rx=c.premier_capteur_rx          #premier_capteur  sur la balance RX
# Init HX711 module, hx.tare(c.HX_TARE), hx.set_scale(c.HX_SCALE)#cf fichier config capteur_i= HX711(DOUT,SCK)
capteur_0 = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur 10kg

capteur_1 = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur 20kg_i     
capteur_2 = HX711(c.HX_DT_2, c.HX_SCK_2)     #capteur 20kg_i  
capteur_3 = HX711(c.HX_DT_3, c.HX_SCK_3)     #capteur 20kg_i  
capteur_4 = HX711(c.HX_DT_4, c.HX_SCK_4)     #capteur 20kg_i  
capteur_5 = HX711(c.HX_DT_5, c.HX_SCK_5)     #capteur 20kg_i  
capteur_6 = HX711(c.HX_DT_6, c.HX_SCK_6)     #capteur 20kg_i  

capteur_7 = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur 30kg
capteur_8 = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur 50kg

capteur_9  = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur ADC     
capteur_10 = HX711(c.HX_DT_2, c.HX_SCK_2)    #capteur ADC  
capteur_11= HX711(c.HX_DT_3, c.HX_SCK_3)     #capteur ADC  
capteur_12 = HX711(c.HX_DT_4, c.HX_SCK_4)   #capteur ADC  
capteur_13= HX711(c.HX_DT_5, c.HX_SCK_5)    #capteur ADC  
capteur_14= HX711(c.HX_DT_6, c.HX_SCK_6)    #capteur ADC 

capteurs=[capteur_0,capteur_1,capteur_2,capteur_3,capteur_4,capteur_5,capteur_6,capteur_7,capteur_8,capteur_9,capteur_10,capteur_11,capteur_12,capteur_13,capteur_14]

#Init paramètres capteurs
tare =c.tare                                                  # tare_i : valeur ADC sans rien sur le capteur
coeff=c.coeff                                               #coeff multiplicateur pour obtenir des grammes 
#init deepsleep
sleep=c.sleep

#init temperature********************************************ne marche pas
GAIN_distant=c.GAIN_distant                                          #paramètres de mesure de la température : à régler pour chaque Lopy
OFFSET_distant=c.OFFSET_distant                                  #paramètres de mesure de la température : à régler pour chaque Lopy
GAIN_local=c.GAIN_local                                                 #paramètres de mesure de la température : à régler pour chaque Lopy
OFFSET_local=c.OFFSET_local                                         #paramètres de mesure de la température : à régler pour chaque Lopy

#Init variables locales
temperature_distant=temperature_local=poids_en_grammes=poids_en_gr_distant_total=poids_en_gr_local_total=0
lecture_capteur=[0]*9

liste=[0]*24                                                                    # liste des valeurs HX711 déclarées "fausses"
for i in range (24):
    liste[i]=2**i-1
    
print ('configuration:', configuration,  'debug:',  debug, 'mise en sommeil: ', wake,'date: ',   rtc.now(), 'premier_capteur_TX', c.premier_capteur, 'nombre_capteurs_TX', c.nombre_capteurs, 'premier_capteur_RX', c.premier_capteur_rx, 'nombre_capteurs_RX', c.nombre_capteurs_rx)

if configuration== 1: # On va écouter le TX et lire le RX si besoin, il y a  nombre_capteurs_rx capteurs sur le RX; il y a nombre_capteurs capteurs sur le TX;   
#trame enregistrée=label+delimiteur+str(numero_trame)+delimiteur+str(t)+delimiteur+w+{delimiteur+str(lecture_capteur[i])}*nb_capteurs+delimiteur+time_stamp+delimiteur+"\n"        
    lora = LoRa(mode=LoRa.LORA, frequency=c.LORA_FREQUENCY)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    while True:   
        trame_ch=s.recv(128)     
        pycom.rgbled(c.vert_pale)             
        time.sleep(2)         
        if trame_ch:      
            pycom.rgbled(c.rouge_pale)  
            print( "trame : ", trame_ch)
            time.sleep(2)         
            trame = trame_ch.decode('utf-8')                      #sinon pbs compatibilité avec binaire?
            trame=trame.split(delimiteur)                               #on vire le delimiteur et on met les data dans une liste        
            poids_en_gr_distant_total=0
            i=0
            if trame[0] ==label :                                             #vérification champ 0  pour controle destinataire
                temperature_distant   =(float(trame[2])/2.5-30)
                temperature_local       =temperatureLopy(GAIN_local,OFFSET_local)/2.5-30            #trame [0]=label, trame [1]=numéro trame, trame [2]=  température, trame [3]=w 
                for g in trame:
                    if i >=4:
                        if g!='':
                            poids_en_gr_distant_total+=float(g)
                    print ("i ", i,"   g ", g, "    poids_en_gr_distant_total ", poids_en_gr_distant_total)
                    i+=1
                pycom.rgbled(c.vert_pale)            
                time.sleep(2) 
                numero_trame  =int(trame[1])
                trame_flash=int(flashReadTrame())
                if abs(numero_trame - trame_flash)>1:          #si la différence est supérieure à 1, il y a des trames perdues
                    print (" perte trames: ",  numero_trame - trame_flash)          
                t=rtc.now()                                                      #on fait un timestamp, le temps  est initialisé dans la config
                ts=''
                for g in t: 
                    ts+=str(g)+delimiteur
                trame_ch+=ts+'\n'                                       #on ajoute le timestamp à la trame reçue
                flashWriteData(trame_ch)                               #on sauve la trame sur flash
                flashWriteTrame ( (trame[1]))                        #on écrit le nouveau numero de trame
            else:
                print ("erreur transmission")                
            print("poids_total : g ", poids_en_gr_distant_total, " T RX: ", temperature_local, " T TX: ", temperature_distant)
            time.sleep(1)       
        pycom.rgbled(c.bleu_pale)             
        time.sleep(2)  
    

        if c.nombre_capteurs_rx!=  0 : #On va mesurer sur le RX il y a  nombre_capteurs_rx capteurs sur le RX; il y a nombre_capteurs capteurs sur le TX
            numero_trame=0
            poids_en_gr_total=b=0
            trame=''
            poids_en_gr=poids_en_gr_total=0
            for i in range(premier_capteur_rx, nombre_capteurs_rx+premier_capteur_rx):#on fait la mesure sur les i capteur_i de premier_capteur_rx à nombre_capteurs_rx+premier_capteur_rx
                capteur=capteurs[i]
                lecture_capteur[i]=0
                j=n= moyenne=0
                while j < nombre_point and n< nombre_point:
                    lecture_capteur[i]=acquisitionCapteur(capteur)  #fait l'acquisition sur le capteur _i 
                    print('capteur n°', i, ' ', lecture_capteur[i], 'poids ',  (lecture_capteur[i]-tare[i])*coeff[i])
                    moyenne+=lecture_capteur[i]
                    if lecture_capteur[i] in liste:
                        moyenne-=lecture_capteur[i]                     
                        print("liste ",  end="")
                        j-=1
                        n+=1
                    j+=1
                if n>=nombre_point:                     
                    print ('beaucoup d\'erreurs capteur n°', i,  end="")
                if j:                                                 
                    lecture_capteur[i]=moyenne/j
                poids_en_gr=((lecture_capteur[i]-tare[i])*coeff[i])
                print(" n°", i, poids_en_gr,"  ", lecture_capteur[i],  end="" )
                poids_en_gr_total=poids_en_gr+poids_en_gr_total
                trame+=delimiteur+str(lecture_capteur[i])
                i +=1
            numero_trame+=1 
            t=temperatureLopy(GAIN_local,OFFSET_local)                     #mesure de la température du TX***************************************************************************    
            timest = time.localtime()                                                      #on met un timestamp sur la trame
            trame=str(timest)+delimiteur+str(numero_trame)+delimiteur+str(t)+trame+delimiteur+"\n"
            flashWriteData(trame)
            print("poids_en_gr_total", poids_en_gr_total, " Température RX: ", t,  " n° trame: ", numero_trame, '****', trame)
        time.sleep(delai_local)       
        wdt.feed() # feeds  watchgdog



if configuration== 2               : # ON VA CONFIGURER LE TX, il y a nombre_capteurs capteurs sur le TX; 
#trame=label+delimiteur+str(numero_trame)+delimiteur+str(t)+delimiteur+w+{delimiteur+str(lecture_capteur[i])}*nombre_capteurs+delimiteur+"\n"        
    lora = LoRa(mode=LoRa.LORA, frequency=c.LORA_FREQUENCY)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
 
    while True:
        alimCapteurs(1)                                         #on alimente les HX711
        if debug:
            pycom.rgbled(c.bleu_pale)             
        trame=''
        poids_en_gr=poids_en_gr_total=0
        m=flashReadMeasure()
        derniere_mesures=m.split(delimiteur)                          #on vire le delimiteur et on met les data dans une liste    
        for i in range(premier_capteur, nombre_capteurs+premier_capteur): #on fait la mesure sur les i capteur_i de premier_capteur à premier_capteur+nombre_capteurs
            capteur=capteurs[i]
            derniere_mesure=float (derniere_mesures[i-premier_capteur])#démarre à indice= zéro
            lecture_capteur[i-premier_capteur]=j=n= moyenne=0
            while j < nombre_point and n< nombre_point:
                lecture_capteur[i-premier_capteur]=acquisitionCapteur(capteur)  #fait l'acquisition sur le capteur _i 
                lecture_capteur[i-premier_capteur]= (lecture_capteur[i-premier_capteur]-tare[i])*coeff[i]
                if debug: 
                    print('capteur n°', i,  '   poids ',  lecture_capteur[i-premier_capteur], end="")
                    pycom.rgbled(c.jaune_pale)
                moyenne+=lecture_capteur[i-premier_capteur]
                if abs(lecture_capteur[i-premier_capteur] -derniere_mesure)>=precision*abs(derniere_mesure):
                    moyenne-=lecture_capteur[i-premier_capteur]                     
                    if debug: 
                        print("  erreurs  ", end="")
                        pycom.rgbled(c.orange_pale)
                    j-=1
                    n+=1
                j+=1
            if n>=nombre_point:           #trop d'erreurs, on refait une deuxième série de mesures
                lecture_capteur[i-premier_capteur]=j=n= moyenne=0
                while j < nombre_point and n< nombre_point:
                    lecture_capteur[i-premier_capteur]=acquisitionCapteur(capteur)  #fait l'acquisition sur le capteur _i 
                    if debug: 
                        print('capteur n°', i,  ' valeur ADC  ',  lecture_capteur[i-premier_capteur], end="")
                        pycom.rgbled(c.rouge_pale)
                    moyenne+=lecture_capteur[i-premier_capteur]
                    if lecture_capteur[i-premier_capteur] in liste:
                        moyenne-=lecture_capteur[i-premier_capteur]                     
                        if debug: 
                            print(" liste  ", end="") 
                            pycom.rgbled(c.RED)
                        j-=1
                        n+=1
                    j+=1
            if n>=nombre_point and debug:                     
                print ('  beaucoup d\'erreurs capteur n°', i , end="")
            if j:                                                
                lecture_capteur[i-premier_capteur]=moyenne/j
            lecture_capteur[i-premier_capteur]= (lecture_capteur[i-premier_capteur]-tare[i])*coeff[i]
            if debug:
                print('  capteur n°', i, '   poids ',  lecture_capteur[i-premier_capteur])
                pycom.rgbled(c.violet)
                time.sleep(0.5)
            poids_en_gr_total+= lecture_capteur[i-premier_capteur]
            trame+=str( lecture_capteur[i-premier_capteur])+delimiteur 
        alimCapteurs(0)                                                           #on coupe l'alimentation des HX711
        numero_trame= int(flashReadTrame() )                     #on lit le n° trame sur flash du TX
        t=temperatureLopy(GAIN_distant,OFFSET_distant)     #mesure de la température du TX
        flashWriteMeasure(trame)                                           #on stocke la dernière mesure sur le TX
        trame=label+delimiteur+str(numero_trame)+delimiteur+str(t)+delimiteur+w+delimiteur+trame        
        try:            
            s.send (trame) 
            if debug: 
                print (trame)             
            time.sleep(tempo_lora_emission)                
        except Exception as e:
            if e.errno == errno.EAGAIN:
                if debug: print('cannot send just yet, waiting...  ', b)                  
                time.sleep(0.5)
        flashWriteTrame (str( numero_trame+1))                   #on ecrit le numero de la prochaine trame sur la flash du TX
        if debug:
            flashWriteData(trame)                                            #on sauve les data sur le TX, si debug
            pycom.rgbled(c.vert_pale)             
            time.sleep(2)           
            pycom.rgbled(c.blanc)             
            print("poids_en_gr_total", poids_en_gr_total, " Température TX: ", t,  " n° trame: ", numero_trame, '****', trame)
        wdt.feed()                                                                  # feeds  watchdog 
        if wake: 
            pycom.rgbled(c.RED)                                             # flash rouge
            time.sleep(tempo_lora_emission)                
            machine.deepsleep(sleep)                                     #eteint Lopy
        else :
            pycom.rgbled(c.GREEN)
            time.sleep(delai_local)

print('FIN')
