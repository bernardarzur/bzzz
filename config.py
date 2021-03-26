#accompagne TX_RX_v_18

import ubinascii
import struct
w='bzz_34b0'                                              #nom de la ruche ou du RX,  circuit PROTO 5 : quatre hx711 (n°13 à 16), Lopy4_4ad8,, attention P18, P17 et P10 ne sont pas cablées sur le lopy
configuration='TX'                                     #positionné à 'TX,' ou ' RX ' pour écouter la ruche en configuration point à point
mode_lora='APB'                                       #positionné à 'RAW,' en RX  pour écouter la ruche en configuration point à point (idem pour TX dans ce cas), sinon TX vers le réseau TTN en 'APB' ou 'OTAA'
nombre_capteurs=0                                   #nombre de capteurs sur la balance TX ou RX, 0 -> pas de capteurs : ce peut être le cas du RX, sinon de 1 à 4
premier_capteur =0                                    #indice du premier capteur TX ou RX, de 0 à 3 (si nombre_capteurs = 4, alors premier_capteur=0)
debug=1                                                     # normalement positionné à 0
date=[2019, 11,2,10, 0, 0, 0, 0]              # On met RX à l'heure, ne sert pas pour les TX, [aaaa,m,j,h,mn,s,ms,0], car lors du passage en deepsleep, TX perd la date?
sleep    =6000*10                                     #deepsleep en millisecondes
timeout=60000*10                                     # 60000 millisecondes font une minute
delai_local=2                                              #on attend delai local SECONDES avant de lancer une mesure, doit être inférieure à timeout
delai_flash_mise_en_route=0.02                #durée du flash de la LED
tempo_lora_demarrage = 0                        #le temps en secondes que la carte lora soit opérationnelle
tempo_lora_emission = 5                           #le temps en secondes que la carte lora finisse l'émission
delai_avant_acquisition= 0                         #on attend delai secondes avant de lancer les mesures par le HX

HX_DT_1    = 'P19'   # brochage HX vers Lopy : ne pas utiliser P12 qui sert pour les reboots ni P2,#P18 a P13 sont des INPUT, LoRa utilise  P5, P6, P7 : ne pas utiliser, P16 sert pour la batterie,
HX_SCK_1  = 'P23'   #brochage HX vers jauge 20kg ->Noir E-, Rouge E+, Vert  A+, Blanc A-  module 182409353771
HX_DT_2    = 'P8'
HX_SCK_2  = 'P22'
HX_DT_3    = 'P15'
HX_SCK_3  = 'P20'
HX_DT_4    = 'P13'
HX_SCK_4  = 'P21'

pinBatt='P16'                                    # mesure TENSION BATTERIE attenuation = 0 correspond à 1000mV, attn=1  à 3dB attn=2 à 6dB, attn=3 à 12 dB, pont diviseur (115k et 56k) sur expansion board V2.1A,
resolutionADC=4096                           #10 bits sur Lopy1 : 1024,  12 bits sur Lopy4 : 4096
attn=1                                                 #attn=1  à 3dB
range=10**(3/20)*1000                     # 1412 pour 3 dB
coeff_pont_div=(470+221)/221          #proto_5

#indice        0               1             2             3        # ce sont les valeurs des capteurs 13 à 16 ::: capteurs 20 kg_i : mesures du 1 septembre 2019 sur proto 5
tare =    [-159327,-96885,  -29883,  66287]       # tare  : valeur ADC sans rien sur le capteur
valeur =[503667 ,593906 ,660713,753035 ]       # etalonnage : valeur ADC avec l'étalon sur le capteur
etalon =[6930 ,   6930 ,    6930,    6930      ]       #  poids de l'étalon en grammes
coeff=   [0]*4
i=0
for g in tare:
    coeff[i] =   etalon[i] /(valeur[i] -tare[i]  )        #  coeff corrigé de la tare ADC, avec l'étalon sur le capteur, normée au poids, gramme/digit# poids_en_gr=((lecture_capteur[i]-tare[i])*mesure[i])
    i+=1

nombre_point=5                         #c'est le nombre d'acquisitions faites par le HX711, qui en fait une moyenne appelée mesure
label='label'                            #trame : champ de controle expéditeur sur label
delimiteur='d'                           #trame : champ delimiteur entre champs de la trame, ne pas utiliser d dans les autres champs, nom de la ruche entre autres!!!

GAIN_distant=0.80                                                                  #nok paramètres de mesure de la température : à régler pour chaque Arduino
OFFSET_distant=314
GAIN_local=1.22                                                                      #nok paramètres de mesure de la température : à régler pour chaque Arduino
OFFSET_local=318

#mode LoRa:  RAW,  APB,  OTAA;  LoRa-MAC (which we also call Raw-LoRa); LoRaWAN mode implements the full LoRaWAN stack for a class A device.
#It supports both OTAA and ABP connection methods; ABP stands for Authentication By Personalisation. It means that the encryption keys are configured manually on the device and can start sending
#frames to the Gateway without needing a 'handshake' procedure to exchange the keys;  On définit le mode de transmission LoRa, RAW (transmission la plus rapide entre TX et RX propriétaire sans cryptage,
#APB (on émet en mode crypté sans recevoir d'ACK de la part du récepteur qui est le RX ou la GW) et OTAA (mode complet mais, le plus lent, avec échange entre TX et récepteur)
LORA_FREQUENCY = 863000000       #parametres RAW
data_rate=5                                       # set the LoRaWAN data rate DR_5
dev_eui =( 0xD8,0x4A,0x78,0xFE,0xFF,0xA4,0xAE,0x30)       #à inverser  30aea4FFFE784ad8 nok
#parametres OTAA donnés par TTN
app_eui = ubinascii.unhexlify('BABE01D07ED5B370')#(0xBA,0xBE,0x01,0xD0,0x7E,0xD5,0xB3,0x70)# OTAA authentication parameters, à inverser70B3D57ED001BEBA, app_eui commune pour tous les bzzx de TTN (application fablablannionbzz
app_key = ubinascii.unhexlify('8374D4710960E6421BDCF15F639E8411')#pas  la bonne,
#parametres APB donnés par TTN
dev_addr = struct.unpack(">l", ubinascii.unhexlify('2601136A'))[0]            #parametres ABP 26011B2D OK
nwk_swkey = ubinascii.unhexlify('0E179E966E4D51189BA37C23BB226ED2')#(0xA3, 0xBE, 0x3D, 0x74, 0xAF, 0x21, 0x79, 0xFA, 0xB9, 0xE1, 0x1C, 0xFE, 0x07, 0xC5, 0x46, 0x87)# nok A3BE3D74AF2179FAB9E11CFE07C54687
app_swkey = ubinascii.unhexlify('28310CDC4DE95F89F86D3E64805C5551')#(0x83, 0x74, 0xD4, 0x71, 0x09, 0x60, 0xE6, 0x42, 0x1B, 0xDC, 0xF1, 0x5F, 0x63, 0x9E, 0x84, 0x11)#nok 8374D4710960E6421BDCF15F639E8411

# LED color
BLACK = 0x000000
blanc=    0x7f7f7f
GREEN = 0x007f00
vert_pale=0x000800
YELLOW = 0x7f7f00
jaune_pale=0x080800
RED = 0x7f0000
rouge_pale=0x080000
orange_pale=0xFF6600
BLUE = 0x00007f
bleu_pale=0x000008
violet=0xFF33CC
