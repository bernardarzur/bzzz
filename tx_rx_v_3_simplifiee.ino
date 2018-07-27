/****************************************************************************VERSIONS********************************************************************************
version V1 : y a le local capteur et le distant, on peut tester en local (sans lora), on enregistre sur eeprom un des deux capteurs; v2 -> deux capteurs locaux et un distant; v3 -> corrige gros
bug : il faut faire une pseudo-mesure avant de démarrer, bof, finalement on fait moyenne de 100 mesures, v4-> temperature et label, v5-> deux capteurs dans le distant (poids = somme des deux)
v6-> on rajoute un capteur local aux deux distants (v5 ne marche plus) puis versions tx_rx_v1: on y met les deux, ainsi que la lecture; version tx_rx_v2 : config 4 capteurs 20kg; 
version tx_rx_v3 : on fait un cycle de mesures sur n points, b fois de suite en envoyant un numéro de trame sauvé sur EEPROM TX (on s'est aperçu qu'on perdait bcp de trames) et en mars 2018, on rajoute
config 1014 et 2014 en nombre "long" sur 4 octets et config 10145 et 20145 en nombre "int" sur 2 octets pour mieux remplir l'eeprom
version enregistreur_température en juin 2018 pour mesurer et enregistrer des températures : case 100 et 300
version tx_rx_v3_simplifiee 
*************************************************************************************************************************************************************
  
      case 1 : label_rx= 0 ->> ON VA CONFIGURER LE RX, zero     CAPTEUR SUR LE RX, configuration TX selon valeur de label
      case 1 : label_rx= 41 ->> ON VA CONFIGURER LE RX, UN SEUL CAPTEUR SUR LE RX, configuration TX selon valeur de label
      case 1 : label_rx= 42 ->> ON VA CONFIGURER LE RX, DEUX   CAPTEURS SUR LE RX, configuration TX selon valeur de label
      case 1 : label_rx= 44 ->> ON VA CONFIGURER LE RX, QUATRE CAPTEURS SUR LE RX,configuration TX selon valeur de label
      case 1 : label= 0 ->> ON VA CONFIGURER LE RX, zero     CAPTEUR SUR LE TX, configuration RX selon valeur de label_rx      
      case 1 : label= 41 ->> ON VA CONFIGURER LE RX; il y a x capteurs sur le RX; il y a 1 capteur sur le TX; TX transmet valeur brute ADC; la trame reçue fait 7 octets  :  2 [label]+1 [T]+4 [1 long]
      case 1 : label= 1 ->>ON VA CONFIGURER LE RX; il y a x capteurs sur le RX; il y a x capteurs sur le TX, TX calcule poids total en g qu'on recoit sur RX; la trame fait 5 octets : 2 [label/num trame]+1 [T]+2 [1 int]
      case 1 : label= 11 ->>ON VA CONFIGURER LE RX; il y a x capteurs sur le RX; il y a x capteurs sur le TX, TX calcule poids total en g qu'on recoit sur RX;la trame fait 7 octets : 2 [label/num trame]+1 [T]+4 [1 long]
      case 1 : label= 44 ->>ON VA CONFIGURER LE RX; il y a x capteurs sur le RX; il y a 4 capteurs sur le TX; la trame reçue fait 19 octets : 2 [label]+1 [T]+16 [4 long]
      
      case 2 : label= 1  ->>  ON VA CONFIGURER LE TX; il y a 4 capteurs sur le TX mais on ne renvoie que la somme en grammes (INT); la trame émise fait 5 octets  : 2 [label]+1 [T]+2 [1* int]
      case 2 : label= 11 ->>  ON VA CONFIGURER LE TX; il y a 4 capteurs sur le TX mais on ne renvoie que la somme en grammes (LONG); la trame reçue fait 7 octets : 2 [label/trame]+1 [T]+4 [1 long]
      case 2 : label= 41 ->>  ON VA CONFIGURER LE TX;  il y a 1 capteur sur le TX; la trame émise (valeur ADC) fait 7 octets  : 2 [label]+1 [T]+4 [1* long]
      case 2 : label= 42 ->>  ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a 2 capteurs sur le TX; la trame émise fait 11 octets : 2 [label]+1 [T]+8 [2 long]
      case 2 : label= 44 ->>  ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a 4 capteurs sur le TX; la trame émise fait 19 octets : 2 [label]+1 [T]+16 [4 long]
      
      case 3 : label= x, label_rx=y ->>ON VA LIRE L'EEPROM selon la valeur de label et de label_rx
      case 30 : ->>ON VA LIRE L'EEPROM octet par octet
      case 100 : label= 1 ->> RX SEULEMENT PAS DE TX , 0 CAPTEUR SUR LE RX, ON VA CONFIGURER LE RX    ; MESURE TEMPERATURE SEULE ET ENREGISTREMENT, seul cas de RX où on met l'Arduino en sommeil      
      case 300 : label= 1 ->> ON VA LIRE L'EEPROM; il y a 0 capteur sur le RX; il y a 0 capteur  sur le TX;la trame EEPROM fait  1 octet pour mesurer la temperature : 1 [T] 
      
*///_______________________________________________________________________________________________________________________________________________________________________________________
int  configuration =1; //  Choisir une configuration: 1er chiffre 1->configuration RX, 2->configurationTX, 3->lecture EEPROM                                                               |
//  |______________________________________________________________________________________________________________________________________________________________________________________|

byte label_rx=0;//configuration RX, type de mesure du RX ;  41 ou 42 -> on lit un ou deux ADC sur 4 octets; 44 -> on lit 4 ADC sur 4 octets; 0 -> rien sur le RX;
byte label=11;//configuration TX, controle type de trame expéditeur;  41 ou 42 ou 44-> on lit un ou deux ou quatre ADC sur 4 octets; 1 -> on lit un calcul sur 2 octets; 11-> on lit un calcul sur 4 octets;

int eeprom=1;              //1 si on veut sauvegarder les mesures sur EEPROM du RX, 0 sinon
int economiseur=1;         //1 si on veut utiliser la carte économiseur (active la fonction miseEnSommeil). fonction TX en principe
byte debug=1;              //activation sortie série pour le TX, si debug à 1
int nombre_point=10;       //c'est le nombre d'acquisitions faites par le HX711, qui en fait une moyenne appelée mesure
byte b_mesure_par_cycle = 3;  //on fait "b_mesure_par_cycle"  mesures et on envoie "b_mesure_par_cycle" trames avec le même n° "numero_trame" sur l'octet 3eme, fonction TX en principe
long tempo_local=3000;      //tempo entre deux mesures si capteur local seulement, sinon c'est le distant qui pilote, fonction RX en principe



int pin_reed = 9;          // commande Relais Reed pour couper l'alimentation du Arduino sur le TX, ou le RX si on est en mode local économe (sans PC)
int tempo_decharge_capa_eco = 1000;     //temps de décharge de la capa économiseur (mini 300ms)
int tempo_lora_demarrage = 1000;        //le temps que la carte lora soit opérationnelle
int tempo_lora_emission = 3000;         //le temps que la carte lora finisse l'émission


