# HX711_1
# brochage HX vers Lopy    pour le 20 kg ->Blanc pin#DOUT, Jaune pin#SCK, Noir   pin#GRND et Rouge pin#5 volts -MAJ 3 avril 2017
#brochage HX vers jauge 20kg ->Noir E-, Rouge E+, Vert  A+, Blanc A-  module 182409353771
#GND ->P25  et 3.3Volts ->P24
HX_DT_1    = 'P18'#P18 a P13 sont des INPUT
HX_SCK_1  = 'P23'
# HX711_2
HX_DT_2    = 'P17'
HX_SCK_2  = 'P22'
# HX711_3
HX_DT_3    = 'P15'#la P16 sert pour tension batterie?
HX_SCK_3  = 'P21'
# HX711_4
HX_DT_4    = 'P14'
HX_SCK_4  = 'P20'
# HX711_5
HX_DT_5     = 'P13'
HX_SCK_5   = 'P19'
# HX711_6
HX_DT_6    = 'P11'#P10 sert aussi a SPIO CLK et P11 a SPIO MOSI 
HX_SCK_6  = 'P10'
nombre_capteurs=6                 #nombre de capteurs sur la balance
tare_20kg = [-232000,0,69060, -110000, 40470, 72660  ] # tare 20kg_xx : valeur ADC sans rien sur le capteur le 03/12/2017 (n°0_B)
valeur_20kg =[437500, 670900,755500, 551000, 719900, 766150 ]  # etalonnage 20kg_1: valeur ADC avec l'étalon sur le capteur
etalon_20kg = 6930                 # etalonnage 20kg_1: poids de l'étalon en grammes
mesure_20kg=[0, 0, 0, 0, 0, 0]
lecture_capteur=[0, 0, 0, 0, 0, 0,]

delai_avant_acquisition=0.1     #on attend delai avant de lancer les mesures par le HX
delai_local=3     #on attend delai local avant de lancer une mesure
tempo_lora_demarrage = 1      #le temps que la carte lora soit opérationnelle
tempo_lora_emission = 1          #le temps que la carte lora finisse l'émission
nombre_point=10                   #c'est le nombre d'acquisitions faites par le HX711, qui en fait une moyenne appelée mesure
b_mesure_par_cycle = 3           #on fait "b_mesure_par_cycle"  mesures et on envoie "b_mesure_par_cycle" trames avec le même n° "numero de trame" sur le champ numero_trame

label='label'                        #controle expéditeur sur label
delimiteur='d'                       #delimiteur entre champs de la trame
numero_trame=0                    #controle expéditeur sur n° trame
lecture=0                                #mode sans lecture par défaut
a_max=1                                 #affichage port serie a est le nb max de mesures par ligne, 
a=1                                          #affichage port serie a est le nb  de mesures par ligne, 
b=0                                          #b est le nombre total de mesures

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
LORA_FREQUENCY = 868100000
LORA_DR = 5   # DR_5

# Prefix of each packet
PKT_PREFIX = b'W '

# Sleep time in packet send
SLEEP_MAIN = 60

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


#deepsleep
sleep=10
WPUA_ADDR = (0x09)
OPTION_REG_ADDR = (0x0E)
IOCAP_ADDR = (0x1A)
IOCAN_ADDR = (0x1B)

WAKE_STATUS_ADDR = (0x40)
MIN_BAT_ADDR = (0x41)
SLEEP_TIME_ADDR = (0x42)
CTRL_0_ADDR = (0x45)

EXP_RTC_PERIOD = (7000)
