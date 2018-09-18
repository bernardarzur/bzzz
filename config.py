# configuration 1 : RX ET TX, ON VA CONFIGURER LE RX; il y a x capteurs sur le RX; il y a y capteurs sur le TX
# configuration 2 : RX ET TX, ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a y capteurs sur le TX
configuration=2
debug=1
wake=1                                                           # pas de deepsleep wake =0, période d'émission selon delai_local,  deepsleep -> wake =1, période d'émission selon sleepdebug=1
date=[2018, 9,  7, 11, 10, 0, 0, 0]
timeout=300000
delai_local=10                            #on attend delai local SECONDES avant de lancer une mesure
# brochage HX vers Lopy    pour le 20 kg ->Blanc pin#DOUT, Jaune pin#SCK, Noir   pin#GRND et Rouge pin#3.3volts -MAJ 3 avril 2017#GND ->P25  et 3.3Volts ->P24
#brochage HX vers jauge 20kg ->Noir E-, Rouge E+, Vert  A+, Blanc A-  module 182409353771
HX_DT_1    = 'P4'#P18 a P13 sont des INPUT
HX_SCK_1  = 'P3'
# HX711_2
HX_DT_2    = 'P13'
HX_SCK_2  = 'P22'
# HX711_3
HX_DT_3    = 'P15'#la P16 sert pour tension batterie?
HX_SCK_3  = 'P21'
# HX711_4
HX_DT_4    = 'P14'
HX_SCK_4  = 'P20'
# HX711_5
HX_DT_5     = 'P23'
HX_SCK_5   = 'P9'
# HX711_6
HX_DT_6    = 'P11'#P10 sert aussi a SPIO CLK et P11 a SPIO MOSI 
HX_SCK_6  = 'P8'#P10, P17, P18 pas possibles?, servent au deepsleep, P23 ne marche pas?(sur le 34b), ne pas utiliser P12 qui sert pour les reboots 

nombre_capteurs_rx=0                #nombre de capteurs sur la balance RX, de 1 à 6 dans notre balance n°1
premier_capteur_rx=0                 #indice du premier capteur TX

nombre_capteurs=6                     #nombre de capteurs sur la balance TX, de 1 à 6 dans notre balance n°1
premier_capteur =1                      #indice du premier capteur TX
#indice        0               1             2             3              4             5            6            7             8 
tare =    [279600,  -232000,             0,  69060, -110000,    40470,   72660,  188850,  72500  ] # tare  : valeur ADC sans rien sur le capteur  
valeur =[1886000,  437500,   670900,755500,  551000,  719900, 766150,  723000 , 103000 ]  # etalonnage : valeur ADC avec l'étalon sur le capteur
etalon =[5202,            6930,       6930,    6930,       6930,     6930,     6930,        1550,     5202]               #  poids de l'étalon en grammes
mesure=   [0]*9
lecture_capteur=[ 0]*9
# en position 0 :::        tare_10kg = 279600   lecture du capteur 10kg_leny sans rien dessus le 23/01/2017  etalon_10kg = 5202g    valeur_10kg = 1886000
# en position 1 à 6 ::: capteurs 20 kg_série_A : mesures du 13 décembre 2017
# en position 7 :::       tare_30kg = 188850 valeur ADC sans rien le 15/04/2017 etalon_30kg = 1550g    mesure_30kg = 723000 valeur ADC avec l'étalon sur la balance 
# en position 8 :::        tare_50kg = 72500  sans rien dessus le 23/01/2017 etalon_50kg = 5202   grammes lecture_50kg = 103000
precision=0.01                          #precision souhaitée pour valider l'acquisition d'une mesure
delai_avant_acquisition=0.1      #on attend delai avant de lancer les mesures par le HX
tempo_lora_demarrage = 0.1    #le temps que la carte lora soit opérationnelle
tempo_lora_emission =0.1         #le temps que la carte lora finisse l'émission
nombre_point=3                        #c'est le nombre d'acquisitions faites par le HX711, qui en fait une moyenne appelée mesure

w='ruche_a448'                    #champ réservé usage ultérieur, libre
label='label'                        #champ de controle expéditeur sur label
delimiteur='d'                       #champ delimiteur entre champs de la trame, ne pas utiliser d dans les autres champs!!!

GAIN_distant=0.80                                                                  #paramètres de mesure de la température : à régler pour chaque Arduino
OFFSET_distant=314                                                               #paramètres de mesure de la température : à régler pour chaque Arduino
GAIN_local=1.22                                                                      #paramètres de mesure de la température : à régler pour chaque Arduino
OFFSET_local=318                                                                   #paramètres de mesure de la température : à régler pour chaque Arduino

# TTN Node IDs
DEV_EUI = '70B3D5499390A31C'
APP_EUI = '70B3D57ED0007FAD'
APP_KEY = '2455433205F12974AB5629B85490D79F'

# Debug
DEBUG_LED = True
DEBUG_CON = True

# LoRa setup
LORA_FREQUENCY = 863000000
LORA_DR = 5   # DR_5
PKT_PREFIX = b'W '   # Prefix of each packet
SLEEP_MAIN = 60        # Sleep time in packet send

# Low Energy config
DIS_WIFI = True
DIS_BLE = True
HEARTBEAT = False

# LED color
LED_OFF = 0x000000
GREEN = 0x007f00
YELLOW = 0x7f7f00
RED = 0x7f0000
BLUE = 0x00007f

#deepsleep en millisecondes
sleep=600000