#include "EEPROM.h"
int EEPROM_LENGTH=1024;     // l'adresse de la dernière sauvegarde est sauvée sur les 2 premiers octets de l'EEprom (0 et 1),on peut donc lire/écrire jusqu'à 1022 octets
int address = 2;            //adresse pour sauver une trame de données sur l'eeprom RX, on démarre à 2 pour les ecritures
int read_addr = 2;          //adresse pour lire les données sur eeprom, on démarre à 2 pour les lectures
byte premier_octet=3;       //premier octet de lecture_capteur_1 sur la trame reçue, le zero est le label, le 1 le numero trame, le 2 la temperature
byte octet_par_trame_max=19; //c'est la longueur de trame la plus longue de tous les "cases" programmés, elle sert à programmer les deux tableaux data et data_rcv
byte numero_trame=0;
byte eeprom_1023=0;
byte lecture=0;//mode sans lecture par défaut
byte a_max=1;//affichage port serie a est le nb max de mesures par ligne, 
byte a=1;//affichage port serie a est le nb  de mesures par ligne, 
byte b=0;//b est le nombre total de mesures
byte octet_par_trame=1;
byte octet_gestion_trame=0;
byte l=4;                  //nombre d'octets par mesure envoyée sur LoRa, si c'est un long, l=4,  
long lecture_capteur = 0;
long lecture_capteur_1 = 0;
long lecture_capteur_2 = 0;
long lecture_capteur_3 = 0;
long lecture_capteur_4 = 0;
float temp_TX=0;
float temp_RX=0;
float poids_en_grammes=0;        
float poids_en_gr_total=0;
float poids_en_gr_local=0; 
float poids_en_gr_distant=0;
int   poids_int=0;//permet de ramener la mesure sur deux octets pour réduire mémoire sur EEPROM (l=2 dans ce cas, config 2014)
long  poids_long=0;//permet de ramener la mesure sur 4 octets pour le passer au shield

#include "HX711.h"
//HX711 capteur_machin  (DOUT, SCK);EXEMPLES : HX711.DOUT- pin #A1  et  HX711.PD_SCK-  pin #A0 ->HX711 capteur_machin(A1, A0)
HX711 capteur_10kg(A1, A0);//HX711.DOUT- pin #A1  et  HX711.PD_SCK-  pin #A0 
HX711 capteur_30kg(A3, A2);//HX711.DOUT- pin #A1  et  HX711.PD_SCK-  pin #A0 
HX711 capteur_20kg_1(A3, A2);//HX711.DOUT- pin #A1  et  HX711.PD_SCK-  pin #A0 
HX711 capteur_20kg_2(A5, A4);//HX711.DOUT- pin #A1  et  HX711.PD_SCK-  pin #A0 
HX711 capteur_20kg_3(2, 3);//HX711.DOUT- pin #A1  et  HX711.PD_SCK-  pin #A0 
HX711 capteur_20kg_4(A1, A0);//HX711.DOUT- pin #A1  et  HX711.PD_SCK-  pin #A0 
HX711 capteur_50kg(A1, A0);//HX711.DOUT- pin #A1  et  HX711.PD_SCK-  pin #A0 
// brochage HX vers Arduino    pour le 50 kg ->Blanc pin#DOUT, Jaune pin#SCK, Marron pin#GRND et Vert  pin#5 volts -MAJ 14 mars 2017
// brochage HX vers Arduino    pour le 30 kg ->Blanc pin#DOUT, Jaune pin#SCK, Noir   pin#GRND et Rouge pin#5 volts -MAJ 14 mars 2017
// brochage HX vers Arduino    pour le 20 kg ->Blanc pin#DOUT, Jaune pin#SCK, Noir   pin#GRND et Rouge pin#5 volts -MAJ 3 avril 2017
// brochage HX vers Arduino    pour le 10 kg ->Blanc pin#DOUT, Jaune pin#SCK, Marron pin#GRND et Vert  pin#5 volts -MAJ 14 mars 2017
//brochage HX vers jauge 50kg ->Marron E-, Blanc E+, Vert A+, Jaune A-
//brochage HX vers jauge 10kg ->jauneE-, brunE+, vertA-, blancA+ (attention marqué inverse sur capteur)
//brochage HX vers jauge 20kg ->Noir E-, Rouge E+, Vert  A+, Blanc A-  module 182409353771
//brochage HX vers jauge 30kg ->Noir E-, Rouge E+, Jaune A+, Blanc A-
const int   delai_avant_acquisition=100;//on attend delai avant de lancer les mesures par le HX
const float tare_20kg_1 = -44450; // tare 20kg_1 : valeur ADC sans rien le 04/04/2017
const float etalon_20kg_1 = 5202; // etalonnage 20kg_1: poids de l'étalon en grammes
const float mesure_20kg_1 = 478650 -tare_20kg_1; // etalonnage 20kg_1: valeur ADC avec l'étalon sur la balance moins la tare
const float tare_20kg_2 = 95900; // tare 20kg_1 : valeur ADC sans rien le 04/04/2017
const float etalon_20kg_2 = 5202; // etalonnage 20kg_1: poids de l'étalon en grammes
const float mesure_20kg_2 = 613000 -tare_20kg_2; // etalonnage 20kg_1: valeur ADC avec l'étalon sur la balance moins la tare
const float tare_20kg_3 = -95950; // tare 20kg_1 : valeur ADC sans rien le 04/04/2017
const float etalon_20kg_3 = 5202; // etalonnage 20kg_1: poids de l'étalon en grammes
const float mesure_20kg_3 = 408200 -tare_20kg_3; // etalonnage 20kg_1: valeur ADC avec l'étalon sur la balance moins la tare
const float tare_20kg_4 = 95950; // tare 20kg_1 : valeur ADC sans rien le 04/04/2017
const float etalon_20kg_4 = 5202; // etalonnage 20kg_1: poids de l'étalon en grammes
const float mesure_20kg_4 = 613500 -tare_20kg_4; // etalonnage 20kg_1: valeur ADC avec l'étalon sur la balance moins la tareconst float tare_30kg = 203000; // tare 30kg: valeur ADC sans rien le 23/01/2017
const float tare_30kg = 188850; // tare 30kg: valeur ADC sans rien le 15/04/2017
const float etalon_30kg = 5202; // etalonnage 30kg: poids de l'étalon en grammes
const float mesure_30kg = 723000-tare_30kg; // etalonnage 30kg: valeur ADC avec l'étalon sur la balance moins la tare
const float tare_50kg = 420000;//lecture du capteur pedale sans rien dessus le 23/01/2017
const float etalon_50kg = 5202;//poids de l'étalon pedale en grammes
const float mesure_50kg = 559000-tare_50kg;//mesure du poids de l'étalon pedale en tenant compte de la tare
const float tare_10kg = 279600;//lecture du capteur 10kg_leny sans rien dessus le 23/01/2017
const float etalon_10kg = 5202;//poids de l'étalon 10kg_leny en grammes
const float mesure_10kg = 1886000-tare_10kg;//mesure du poids de l'étalon 10kg_leny en tenant compte de la tare, = lecture - tare
const float GAIN_distant=0.400;//paramètres de mesure de la température : à régler pour chaque Arduino, ici c'est le numero Nano I
const float OFFSET_distant=313.18;//paramètres de mesure de la température : à régler pour chaque Arduino
const float GAIN_local=1.22;//paramètres de mesure de la température : à régler pour chaque Arduino
const float OFFSET_local=314;//paramètres de mesure de la température : à régler pour chaque Arduino

