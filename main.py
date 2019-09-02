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
import pycom
import os
from hx711 import HX711
from network import LoRa
import socket 
import time
import config as c
import machine
from machine import WDT
from machine import RTC
from machine import ADC
import errno
from network import WLAN
import ubinascii

def acquisitionCapteur( capteur) :
     capteur.power_up()#reveille le HX711 n°'capteur'
     time.sleep (c.delai_avant_acquisition)
     lecture_capteur = capteur.read()
     capteur.power_down()# put the ADC in sleep mode
     return lecture_capteur
 
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

def flashReadData() : #on lit data dans fichier data
     ofi=open('fichier_data', 'r')
     t=ofi.read()
     ofi.close()
     return t   

def temperatureLopy(GAIN,OFFSET) :
    t=GAIN+OFFSET#***********************************************************fonction bidon
    return t
    
def tensionBatterie():
    adc = ADC()
    batt = adc.channel(attn=c.attn, pin=c.pinBatt)# attenuation = 1, correspond à 3dB: gamme 0-1412 mV, pont diviseur (115k et 56k) sur expansion board V2.1A de 3.05, ADC 12 bits : 4096
    v=batt.value()
    if v==c.resolutionADC-1:
        v=-1
    #v=int(v*c.range/c.resolutionADC*c.coeff_pont_div)#mV
    return v

#Init constantes, selon fichier config.py
configuration=c.configuration                                     #configuration   =1 on configure le RX,  configuration   =2 on configure le TX,
debug=c.debug
wake=c.wake   # pas de deepsleep wake =0, période d'émission selon delai_local,  mise en sommeil du TX entre deux mesures (deepsleep) -> wake =1, période d'émission égale à sleep + temps de mesure
mode_lora=c.mode_lora                                             #mode LoRa:  RAW,  APB,  OTAA; 
data_rate=c. data_rate # set the LoRaWAN data rate
nombre_point=c.nombre_point                                   #c'est le nombre d'acquisitions faites par le HX711, qui en fait une moyenne appelée mesure
label=c.label                                                                #controle expéditeur sur label, en mode RAW seulement
delimiteur=c.delimiteur                                               #delimiteur entre champs de la trame
w=c.w                                                                          #champ identification (nom de la ruche, ...)

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
capteur_5 = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur 20kg_i  
capteur_6 = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur 20kg_i  
capteur_7 = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur 30kg
capteur_8 = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur 50kg
capteur_9  = HX711(c.HX_DT_1, c.HX_SCK_1)     #capteur ADC     
capteur_10 = HX711(c.HX_DT_2, c.HX_SCK_2)    #capteur ADC  
capteur_11 = HX711(c.HX_DT_3, c.HX_SCK_3)    #capteur ADC  
capteur_12 = HX711(c.HX_DT_4, c.HX_SCK_4)    #capteur ADC  
capteur_13 = HX711(c.HX_DT_1, c.HX_SCK_1)    #capteur 20kg_i  
capteur_14 = HX711(c.HX_DT_2, c.HX_SCK_2)    #capteur 20kg_i 
capteur_15 = HX711(c.HX_DT_3, c.HX_SCK_3)    #capteur 20kg_i
capteur_16 = HX711(c.HX_DT_4, c.HX_SCK_4)    #capteur 20kg_i
capteurs=[capteur_0,capteur_1,capteur_2,capteur_3,capteur_4,capteur_5,capteur_6,capteur_7,capteur_8,capteur_9,capteur_10,capteur_11,capteur_12,capteur_13,capteur_14, capteur_15, capteur_16]
tare =c.tare                                                  # tare_i : valeur ADC sans rien sur le capteur
coeff=c.coeff                                                #coeff multiplicateur pour obtenir des grammes 
sleep=c.sleep                                               #init deepsleep

##############DEBUT PROG

temperature_distant=temperature_local=poids_en_grammes=poids_en_gr_distant_total=poids_en_gr_local_total=numero_trame=0
lecture_capteur=[0]*9
rtc = RTC()
rtc.init(c.date)
pycom.heartbeat(False)
pycom.rgbled(c.violet)                                             # flash violet            
time.sleep (c.delai_flash_mise_en_route)
pycom.rgbled(c.BLACK)
wdt = WDT(timeout=c.timeout)                                 # enable  watchgdog with a timeout of c.timeout milliseconds    
print ('configuration: ', configuration,  'mode_lora:  ', mode_lora,'debug:',  debug, 'mise en sommeil: ', wake,'date: ',   rtc.now(), 'premier_capteur_TX: ', c.premier_capteur, 'nombre_capteurs_TX: ', c.nombre_capteurs, 'premier_capteur_RX: ', c.premier_capteur_rx, 'nombre_capteurs_RX: ', c.nombre_capteurs_rx, 'tension_Batterie digits : ', tensionBatterie())
if debug:    #permet de recuperer le dev_eui
    wl = WLAN()
    print('dev_eui : ', ubinascii.hexlify(wl.mac())[:6] + 'FFFE' + ubinascii.hexlify(wl.mac())[6:])
    
    
