#accompagne TX_v_18

w='bzz8'                                              #nom de la ruche ou du RX,  circuit PROTO 5 : quatre hx711 (n°13 à 16), Lopy4_4ad8,, attention P18, P17 et P10 ne sont pas cablées sur le lopy
date=[2019, 9, 2 ,9, 45, 0, 0, 0]       # On met RX à l'heure, ne sert pas pour les TX, [aaaa,m,j,h,mn,s,ms,0], car lors du passage en deepsleep, TX perd la date?
sleep    =60000*10                                        #deepsleep en millisecondes
timeout=60000*1                                      # 60000 millisecondes font une minute
delai_local=10                                        #on attend delai local SECONDES avant de lancer une mesure, doit être inférieure à timeout
delai_flash_mise_en_route=0.04
tempo_lora_demarrage = 0    #le temps en secondes que la carte lora soit opérationnelle
tempo_lora_emission = 0        #le temps en secondes que la carte lora finisse l'émission
delai_avant_acquisition= 0      #on attend delai secondes avant de lancer les mesures par le HX  

#brochage HX vers jauge 20kg ->Noir E-, Rouge E+, Vert  A+, Blanc A-  module 182409353771
HX_DT_1    = 'P19'# brochage HX vers Lopy : ne pas utiliser P12 qui sert pour les reboots ni P2,#P18 a P13 sont des INPUT, LoRa utilise  P5, P6, P7 : ne pas utiliser, P16 sert pour la batterie,
HX_SCK_1  = 'P23'
HX_DT_2    = 'P8'
HX_SCK_2  = 'P22'
HX_DT_3    = 'P15'
HX_SCK_3  = 'P20'
HX_DT_4    = 'P13'
HX_SCK_4  = 'P21'

pinBatt='P16'# mesure TENSION BATTERIE attenuation = 0 correspond à 1000mV, attn=1  à 3dB attn=2 à 6dB, attn=3 à 12 dB, pont diviseur (115k et 56k) sur expansion board V2.1A, 
resolutionADC=4096#10 bits sur Lopy1 : 1024,  12 bits sur Lopy4 : 4096
attn=1
range=10**(3/20)*1000# 1412 pour 3 dB
coeff_pont_div=(470+221)/221 

nombre_capteurs=4                     #nombre de capteurs sur la balance TX, de 1 à 4 dans notre balance n°1
premier_capteur =0                     #indice du premier capteur TX
#indice        0               1             2             3              4             5            6            7             8          9           10        11        12         13             14         15        16
tare =    [-159327,-96885,  -29883,  66287]       # tare  : valeur ADC sans rien sur le capteur  
valeur =[ 503667 ,593906 ,660713,753035 ]  # etalonnage : valeur ADC avec l'étalon sur le capteur
etalon =[ 6930 ,   6930 ,    6930,    6930      ]               #  poids de l'étalon en grammes
coeff=   [0]*4
i=0
for g in tare:
    coeff[i] =   etalon[i] /(valeur[i] -tare[i]  )        #  coeff corrigé de la tare ADC, avec l'étalon sur le capteur, normée au poids, gramme/digit# poids_en_gr=((lecture_capteur[i]-tare[i])*mesure[i])
    i+=1

# en position 13 à 16 ::: capteurs 20 kg_i : mesures du 1 septembre 2019
precision=0.01                            #precision souhaitée pour valider l'acquisition d'une mesure
nombre_point=5                         #c'est le nombre d'acquisitions faites par le HX711, qui en fait une moyenne appelée mesure

label='label'                            #trame : champ de controle expéditeur sur label
delimiteur='d'                           #trame : champ delimiteur entre champs de la trame, ne pas utiliser d dans les autres champs, nom de la ruche entre autres!!!

LORA_FREQUENCY = 863000000       #parametres RAW
data_rate=5                                       # set the LoRaWAN data rate DR_5

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



