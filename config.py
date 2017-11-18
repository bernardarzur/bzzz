# HX711_1
# brochage HX vers Lopy    pour le 20 kg ->Blanc pin#DOUT, Jaune pin#SCK, Noir   pin#GRND et Rouge pin#5 volts -MAJ 3 avril 2017
#brochage HX vers jauge 20kg ->Noir E-, Rouge E+, Vert  A+, Blanc A-  module 182409353771
HX_DT_1 = 'P21'
HX_SCK_1 = 'P22'
# HX711_2
HX_DT_2 = 'P1'
HX_SCK_2 = 'P2'
nombre_capteurs=6                 #nombre de capteurs sur la balance
tare_20kg = [-44450,95900,-95950, -95950, -95950, -95950  ] # tare 20kg_xx : valeur ADC sans rien sur le capteur le 04/04/2017 
valeur_20kg =[478650, 613000,408200, 613500, 613500, 613500 ]  # etalonnage 20kg_1: valeur ADC avec l'étalon sur le capteur
etalon_20kg = 5202                 # etalonnage 20kg_1: poids de l'étalon en grammes
delai_avant_acquisition=0.1     #on attend delai avant de lancer les mesures par le HX
tempo_lora_demarrage = 1      #le temps que la carte lora soit opérationnelle
tempo_lora_emission = 3          #le temps que la carte lora finisse l'émission
nombre_point=10                     #c'est le nombre d'acquisitions faites par le HX711, qui en fait une moyenne appelée mesure
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