if configuration== 1: # On va écouter le TX  en point à point seulement (la configuration du TX dans ce cas est forcement en RAW) et lire le RX si besoin, 
#il y a  nombre_capteurs_rx capteurs sur le RX; il y a nombre_capteurs capteurs sur le TX;  ne fonctionne qu'en mode LoRa RAW
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
                #temperature_distant   =(float(trame[1])/2.5-30)
                v   =int(trame[1]) #tension_Batterie
                temperature_local       =temperatureLopy(c.GAIN_local,c.OFFSET_local)            #trame [0]=label, trame [1]=  température, trame [2]=w 
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
            print(trame_ch," poids_total: ", poids_en_gr_distant_total,  " T_RX: ", temperature_local,   " N_T: ", numero_trame, "tension_Batterie : ", v, "batt_local : ",  tensionBatterie())      
        deltaT=time.time()-t0       #si pas de transmission pendant 2 fois le temps de deepsleep, on allume en rouge
        if deltaT> c.sleep*2/1000:
            pycom.rgbled(c.RED)
        else:
            pycom.rgbled(c.BLACK)            
        time.sleep(c.delai_local)  
        

        print (" ", deltaT, end="")

        if c.nombre_capteurs_rx!=  0 : #On va mesurer sur le RX il y a  nombre_capteurs_rx capteurs sur le RX; il y a nombre_capteurs capteurs sur le TX
            trame=''
            poids_en_gr=poids_en_gr_total=0
            for i in range(premier_capteur_rx, nombre_capteurs_rx+premier_capteur_rx): #on fait la mesure sur les i capteur_i de premier_capteur à premier_capteur+nombre_capteurs
                capteur=capteurs[i]
                lecture_capteur[i-premier_capteur]=n= moyenne=0
                capteur.power_up()#reveille le HX711 n°'capteur'
                time.sleep (c.delai_avant_acquisition)
                for n in range(0, nombre_point) :
                    lecture_capteur[i-premier_capteur]=capteur.read()  #fait l'acquisition sur le capteur _i 
                    lecture_capteur[i-premier_capteur]= (lecture_capteur[i-premier_capteur]-tare[i])*coeff[i]
                    if debug: 
                        print('capteur n°', i,  '   poids ',  lecture_capteur[i-premier_capteur], end="")
                        pycom.rgbled(c.jaune_pale)
                        time.sleep (c.delai_avant_acquisition)
                    moyenne+=lecture_capteur[i-premier_capteur]
                    n+=1
            lecture_capteur[i-premier_capteur]=moyenne/n
            poids_en_gr_total+= lecture_capteur[i-premier_capteur]
            trame+=str( lecture_capteur[i-premier_capteur])+delimiteur            
            capteur.power_down()# put the ADC n° i in sleep mode 
            i+=1
            t=temperatureLopy(c.GAIN_local,c.OFFSET_local)                     #mesure de la température du TX***************************************************************************    
            timest = time.localtime()                                                      #on met un timestamp sur la trame
            trame=str(timest)+delimiteur+str(t)+trame+delimiteur+"\n"
            flashWriteData(trame)
            print("poids_en_gr_total", poids_en_gr_total, " Température RX: ", t, '****', trame)
            time.sleep(c.delai_local)       
        wdt.feed() # feeds  watchgdog