#include <SPI.h> //Circuit: SS:   pin 10 // the other you need are controlled by the SPI library):MOSI: pin 11  Handled by SPI.H MISO: pin 12 Handled by SPI.H SCK:  pin 13 Handled by SPI.H
const int CS = 10; // SS already defined by SPI conflicts with same pin nr 10 :)//#define SLAVESELECT 10//ss
const int pin_paquet_recu = 9; // commande led quand on est en train de recevoir un paquet LORA
const int pin_x_paquet_recu = 8; // commande led quand on a reçu au moins un paquet LORA
#define ARDUINO_CMD_AVAILABLE 0x00// Arduino commands
#define ARDUINO_CMD_READ      0x01
#define ARDUINO_CMD_WRITE     0x02
#define ARDUINO_CMD_TEST      0x03 

const int wait_time_us_between_spi_msg   = 200;// Minimum wait time between SPI message: 160 us
const int wait_time_us_between_bytes_spi =  20;//Minimum wait time between two bytes in a SPI message: 15 us
int previous_cmd_status;
int shield_status;
int available_msb;
int available_lsb;
int available;


void setup() {
  Serial.begin(9600);
 
  pinMode(CS, OUTPUT); // we use this for SS pin // start the SPI library:
  pinMode(pin_reed, OUTPUT); // we use this for pin_reed
  digitalWrite(pin_reed,LOW); 
 
  SPI.begin();  // wake up the SPI bus.
  SPI.setClockDivider(SPI_CLOCK_DIV32) ; // 16MHz/32 = 0.5 MHz
  SPI.setDataMode(SPI_MODE0);  // By Default SPI_MODE0, we make this fact explicit.
  SPI.setBitOrder(MSBFIRST);   // By Default MSBFIRST,  we make this fact explicit.
  delay(100);
 
}


