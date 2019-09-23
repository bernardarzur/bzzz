#accompagne main_RX_v_18

w='RX_34b0'                                        #nom de la ruche, ou identifiant TTN, Lopy_d74e
date=[2019, 9, 20 ,10, 30, 0, 0, 0]          # On met RX à l'heure, ne sert pas pour les TX, [aaaa,m,j,h,mn,s,ms,0], car lors du passage en deepsleep, TX perd la date?
timeout=60000*20                                 # timeout  en millisecondes ; 60000 millisecondes font une minute
delai_flash_mise_en_route=0.02
sleep    =60000*10                                        #deepsleep en millisecondes
delai_local=2 
label='label'                            #champ de controle expéditeur sur label
delimiteur='d'                           #champ delimiteur entre champs de la trame, ne pas utiliser d dans les autres champs!!!

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