if configuration== 2               : # ON VA CONFIGURER LE TX, il y a nombre_capteurs capteurs sur le TX; 
#trame=[label+delimiteur]+str(t)+delimiteur+w+{delimiteur+str(lecture_capteur[i])}*nombre_capteurs+delimiteur+"\n"; la trame RAW nécessite un "label" pour identification sans ambigüité
    adc = ADC()
    batt = adc.channel(attn=c.attn, pin=c.pinBatt)# attenuation = 1, correspond à 3dB: gamme 0-1412 mV, pont diviseur (115k et 56k) sur expansion board V2.1A de 3.05, ADC 12 bits : 4096   
    
    if mode_lora== 'RAW'              : # On définit le mode de transmission LoRa, RAW (transmission la plus rapide entre TX et RX propriétaire sans cryptage), LoRa-MAC (which we also call Raw-LoRa)
        lora = LoRa(mode=LoRa.LORA, frequency=c.LORA_FREQUENCY)
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        s.setblocking(False)
        
    if mode_lora== 'APB'              : #APB (on émet en mode crypté sans recevoir d'ACK de la part du récepteur qui est le RX ou la GW) ABP stands for Authentication By Personalisation. 
        lora = LoRa(mode=LoRa.LORAWAN, frequency=c.LORA_FREQUENCY)      
        lora.join(activation=LoRa.ABP, auth=(c.dev_addr,c.nwk_swkey, c.app_swkey))        # join a network using ABP (Activation By Personalization), Les clés ont été  fournies avant le joint par TTN (par ex).      
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)        # create a LoRa socket        
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, data_rate)        # set the LoRaWAN data rate
        s.setblocking(True)                # make the socket blocking
        
    if mode_lora== 'OTAA'              : #  OTAA (mode complet mais, le plus lent, avec échange entre TX et récepteur)
        lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
        lora.join(activation=LoRa.OTAA, auth=(c.app_eui, c.app_key), timeout=0)        # join a network using OTAA (Over the Air Activation) needing a 'handshake' procedure to exchange the keys  

        while not lora.has_joined():                # wait until the module has joined the network
            time.sleep(2.5)
            print('Not yet joined...')
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)        # create a LoRa socket
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)        # set the LoRaWAN data rate
        s.setblocking(True)        # make the socket blocking       # (waits for the data to be sent and for the 2 receive windows to expire)
    
    while True:
        pycom.rgbled(c.BLACK)
        if debug:
            pycom.rgbled(c.bleu_pale)             
        trame=''
        poids_en_gr=poids_en_gr_total=moyenne=tension=0
        t1=moy=[0]*nombre_point
        for i in range(premier_capteur, nombre_capteurs+premier_capteur): #on fait la mesure sur les i capteur_i de premier_capteur à premier_capteur+nombre_capteurs
            capteur=capteurs[i]
            lecture_capteur[i-premier_capteur]=n= moyenne=0
            capteur.power_up()#reveille le HX711 n°'capteur'
            time.sleep (c.delai_avant_acquisition)
            for n in range(0, nombre_point) :
                lecture_capteur[i-premier_capteur]=capteur.read()  #fait l'acquisition sur le capteur _i 
                lecture_capteur[i-premier_capteur]=int( (lecture_capteur[i-premier_capteur]-tare[i])*coeff[i])#calcule le poids en grammes
                if debug: 
                    print(' capteur n°', i,  '   poids ',  lecture_capteur[i-premier_capteur], end="")
                    pycom.rgbled(c.GREEN)
                    time.sleep (c.delai_avant_acquisition)
                moy[n]=int(lecture_capteur[i-premier_capteur])
                n+=1
            moy.sort()
            lecture_capteur=[0]*9
            poids_en_gr_total=0
            for n in range(1, nombre_point-1):#on élimine minimum et maximum
                lecture_capteur[i-premier_capteur]+=moy[n]
                n+=1
            lecture_capteur[i-premier_capteur]=int(lecture_capteur[i-premier_capteur]/(nombre_point-2))
            poids_en_gr_total+= lecture_capteur[i-premier_capteur]
            trame+=str( lecture_capteur[i-premier_capteur])+delimiteur            
            capteur.power_down()# put the ADC n° i in sleep mode 
            i+=1
        for n in range(0, nombre_point) :
            t1[n]=batt.value()
            if debug:
                print('tension_digits : ', t1[n], end='')  
            n+=1
        t1.sort()
        tension=0
        for n in range(1, nombre_point-1):#on élimine minimum et maximum
            tension+=t1[n]
            n+=1 
        tension=int(tension*c.range/c.resolutionADC*c.coeff_pont_div /(nombre_point-2))#mesure de la tension Batterie du TX en mV
        if mode_lora=='RAW' :
            trame=label+delimiteur+str(tension)+delimiteur+w+delimiteur+trame
        else:
            trame=str(tension)+delimiteur+w+delimiteur+trame
        if debug:
            pycom.rgbled(c.blanc)
        try:            
            s.send (trame) 
            time.sleep(c.tempo_lora_emission)                
        except Exception as e:
            if e.errno == errno.EAGAIN:
                if debug: 
                    print('cannot send just yet, waiting...  ')                  
                time.sleep(0.5)   
        s.setblocking(False)
        numero_trame+=1  
        if debug:
            print("poids_en_gr_total", poids_en_gr_total, " tension_Batterie: ", tension, '****'," N_T: ",  numero_trame," ",  trame)                                                                                               
        if not wake :
            pycom.rgbled(c.GREEN)
            wdt.feed()                                                          # feeds  watchdog 
            time.sleep(c.delai_local)        
        if wake: 
            pycom.rgbled(c.RED)                                             # flash rouge            
            time.sleep (c.delai_flash_mise_en_route)                
            machine.deepsleep(c.sleep)                                     #eteint Lopy
        pycom.rgbled(c.BLUE)
        time.sleep (c.delai_flash_mise_en_route)

print('FIN')