void loop() {
  int transmission=0;
  byte data[octet_par_trame_max]= {};
  byte data_rcv[octet_par_trame_max]= {};
  byte buf[octet_par_trame_max] = {};

  switch (configuration) {
    
    case 100 : // RX SEULEMENT PAS DE TX , 0 CAPTEUR SUR LE RX, ON VA CONFIGURER LE RX    ; MESURE TEMPERATURE SEULE ET ENREGISTREMENT
    while (1){
      delay (tempo_local);//tempo des cycles d'acquisitions pilotée en local
      transmission=1 ;//la transmission est déclarée bonne puisqu'il n'y en a pas!
      octet_par_trame=1;
      octet_gestion_trame=0;
      address= adresseCourante();//adresse d'une trame EEPROM, On la lit sur les 2 premiers octets EEPROM
      temp_RX        =temperatureArduino(GAIN_local,OFFSET_local)/2.5-30;//la fonction temperatureArduino amplifie la valeur (pour garder de la précision et du positif, on ne transmet qu'un byte)
      temp_TX      =temperatureArduino(GAIN_local,OFFSET_local);
      if (debug) {Serial.print("Température RX: ");Serial.print(temp_RX);Serial.print("*Température TX:  ");Serial.print(temp_TX);Serial.print("*");}
      data_rcv[0]=temp_TX; 

       if (eeprom) {
           address=sauverEeprom( address,data_rcv , octet_par_trame, octet_gestion_trame);//on sauve la température distante sur octet_par_trame moins octet_gestion à partir de l'adresse "address" puis 
           //la fonction sauver met à jour l' adresse de sauvegarde, que l'on écrit sur les octets 1 et 2 de l'ee
      EEPROM.write (0, (address>>8) & 0xFF);//on sauve la prochaine @ sur octets 0 & 1, puisqu'on coupe l'arduino
      EEPROM.write (1, address & 0xFF);
      if (debug) { Serial.print(" adresse: ");Serial.println(address); }
                    }
      miseEnSommeil(); //eteint Arduino
              }
         break;
      
      


      
    case 1 : // RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteurs sur le RX(label_RX=0); il y a x capteurs (sous-capteurs) sur le TX, on calcule poids total en g et on envoie comme un seul capteur 
    //(label 1 ou 11); trame reçue= 5/7 octets : 2 [label/num trame]+1 [T]+2/4 [1 int ou un long]; on peut envoyer valeur ADC : label 41/42/44 et on calcule le poids sur le RX, trame reçue=7/11/19 oct
  if (label!=0){//si label =0, il n'y a pas de distant
      available = checkifAvailableRXData() ;//on regarde si il y a des paquets LoRa en attente
      octet_gestion_trame=2;
      eeprom_1023 = EEPROM.read(1023);
      while (!available){
        available = checkifAvailableRXData() ;
        delay (100);
      }
      readAvailableRXData(data_rcv , available);
      if (data_rcv[premier_octet-3]==label)      {//vérification octet premier  pour controle destinataire, et controle n° trame pour prendre une seule mesure
       transmission=1 ;//transmission déclarée OK 
       numero_trame                    =data_rcv[premier_octet-2];//octet deuxieme
       temp_TX                         =(data_rcv[premier_octet-1]/2.5-30);//octet troisieme
       temp_RX                         =temperatureArduino(GAIN_local,OFFSET_local)/2.5-30;       
          if (data_rcv[premier_octet-3]==1){ //on regarde le type de valeur sur le label, 1 -> on lit directement un calcul sur 2 octets
              lecture_capteur_1        =lectureInt( premier_octet, data_rcv);                     
              octet_par_trame=5;                         
              poids_en_gr_distant=lecture_capteur_1;
          }          
          if (data_rcv[premier_octet-3]==11){ //on regarde le type de valeur sur le label, 11 -> on lit directement un calcul sur 4 octets
             lecture_capteur_1        =lectureLong( premier_octet, data_rcv);      
             octet_par_trame=7;                         
             poids_en_gr_distant=lecture_capteur_1;
          }       
          if (data_rcv[premier_octet-3]==41){ //on regarde le type de valeur sur le label, 41 -> on lit un ADC sur 4 octets             
              lecture_capteur_1        =lectureLong( premier_octet, data_rcv);
              octet_par_trame=7;                          
              poids_en_gr_distant=((lecture_capteur_1-tare_30kg)/mesure_30kg*etalon_30kg);//on calcule le poids en fonction des parametres capteur
          }
          if (data_rcv[premier_octet-3]==44){ //on regarde le type de valeur sur le label, 44 -> on lit 4 ADC sur 4 octets*4
              octet_par_trame=19;                         
              lecture_capteur_1        =lectureLong( premier_octet, data_rcv);
              poids_en_gr_distant      =((lecture_capteur_1-tare_20kg_1)/mesure_20kg_1*etalon_20kg_1);Serial.print(" n°1 ");Serial.print(poids_en_gr_distant);
              lecture_capteur_2        =lectureLong( premier_octet+l, data_rcv);
              poids_en_gr_distant      =((lecture_capteur_2-tare_20kg_2)/mesure_20kg_2*etalon_20kg_2);Serial.print(" n°2 ");Serial.print(poids_en_gr_distant);
              lecture_capteur_3        =lectureLong( premier_octet+2*l, data_rcv);
              poids_en_gr_distant      =((lecture_capteur_3-tare_20kg_3)/mesure_20kg_3*etalon_20kg_3);Serial.print(" n°3 ");Serial.print(poids_en_gr_distant);
              lecture_capteur_4        =lectureLong( premier_octet+3*l, data_rcv);
              poids_en_gr_distant      =((lecture_capteur_4-tare_20kg_4)/mesure_20kg_4*etalon_20kg_4);Serial.print(" n°4 ");Serial.print(poids_en_gr_distant);
              poids_en_gr_distant      =((lecture_capteur_1-tare_20kg_1)/mesure_20kg_1*etalon_20kg_1)+((lecture_capteur_2-tare_20kg_2)/mesure_20kg_2*etalon_20kg_2)+((lecture_capteur_3-tare_20kg_3)/mesure_20kg_3*etalon_20kg_3)+((lecture_capteur_4-tare_20kg_4)/mesure_20kg_4*etalon_20kg_4);
              Serial.print(" poids en gr distant: ");Serial.print(poids_en_gr_distant);
          }

       Serial.print(" Temp RX: ");Serial.print(temp_RX);Serial.print(" Temp TX: ");Serial.print(temp_TX);Serial.print (" label: ");Serial.print(label);Serial.print (" label_rx: ");Serial.print(label_rx);Serial.print (" trame: ");Serial.print(numero_trame);Serial.print(" poids en gr distant: ");Serial.print(poids_en_gr_distant);
       if   (numero_trame - eeprom_1023>1)
          {//si la différence est supérieure à 1, il y a des trames perdues
            Serial.print (" perte trames: "); Serial.println((data_rcv[1]- (EEPROM.read(1023))));
          }   
       if ((eeprom)&&(numero_trame!=eeprom_1023))//on ne sauvegarde que la première trame si on fait b mesures successives sur le TX, attention à sauvergarde si label_rx#0...
          { 
           address=sauverEeprom( address,data_rcv , octet_par_trame, octet_gestion_trame);//on sauve la température distante sur octet_par_trame moins octet_gestion à partir de l'adresse "address" puis 
           //la fonction sauver met à jour la nouvelle adresse de sauvegarde, que l'on écrit sur les octets 1 et 2   
           EEPROM.write (1023, numero_trame);//on écrit le nouveau numero de trame   
          }    
      }
          else {
           Serial.println ("erreur transmission");
           Serial.print (" data0: "); Serial.println(data_rcv[0]);Serial.print (" label: ");Serial.println(label);
           }
  }           

      
if (label_rx!=0){// il y a x capteurs sur le RX(label_RX#0);  on calcule poids total en g; trame = 4/8/16 octets : 4/8/16 (un/deux/quatre long]; label_RX= 41/42/44 et on calcule le poids en grammes
       
          delay (tempo_local);//tempo des cycles d'acquisitions si pilotée en local (label=0)
          if (label_rx==41){ //on regarde le type de valeur sur le label, 41 -> on lit un ADC sur 4 octets             
              octet_par_trame=4;             
              lecture_capteur_1=acquisitionCapteur20kg_1(tare_20kg_1,mesure_20kg_1,etalon_20kg_1,nombre_point);//fait l'acquisition sur le capteur n°1-20 kg sur une moyenne de nombre_point                                             
              poids_en_gr_local=((lecture_capteur_1-tare_30kg)/mesure_30kg*etalon_30kg);//on calcule le poids en fonction des parametres capteur
                      if (eeprom) {
                           address=sauverEntier(address, lecture_capteur_1);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
                       }
          }
          if (label_rx==42){ //on regarde le type de valeur sur le label, 42 -> on lit 2 ADC sur 4 octets*2
              octet_par_trame=8;              
              lecture_capteur_1=acquisitionCapteur20kg_1(tare_20kg_1,mesure_20kg_1,etalon_20kg_1,nombre_point);//fait l'acquisition sur le capteur n°1-20 kg sur une moyenne de nombre_point                                             
              poids_en_gr_local      =((lecture_capteur_1-tare_20kg_1)/mesure_20kg_1*etalon_20kg_1);Serial.print(" n°1 ");Serial.print(poids_en_gr_local);
                      if (eeprom) {
                           address=sauverEntier(address, lecture_capteur_1);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
                       }              
              poids_en_gr_local      =((lecture_capteur_2-tare_20kg_2)/mesure_20kg_2*etalon_20kg_2);Serial.print(" n°2 ");Serial.print(poids_en_gr_local);
                      if (eeprom) {
                           address=sauverEntier(address, lecture_capteur_2);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
                       }              
          }

          if (label_rx==44){ //on regarde le type de valeur sur le label, 44 -> on lit 4 ADC sur 4 octets*4
              octet_par_trame=16;              
              lecture_capteur_1=acquisitionCapteur20kg_1(tare_20kg_1,mesure_20kg_1,etalon_20kg_1,nombre_point);//fait l'acquisition sur le capteur n°1-20 kg sur une moyenne de nombre_point                                             
              poids_en_gr_local      =((lecture_capteur_1-tare_20kg_1)/mesure_20kg_1*etalon_20kg_1);Serial.print(" n°1 ");Serial.print(poids_en_gr_local);
                      if (eeprom) {
                           address=sauverEntier(address, lecture_capteur_1);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
                       }              
              poids_en_gr_local      =((lecture_capteur_2-tare_20kg_2)/mesure_20kg_2*etalon_20kg_2);Serial.print(" n°2 ");Serial.print(poids_en_gr_local);
                      if (eeprom) {
                           address=sauverEntier(address, lecture_capteur_2);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
                       }              
              poids_en_gr_local      =((lecture_capteur_3-tare_20kg_3)/mesure_20kg_3*etalon_20kg_3);Serial.print(" n°3 ");Serial.print(poids_en_gr_local);
                      if (eeprom) {
                           address=sauverEntier(address, lecture_capteur_3);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
                       }              
              poids_en_gr_local      =((lecture_capteur_4-tare_20kg_4)/mesure_20kg_4*etalon_20kg_4);Serial.print(" n°4 ");Serial.print(poids_en_gr_local);
                      if (eeprom) {
                           address=sauverEntier(address, lecture_capteur_4);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
                       }              poids_en_gr_local      =((lecture_capteur_1-tare_20kg_1)/mesure_20kg_1*etalon_20kg_1)+((lecture_capteur_2-tare_20kg_2)/mesure_20kg_2*etalon_20kg_2)+((lecture_capteur_3-tare_20kg_3)/mesure_20kg_3*etalon_20kg_3)+((lecture_capteur_4-tare_20kg_4)/mesure_20kg_4*etalon_20kg_4);
          }
          
       temp_RX=temperatureArduino(GAIN_local,OFFSET_local)/2.5-30;
       Serial.print(" poids en gr local: ");Serial.print(poids_en_gr_local); Serial.print(" Temp RX: ");Serial.print(temp_RX);Serial.print(" Temp TX: ");           
  
      }
        
      break;


    
  case 2 : // ON VA CONFIGURER LE TX; il y a un ou quatre capteurs sur le TX mais on ne renvoie que la somme en grammes; la trame émise fait 5 ou 7 octets : 2 [label/trame]+1 [T]+1 int ou long
        if (label==1) { 
          octet_par_trame=5;
        }
        if (label==11 || label==41) { 
          octet_par_trame=7;
        }
        if (label==11 || label==42) { 
          octet_par_trame=11;
        }
        if (label==11 || label==44) { 
          octet_par_trame=19;
        }        
       while (b < b_mesure_par_cycle) 
       { //on va envoyer b mesures pour savoir pourquoi la première mesure est fausse, sur capteurs 4 & 3 en particulier
        b+=1;
        poids_en_gr_total = 0;
        delay(tempo_lora_demarrage);//le temps que la carte LoRa se mette en marche
                if (label==1 || label==11) {        
        lecture_capteur_1=acquisitionCapteur20kg_1(tare_20kg_1,mesure_20kg_1,etalon_20kg_1,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        lecture_capteur_2=acquisitionCapteur20kg_2(tare_20kg_2,mesure_20kg_2,etalon_20kg_2,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        lecture_capteur_3=acquisitionCapteur20kg_3(tare_20kg_3,mesure_20kg_3,etalon_20kg_3,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        lecture_capteur_4=acquisitionCapteur20kg_4(tare_20kg_4,mesure_20kg_4,etalon_20kg_4,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        poids_en_gr_total =(lecture_capteur_1-tare_20kg_1)/mesure_20kg_1*etalon_20kg_1+(lecture_capteur_2-tare_20kg_2)/mesure_20kg_2*etalon_20kg_2+(lecture_capteur_3-tare_20kg_3)/mesure_20kg_3*etalon_20kg_3+(lecture_capteur_4-tare_20kg_4)/mesure_20kg_4*etalon_20kg_4;
        poids_long=abs(poids_en_gr_total);//passe sur 4 octets
        poids_int=abs(poids_en_gr_total);//passe sur 2 octets
                }
                if (label==41) {        
        lecture_capteur_1=acquisitionCapteur50kg(tare_50kg,mesure_50kg,etalon_50kg,nombre_point);//fait l'acquisition sur le capteur 50 kg sur une moyenne de nombre_point       
        poids_en_gr_total =(lecture_capteur_1-tare_20kg_1)/mesure_20kg_1*etalon_20kg_1;
                }
        poids_long=abs(poids_en_gr_total);//float passe sur 4 octets
        poids_int=abs(poids_en_gr_total);//float passe sur 2 octets
        data[0] = label; 
        data[1] = EEPROM.read(1023); //numero trame
        data[2] = temperatureArduino(GAIN_distant,OFFSET_distant);//mesure de la température du TX
                if (label==11) { 
        data[3] =  poids_long >> 24; // il faut decomposer poids_long  en ses 4 octets pour les passer au shield LoRa
        data[4] = (poids_long >> 16) & 0xFF;
        data[5] = (poids_long >>  8) & 0xFF;
        data[6] = (poids_long      ) & 0xFF; 
                }                
                if (label==41) { 
        data[3] =  lecture_capteur_1 >> 24; // il faut decomposer lecture_capteur_1  en ses 4 octets pour les passer au shield LoRa
        data[4] = (lecture_capteur_1 >> 16) & 0xFF;
        data[5] = (lecture_capteur_1 >>  8) & 0xFF;
        data[6] = (lecture_capteur_1      ) & 0xFF; 
                }
                if (label==42) { 
        data[3] =  lecture_capteur_1 >> 24; // il faut decomposer lecture_capteur_1  en ses 4 octets pour les passer au shield LoRa
        data[4] = (lecture_capteur_1 >> 16) & 0xFF;
        data[5] = (lecture_capteur_1 >>  8) & 0xFF;
        data[6] = (lecture_capteur_1      ) & 0xFF;                                
        data[7] =  lecture_capteur_2 >> 24; // il faut decomposer lecture_capteur_2  en ses 4 octets pour les passer au shield LoRa
        data[8] = (lecture_capteur_2 >> 16) & 0xFF;
        data[9] = (lecture_capteur_2 >>  8) & 0xFF;
        data[10]= (lecture_capteur_2      ) & 0xFF;
                }  
                if (label==44) { 
        data[3] =  lecture_capteur_1 >> 24; // il faut decomposer lecture_capteur_1  en ses 4 octets pour les passer au shield LoRa
        data[4] = (lecture_capteur_1 >> 16) & 0xFF;
        data[5] = (lecture_capteur_1 >>  8) & 0xFF;
        data[6] = (lecture_capteur_1      ) & 0xFF;                                
        data[7] =  lecture_capteur_2 >> 24; // il faut decomposer lecture_capteur_2  en ses 4 octets pour les passer au shield LoRa
        data[8] = (lecture_capteur_2 >> 16) & 0xFF;
        data[9] = (lecture_capteur_2 >>  8) & 0xFF;
        data[10]= (lecture_capteur_2      ) & 0xFF;
        data[11] =  lecture_capteur_3 >> 24; // il faut decomposer lecture_capteur_2  en ses 4 octets pour les passer au shield LoRa
        data[12] = (lecture_capteur_3 >> 16) & 0xFF;
        data[13] = (lecture_capteur_3 >>  8) & 0xFF;
        data[14] = (lecture_capteur_3     ) & 0xFF; 
        data[15] =  lecture_capteur_4 >> 24; // il faut decomposer lecture_capteur_2  en ses 4 octets pour les passer au shield LoRa
        data[16] = (lecture_capteur_4 >> 16) & 0xFF;
        data[17] = (lecture_capteur_4 >>  8) & 0xFF;
        data[18] = (lecture_capteur_4     ) & 0xFF;        
                }                 
                if (label==1) { 
        data[3] = (poids_int >>  8) & 0xFF;// il faut decomposer poids_int  en ses 2 octets pour les passer au shield LoRa
        data[4] = (poids_int      ) & 0xFF;  
                }                
        if (debug) {Serial.print (" data0: ");Serial.print (data[0]);Serial.print (" data1: ");Serial.print (data[1]);Serial.print (" data2: ");Serial.print (data[2]);Serial.print (" data3: ");
        Serial.print (data[3]);Serial.print (" data4: ");Serial.print (data[4]);Serial.print (" data5: ");Serial.print (data[5]);Serial.print (" data6: ");Serial.print (data[6]);  
        }
        arduinoLoraTXWrite (data,octet_par_trame);
        delay(tempo_lora_emission);
        if (debug) {Serial.print (" Temp: ");Serial.print (data[2]/2.5-30);Serial.print(" trame: ");Serial.print(EEPROM.read(1023));Serial.print (" b: ");Serial.println (b);
        }
       }
      EEPROM.write (1023, data[1] + 1);
      b=0;
      miseEnSommeil(); //eteint Arduino  
      break; 
 
 

case 3 : // RX: ON VA LIRE L'EEPROM; il y a x capteurs sur le RX; il y a x capteurs sur le TX; la trame EEPROM selon label
          octet_par_trame=0;
          if (label==1){ //on regarde le type de valeur sur le label, 1 -> on lit directement un calcul sur 2 octets
              octet_par_trame=3;
            }
          if ((label==11)||(label==41)){ //on regarde le type de valeur sur le label, 11ou 41 -> on lit directement un calcul ou un ADC sur 4 octets
              octet_par_trame=5;
            }          
          if (label==42){ //on regarde le type de valeur sur le label, 11ou 42 -> on lit directement 2 ADC sur 4 octets*2
              octet_par_trame=9;
            }
          if (label==44){ //on regarde le type de valeur sur le label, 11ou 42 -> on lit directement 2 ADC sur 4 octets*2
              octet_par_trame=17;
            }            
              premier_octet=0;
          if (label_rx==41){ //on regarde le type de valeur sur le label, 11ou 42 -> on lit directement 2 ADC sur 4 octets*2
              octet_par_trame=octet_par_trame+4;
            }              
          if (label_rx==42){ //on regarde le type de valeur sur le label, 11ou 42 -> on lit directement 2 ADC sur 4 octets*2
              octet_par_trame=octet_par_trame+8;
            }
          if (label_rx==44){ //on regarde le type de valeur sur le label, 11ou 42 -> on lit directement 2 ADC sur 4 octets*2
              octet_par_trame=octet_par_trame+16;
            }            
      delay (5000);
      lecture=lecture+1;//mode lecture      
      address = adresseCourante();
      read_addr=4;//les octets 0 et 1 sont pris par l'@ courante (fin de tableau)
      if (lecture==1) {
           Serial.print("Addresse: ");Serial.print(address);
              if (address+2+octet_par_trame  > EEPROM_LENGTH){
                 address=1022;
                 Serial.print("débordement eeprom");
              }
           Serial.println("");
       
       while ((read_addr < address+octet_par_trame) && (label!=0)){     //si label =0, il n'y a pas de distant    
         read_addr =  lectureEeprom(read_addr, buf,octet_par_trame);
         premier_octet=0;              
         temp_TX = buf[0];    Serial.print("temp_TX: ");    Serial.println(temp_TX);         
         premier_octet=premier_octet+1;//on décale de un octet
          if (label==1){ //on regarde le type de valeur sur le label, 1 -> on lit directement un calcul sur 2 octets
             lecture_capteur_1 = buf[premier_octet];
             lecture_capteur_1 *=256;//on recompose le long en concaténant les 2 premiers octets
             lecture_capteur_1 += buf[premier_octet+1];          
             premier_octet=premier_octet+2;//on décale de deux octets              
          } 
          if ((label==11)||(label==41)){ //on regarde le type de valeur sur le label, 11ou 41 -> on lit directement un calcul ou un ADC sur 4 octets
               lecture_capteur_1 = lectureLong(premier_octet, buf);//on lit 4 octets avec lesquels on refait un long
               premier_octet=premier_octet+4;//on décale de quatre octets               
          }
          if ((label==42)||(label==44)){ //on regarde le type de valeur sur le label, 44 ou 42 -> on lit directement 2 ADC sur 4 octets*2
               lecture_capteur_1 = lectureLong(premier_octet, buf);//on lit 4 octets avec lesquels on refait un long
               premier_octet=premier_octet+4;//on décale de quatre octets               
               lecture_capteur_2 = lectureLong(premier_octet, buf);//on lit 4 octets suivants avec lesquels on refait un long
               premier_octet=premier_octet+4;//on décale de quatre octets                              
          }        
          if ((label==44)){ //on regarde le type de valeur sur le label, 44 -> on lit directement 2 ADC sur 4 octets*2
               lecture_capteur_3 = lectureLong(premier_octet, buf);//on lit 4 octets avec lesquels on refait un long
               premier_octet=premier_octet+4;//on décale de quatre octets                              
               lecture_capteur_4 = lectureLong(premier_octet, buf);//on lit 4 octets suivants avec lesquels on refait un long
               premier_octet=premier_octet+4;//on décale de quatre octets               
               
          }
          Serial.print("poids en grammes : ");    Serial.println(lecture_capteur_1);           
          if ((label==42)||(label==44)){ //on regarde le type de valeur sur le label, 42 -> on lit directement 2 ADC sur 4 octets*2
               Serial.print("poids : ");    Serial.println(lecture_capteur_2);
                }
               if ((label==44)){ 
               Serial.print("poids : ");    Serial.println(lecture_capteur_3);
               Serial.print("poids : ");    Serial.println(lecture_capteur_4);
               }  
          
          if (label_rx==41){ //on regarde le type de valeur sur le label_rx, 41 -> on lit  un ADC sur 4 octets
               long lecture_capteur_1 = lectureLong(premier_octet, buf);//on lit 4 octets avec lesquels on refait un long
               premier_octet=premier_octet+4;//on décale de quatre octets                              
          }
          if ((label_rx==42||(label_rx==44))){ //on regarde le type de valeur sur le label_rx, 44 ou 42 -> on lit directement 2 ADC sur 4 octets*2
               long lecture_capteur_1 = lectureLong(premier_octet, buf);//on lit 4 octets avec lesquels on refait un long
               premier_octet=premier_octet+4;//on décale de quatre octets                              
               long lecture_capteur_2 = lectureLong(premier_octet, buf);//on lit 4 octets suivants avec lesquels on refait un long 
               premier_octet=premier_octet+4;//on décale de quatre octets                              
          }        
          if ((label_rx==44)){ //on regarde le type de valeur sur le label_rx, 44 -> on lit directement 2 ADC sur 4 octets*2
               long lecture_capteur_3 = lectureLong(premier_octet, buf);//on lit 4 octets avec lesquels on refait un long
               premier_octet=premier_octet+4;//on décale de quatre octets                              
               long lecture_capteur_4 = lectureLong(premier_octet, buf);//on lit 4 octets suivants avec lesquels on refait un long 
               premier_octet=premier_octet+4;//on décale de quatre octets                              
          }
          if ((label_rx==41)||(label_rx==42)||(label_rx==44)){ //on regarde le type de valeur sur le label_rx, 41 -> on lit  un ADC sur 4 octets          
          Serial.print("poids en grammes: ");    Serial.println(lecture_capteur_1); 
          }
          if ((label_rx==42)||(label_rx==44)){ //on regarde le type de valeur sur le label, label_rx -> on lit directement 2 ADC sur 4 octets*2
         Serial.print("poids en grammes: ");    Serial.println(lecture_capteur_2);
          }
          if ((label_rx==44)){ 
         Serial.print("poids en grammes: ");    Serial.println(lecture_capteur_3);
         Serial.print("poids en grammes: ");    Serial.println(lecture_capteur_4);
          }           
     }
  }
      break;
      
 
case 30 : // lecture brute eeprom
      lecture=lecture+1;//mode lecture
      delay (5000);
      address = adresseCourante();
         if (lecture==1) {
           Serial.print("Addresse:");Serial.print(address);
              if (address+2  > EEPROM_LENGTH){
                 Serial.print("débordement eeprom");
                 address=1022;                 
              }
           Serial.println("");
         }
       while (read_addr < address+octet_par_trame_max) {         
       int temperature_distant=EEPROM.read  ( read_addr-2);     Serial.print("octet num: ") ;    Serial.print(read_addr-2) ;   Serial.print("  valeur octet: ") ; Serial.println(temperature_distant);
         
         read_addr=1+read_addr;//on décale de un octet

     }
      break; 
 
      
case 300 : // RX: ON VA LIRE L'EEPROM; il y a 0 capteur sur le RX; il y a 0 capteur  sur le TX; la trame reçue fait 00 octet ; la trame EEPROM fait  1 octet : 1 [T]
      octet_par_trame=1;
      lecture=lecture+1;//mode lecture
      delay (5000);
      address = adresseCourante();
         if (lecture==1) {
           Serial.print("Addresse: ");Serial.print(address);
              if (address+2+octet_par_trame  > EEPROM_LENGTH){
                 address=1022;
                 Serial.print("débordement eeprom");
              }
           Serial.println("");
         }
       while (read_addr < address) {         
         read_addr =  lectureEeprom(read_addr, buf,octet_par_trame);
         int j = 0;
         temp_TX = buf[j];    Serial.print("temp_TX: ");    Serial.println(temp_TX);    
     }
      EEPROM.write (0, 0);//RAZ de l'@ sur octets 0 & 1
      EEPROM.write (1, 2);   
      break;            
 }
 
 
Serial.println(" boucle suivante ");

}//fin void loop


void miseEnSommeil() {//commande mise en sommeil du Arduino via le circuit économiseur
          if (economiseur) {
            digitalWrite(pin_reed,HIGH); //on fait tirer le celduc qui vide la capa 330 µF à travers une 76 ohms jusqu'à obtenir la valeur du pont inférieur (à choisir faible)            
            delay (tempo_decharge_capa_eco);         // on attend alors la mise en sommeil : tempo au moins égale à RC = 30 millisecondes
          }
}  

long acquisitionCapteur50kg(float tare,float mesure,float etalon, int nombre_point) {
    capteur_50kg.power_up();
    delay (delai_avant_acquisition);          
    long lecture_capteur = capteur_50kg.read_average(nombre_point);//c'est un long moyenné sur x lectures, que l'on va envoyer sur le port serie ou sur eeprom
    float poids_en_gr=(lecture_capteur-tare)/mesure*etalon;
    Serial.print("   valeur ADC 50kg*");Serial.print(lecture_capteur);Serial.print("*");Serial.print(poids_en_gr);Serial.print("*");
    capteur_50kg.power_down();// put the ADC in sleep mode
    return lecture_capteur;
}

 long acquisitionCapteur30kg(float tare,float mesure,float etalon, int nombre_point) {
    capteur_30kg.power_up();
    delay (delai_avant_acquisition);          
    long lecture_capteur = capteur_30kg.read_average(nombre_point);//c'est un long moyenné sur x lectures, que l'on va envoyer sur le port serie ou sur eeprom
    float poids_en_gr=(lecture_capteur-tare)/mesure*etalon;
    Serial.print("   valeur ADC 30kg*");Serial.print(lecture_capteur);Serial.print("*");Serial.print(poids_en_gr);Serial.print("*");
    capteur_30kg.power_down();// put the ADC in sleep mode
    return lecture_capteur;
} 

 long acquisitionCapteur20kg_1(float tare,float mesure,float etalon, int nombre_point) {
    capteur_20kg_1.power_up();
    delay (delai_avant_acquisition);          
    long lecture_capteur = capteur_20kg_1.read_average(nombre_point);//c'est un long moyenné sur x lectures, que l'on va envoyer sur le port serie ou sur eeprom
    float poids_en_gr=(lecture_capteur-tare)/mesure*etalon;
    Serial.print("   valeur ADC 20kg_1*");Serial.print(lecture_capteur);Serial.print("*");Serial.print(poids_en_gr);Serial.print("*");
    capteur_20kg_1.power_down();// put the ADC in sleep mode
    return lecture_capteur;
} 

 long acquisitionCapteur20kg_2(float tare,float mesure,float etalon, int nombre_point) {
    capteur_20kg_2.power_up();
    delay (delai_avant_acquisition);          
    long lecture_capteur = capteur_20kg_2.read_average(nombre_point);//c'est un long moyenné sur x lectures, que l'on va envoyer sur le port serie ou sur eeprom
    float poids_en_gr=(lecture_capteur-tare)/mesure*etalon;
    Serial.print("   valeur ADC 20kg_2*");Serial.print(lecture_capteur);Serial.print("*");Serial.print(poids_en_gr);Serial.print("*");
    capteur_20kg_2.power_down();// put the ADC in sleep mode
    return lecture_capteur;
}

 long acquisitionCapteur20kg_3(float tare,float mesure,float etalon, int nombre_point) {
    capteur_20kg_3.power_up();
    delay (delai_avant_acquisition);          
    long lecture_capteur = capteur_20kg_3.read_average(nombre_point);//c'est un long moyenné sur x lectures, que l'on va envoyer sur le port serie ou sur eeprom
    float poids_en_gr=(lecture_capteur-tare)/mesure*etalon;
    Serial.print("   valeur ADC 20kg_3*");Serial.print(lecture_capteur);Serial.print("*");Serial.print(poids_en_gr);Serial.print("*");
    capteur_20kg_3.power_down();// put the ADC in sleep mode
    return lecture_capteur;
}

 long acquisitionCapteur20kg_4(float tare,float mesure,float etalon, int nombre_point) {
    capteur_20kg_4.power_up();
    delay (delai_avant_acquisition);          
    long lecture_capteur = capteur_20kg_4.read_average(nombre_point);//c'est un long moyenné sur x lectures, que l'on va envoyer sur le port serie ou sur eeprom
    float poids_en_gr=(lecture_capteur-tare)/mesure*etalon;
    Serial.print("   valeur ADC 20kg_4*");Serial.print(lecture_capteur);Serial.print("*");Serial.print(poids_en_gr);Serial.print("*");
    capteur_20kg_4.power_down();// put the ADC in sleep mode
    return lecture_capteur;
}

 long acquisitionCapteur10kg(float tare,float mesure,float etalon, int nombre_point) {
    capteur_10kg.power_up();
    delay (delai_avant_acquisition);          
    long lecture_capteur = capteur_10kg.read_average(nombre_point);//c'est un long moyenné sur x lectures, que l'on va envoyer sur le port serie ou sur eeprom
    float poids_en_gr=(lecture_capteur-tare)/mesure*etalon;
    Serial.print("   valeur ADC 10kg*");Serial.print(lecture_capteur);Serial.print("*");Serial.print(poids_en_gr);Serial.print("*");
    capteur_10kg.power_down();// put the ADC in sleep mode
    return lecture_capteur;
}
         
void readAvailableRXData(byte buf[] , int buf_len) {
  for (int i=0; i<buf_len; i++) {      //  READ BYTE CMD
        digitalWrite(CS,LOW);          
       
        previous_cmd_status = SPI.transfer(ARDUINO_CMD_READ);
        delayMicroseconds(wait_time_us_between_bytes_spi);
        shield_status = SPI.transfer(0x00);
        delayMicroseconds(wait_time_us_between_bytes_spi);
        buf[i] = SPI.transfer(0x00); // Store the received byte
        delayMicroseconds(wait_time_us_between_bytes_spi);
        digitalWrite(CS,HIGH);
        delayMicroseconds(wait_time_us_between_spi_msg);
        } 
}  


int checkifAvailableRXData() {        // data available cmd
  int tmp = 0;
  digitalWrite(CS, LOW); 
  previous_cmd_status = SPI.transfer(ARDUINO_CMD_AVAILABLE);
  delayMicroseconds(wait_time_us_between_bytes_spi);
  shield_status = SPI.transfer(0x00);
  delayMicroseconds(wait_time_us_between_bytes_spi);  
  available_msb = SPI.transfer(0x00);
  delayMicroseconds(wait_time_us_between_bytes_spi); 
  available_lsb = SPI.transfer(0x00);
  delayMicroseconds(wait_time_us_between_bytes_spi);
  digitalWrite(CS,HIGH);   // sets SS pin high to de-select the chip:
  tmp = (available_msb<<8) + available_lsb;
  return tmp;
}

int arduinoLoraTXWrite( byte buf[], int buf_len) {    
  digitalWrite(CS, LOW);
  int  previous_cmd_status  =  SPI.transfer(ARDUINO_CMD_WRITE); // Send: COMMAND Write. The first result byte is the one in which the shield puts the status of last command
  delayMicroseconds(wait_time_us_between_bytes_spi);
  SPI.transfer(buf_len >> 8);    //Send:  Size of bytes to send
  delayMicroseconds(wait_time_us_between_bytes_spi);
  SPI.transfer(buf_len);
    
          for (int i = 0; i < buf_len ; i ++) {    //Send:  payload as bytes to send
          delayMicroseconds(wait_time_us_between_bytes_spi);
          SPI.transfer(buf[ i ]); 
          }
  
  digitalWrite(CS, HIGH);
  return previous_cmd_status;
  
}

long lectureLong(byte premier_octet, byte data_rcv[]){//on lit 4 octets avec lesquels on refait un long 
        int l=4;
        long lecture_capteur = data_rcv[premier_octet];
        for (uint8_t i=premier_octet;i<premier_octet+l;i++) {
            lecture_capteur |= (long)data_rcv[i] << (24 - (8*(i-premier_octet)));//on recompose le long en concaténant les 4 premiers octets
         }
         return lecture_capteur;
}   

int lectureInt(byte premier_octet, byte data_rcv[]){//on lit 2 octets avec lesquels on refait un int 
        int lecture_capteur = data_rcv[premier_octet];
        lecture_capteur *=256;//on recompose l'int en concaténant les 2 premiers octets
        lecture_capteur += data_rcv[premier_octet+1];
         return lecture_capteur;
}

int adresseCourante() {//adresse d'une trame EEPROM, On la lit sur les 2 premiers octets EEPROM
  address = EEPROM.read(0);
  address *= 256; // <=> addresse<<8
  address += EEPROM.read(1); // <=> adress |= EEPROM...
  return address;
}

int lectureEeprom(int adresse,byte buf[],int octet_par_cycle) {//on lit une trame EEPROM qu'on met dans le tableau buf
  byte i=0;
  for(i=0;i< octet_par_cycle;i++) {
    buf[i] = EEPROM.read(adresse+i);
   }
    return adresse+octet_par_cycle;
}

int sauverEntier(int adresse, long entier) {// //fonction d'écriture d'un long de 4 octets en mémoire EEPROM,retourne la prochaine adresse libre sauf si dépassement
   uint8_t i=0;uint8_t data[4];
   data[0] =  entier >> 24; //on va decomposer le long entier en ses 4 octets pour les passer à l'eeprom
   data[1] = (entier >> 16) & 0xFF;
   data[2] = (entier >>  8) & 0xFF;
   data[3] = (entier      ) & 0xFF;
     if (adresse+3 <= EEPROM_LENGTH) {
       for(i;i<4;i++) {
        EEPROM.write(adresse+i, data[i]);
       }
       i=4;
     } 
  EEPROM.write (0, ((adresse+i)>>8) & 0xFF);
  EEPROM.write (1, (adresse+i) & 0xFF);
  Serial.print("adresse   ");Serial.print(adresse+i); 

  return adresse+i;

  }
  
 int sauverEeprom(int adresse, uint8_t buf[19],byte octet_par_trame,byte octet_gestion_trame) {// //fonction d'écriture de nombre_octet octets en mémoire EEPROM,retourne la prochaine adresse libre sauf si dépassement
  uint8_t i=octet_gestion_trame;
    if (adresse+octet_par_trame-octet_gestion_trame+2 >= EEPROM_LENGTH) {//démarre à 2, puisqu'on met le pointeur dans les @ 0 et 1
      i=octet_par_trame;//si débordement, on ne stocke plus
    }
    for(i;i<octet_par_trame;i++) {
      EEPROM.write(adresse+i, buf[i]); //Serial.print(" buf: ");Serial.println(buf[i]); 
    }
    EEPROM.write (0, (adresse>>8) & 0xFF);//on sauve l'@ sur octets 0 & 1
    EEPROM.write (1, adresse & 0xFF);
 return adresse+octet_par_trame-octet_gestion_trame;//on renvoie l'adresse incrémentée
}

byte temperatureArduino(float GAIN,float OFFSET) {
	float wADC;byte temperature;//on ajustebGain et Offset pour chaque Arduino en particulier
	ADCSRA |= (1 << ADEN);//enable the ADC
	ADMUX |= (1 << REFS1) | (1 << REFS0);	//set reference to the internal 1.1V
	ADMUX |= (1 << MUX3);//select the channel
	ADMUX &= ~((1 << MUX2) | (1 << MUX1) | (1 << MUX0));
	delay(10);//let the voltages stabilize
	ADCSRA |= (1 << ADSC);	//start the conversion
	while ((ADCSRA & (1 << ADSC)));	//wait until the conversion is in progress	
	wADC = ADCW;	//get the ADC output
       temperature = ((wADC - OFFSET)+30)*2.5 / GAIN;//calcule température en f(gain, offset) puis ajuste à un octet de -30°C à +70°C, avec un coef de 2.5 pour conserver un peu de précision (0.8°)
  return (temperature);
}




