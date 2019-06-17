#accompagne TX_RX_v_16
# configuration 1 :  ON VA CONFIGURER LE RX; il y a nombre_capteurs_rx capteurs sur le RX; il y a nombre_capteurs capteurs sur le TX
# configuration 2 :  ON VA CONFIGURER LE TX; il y a nombre_capteurs_rx capteurs sur le RX; il y a nombre_capteurs capteurs sur le TX
w='ruche_6574,1 HX avec connecteurs, carte expansion, pull_up'                    #nom de la ruche ou du RX, ou autre identifiant
configuration=2                                   #normalement positionné à 1, puisqu'on se place au RX pour écouter la ruche en configuration point à point, ne sert pas si on a une gateway TTN à portée   
debug=1                                              # normalement positionné à 1
wake=1                                                # normalement positionné à 1; pas de deepsleep wake =0, période d'émission selon delai_local,  deepsleep -> wake =1, période d'émission selon sleepdebug=1, ne sert pas pour les RX
date=[2019, 6, 2 ,11, 50, 0, 0, 0]       # On met RX à l'heure, ne sert pas pour les TX, [aaaa,m,j,h,mn,s,ms,0], car lors du passage en deepsleep, TX perd la date?

timeout=60000                                    # 60000 millisecondes font une minute
delai_local=10                                      #on attend delai local SECONDES avant de lancer une mesure, doit être inférieure à timeout
delai_flash_mise_en_route=0.1
sortie_relais_1='P9'#commande relais Celduc/ULN2003 pour alimenter les HX711, il en faut 2 pour le celduc, car le courant est limité à 12 mA, or il en faut 25(3.3/130)
sortie_relais_2='P9'

# brochage HX vers Lopy    pour le 20 kg ->Blanc pin#DOUT, Jaune pin#SCK, Noir   pin#GRND et Rouge pin#3.3volts -MAJ 3 avril 2017#GND ->P25  et 3.3Volts ->P24
#brochage HX vers jauge 20kg ->Noir E-, Rouge E+, Vert  A+, Blanc A-  module 182409353771
HX_DT_1    = 'P15'
HX_SCK_1  = 'P20'
HX_DT_2    = 'P14'
HX_SCK_2  = 'P21'
HX_DT_3    = 'P17'
HX_SCK_3  = 'P22'
HX_DT_4    = 'P18'
HX_SCK_4  = 'P23'
HX_DT_5     = 'P18'
HX_SCK_5   = 'P23'
HX_DT_6    = 'P18'
HX_SCK_6  = 'P23'
# ne pas utiliser P12 qui sert pour les reboots ni P2,#P18 a P13 sont des INPUT, LoRa utilise  P5, P6, P7 : ne pas utiliser,P16 sert pour la batterie,

nombre_capteurs_rx=0                #nombre de capteurs sur la balance RX
premier_capteur_rx=0                 #indice du premier capteur RX

nombre_capteurs=4                     #nombre de capteurs sur la balance TX, de 1 à 4 dans notre balance n°1
premier_capteur =1                      #indice du premier capteur TX
#indice        0               1             2             3              4             5            6            7             8          9           10        11        12         13       14         15
tare =    [279600,  -232000,             0,    40470,   72660,   69060, -110000,   188850,  72500 ,     0     ,     0     ,     0    ,    0     ,    0     ,    0     ,    0      ] # tare  : valeur ADC sans rien sur le capteur  
valeur =[1886000,  437500,   670900,  719900, 766150, 755500,  551000,  723000 , 103000,    1      ,     1     ,    1     ,    1     ,    1     ,    1     ,    1      ]  # etalonnage : valeur ADC avec l'étalon sur le capteur
etalon =[5202      ,       6930,       6930,    6930 ,      6930,     6930,     6930,        1550,     5202,     1     ,    1      ,    1     ,    1     ,    1     ,    1     ,    1      ]               #  poids de l'étalon en grammes
coeff=   [0]*16
i=0
for g in tare:
    coeff[i] =   etalon[i] /(valeur[i] -tare[i]  )        #  coeff corrigé de la tare ADC, avec l'étalon sur le capteur, normée au poids, gramme/digit# poids_en_gr=((lecture_capteur[i]-tare[i])*mesure[i])
    i+=1
# en position 0 :::        tare_10kg = 279600   lecture du capteur 10kg_leny sans rien dessus le 23/01/2017  etalon_10kg = 5202g    valeur_10kg = 1886000
# en position 1 à 6 ::: capteurs 20 kg_série_A : mesures du 13 décembre 2017
# en position 7 :::       tare_30kg = 188850 valeur ADC sans rien le 15/04/2017 etalon_30kg = 1550g    mesure_30kg = 723000 valeur ADC avec l'étalon sur la balance 
# en position 8 :::        tare_50kg = 72500  sans rien dessus le 23/01/2017 etalon_50kg = 5202   grammes lecture_50kg = 103000
# en position 9 à 14 ::: capteurs ADC, lectures brutes pour étalonnage
precision=0.01                            #precision souhaitée pour valider l'acquisition d'une mesure
nombre_point=3                         #c'est le nombre d'acquisitions faites par le HX711, qui en fait une moyenne appelée mesure
delai_avant_acquisition= 0      #on attend delai secondes avant de lancer les mesures par le HX

label='label'                            #champ de controle expéditeur sur label
delimiteur='d'                           #champ delimiteur entre champs de la trame, ne pas utiliser d dans les autres champs!!!

GAIN_distant=0.80                                                                  #paramètres de mesure de la température : à régler pour chaque Arduino
OFFSET_distant=314                                                               #paramètres de mesure de la température : à régler pour chaque Arduino
GAIN_local=1.22                                                                      #paramètres de mesure de la température : à régler pour chaque Arduino
OFFSET_local=318                                                                   #paramètres de mesure de la température : à régler pour chaque Arduino

# TTN Node IDs, correspond à bzz3 
DEV_EUI = '30AEA4FFFE786574'#30AEA4FFFE786574
APP_EUI = '70B3D57ED001BEBA'#70B3D57ED001BEBA
APP_KEY = '6DE7DBF77E29BA75A460A8E6D72CCF07'#


# LoRa setup
mode_lora='RAW'           #mode LoRa:  RAW,  APB,  OTAA;  LoRa-MAC (which we also call Raw-LoRa); LoRaWAN mode implements the full LoRaWAN stack for a class A device.
#It supports both OTAA and ABP connection methods; ABP stands for Authentication By Personalisation. It means that the encryption keys are configured manually on the device and can start sending 
#frames to the Gateway without needing a 'handshake' procedure to exchange the keys;  On définit le mode de transmission LoRa, RAW (transmission la plus rapide entre TX et RX propriétaire sans cryptage, 
    #APB (on émet en mode crypté sans recevoir d'ACK de la part du récepteur qui est le RX ou la GW) et OTAA (mode complet mais, le plus lent, avec échange entre TX et récepteur)
LORA_FREQUENCY = 863000000
data_rate=5                # set the LoRaWAN data rate DR_5

tempo_lora_demarrage = 0    #le temps en secondes que la carte lora soit opérationnelle
tempo_lora_emission = 0        #le temps en secondes que la carte lora finisse l'émission


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

#deepsleep en millisecondes
sleep=600000

