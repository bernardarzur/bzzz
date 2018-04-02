/*version V1 : y a le local capteur et le distant, on peut tester en local (sans lora), on enregistre sur eeprom un des deux capteurs; v2 -> deux capteurs locaux et un distant; v3 -> corrige gros
bug : il faut faire une pseudo-mesure avant de démarrer, bof, finalement on fait moyenne de 100 mesures, v4-> temperature et label, v5-> deux capteurs dans le distant (poids = somme des deux)
v6-> on rajoute un capteur local aux deux distants (v5 ne marche plus) puis versions tx_rx_v1: on y met les deux, ainsi que la lecture; version tx_rx_v2 : config 4 capteurs 20kg; 
version tx_rx_v3 : on fait un cycle de mesures sur n points, b fois de suite en envoyant un numéro de trame sauvé sur EEPROM TX (on s'est aperçu qu'on perdait bcp de trames) et en mars 2018, on rajoute
config 1014 et 2014
    
      case 110 : // RX SEULEMENT PAS DE TX, ON VA CONFIGURER LE RX, UN SEUL CAPTEUR SUR LE RX,
      case 120 : // RX SEULEMENT PAS DE TX, ON VA CONFIGURER LE RX, DEUX CAPTEURS SUR LE RX,
      case 130 : // RX SEULEMENT PAS DE TX, ON VA CONFIGURER LE RX, TROIS CAPTEURS SUR LE RX,
      case 140 : // RX SEULEMENT PAS DE TX, ON VA CONFIGURER LE RX, quatre CAPTEURS SUR LE RX,

      case 101 : // RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteurs sur le RX; il y a 1 capteurs sur le TX; la trame reçue fait 7 octets  :  2 [label]+1 [T]+4 [1 long]
      case 1014: // RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteurs sur le RX; il y a 4 capteur sur le TX, on calcule poids total en g et on envoie; la trame envoyée fait 7 octets : 2 [label/num trame]+1 [T]+4 [1 long]
      case 10145:// RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteurs sur le RX; il y a 4 capteur sur le TX, on calcule poids total en g et on envoie; la trame envoyée fait 5 octets : 2 [label/num trame]+1 [T]+2 [1 int]
      case 102 : // RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteurs sur le RX; il y a 2 capteurs sur le TX; la trame reçue fait 11 octets : 2 [label]+1 [T]+8 [2 long]
      case 104 : // RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteurs sur le RX; il y a 4 capteurs sur le TX; la trame reçue fait 19 octets : 2 [label]+1 [T]+16 [4 long]
      case 112 : // RX ET TX, ON VA CONFIGURER LE RX; il y a 1 capteurs sur le RX; il y a 2 capteurs sur le TX; la trame reçue fait 11 octets : 2 [label]+1 [T]+8 [2 long]
      case 122 : // RX ET TX, ON VA CONFIGURER LE RX; il y a 2 capteurs sur le RX; il y a 2 capteurs sur le TX; la trame reçue fait 11 octets : 2 [label]+1 [T]+8 [2 long]

      case 201 : // RX ET TX ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a 1 capteurs sur le TX; la trame émise fait 7 octets  : 2 [label]+1 [T]+4 [1* long]
      case 20115:// RX ET TX ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a un capteur sur le TX; la trame émise fait 5 octets  : 2 [label]+1 [T]+2 [1* int]
      case 2014: // RX ET TX ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a 4 capteurs sur le TX mais on ne renvoie que la somme en grammes; la trame reçue fait 7 octets : 2 [label/trame]+1 [T]+4 [1 long]
      case 20145:// RX ET TX ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a 4 capteurs sur le TX mais on ne renvoie que la somme en grammes; la trame reçue fait 5 octets : 2 [label/trame]+1 [T]+2 [1 int]
      case 202 : // RX ET TX ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a 2 capteurs sur le TX; la trame émise fait 11 octets : 2 [label]+1 [T]+8 [2 long]
      case 204 : // RX ET TX ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a 4 capteurs sur le TX; la trame émise fait 19 octets : 2 [label]+1 [T]+16 [4 long]
      
      case 301 : // RX: ON VA LIRE L'EEPROM; il y a 0 capteur sur le RX; il y a 1 capteurs sur le TX; la trame reçue fait  7 octets ; la trame EEPROM fait  5 octets : 1 [T]+4 [1* long]
      case 30145: // RX: ON VA LIRE L'EEPROM; il y a 0 capteur sur le RX; il y a 1 capteurs sur le TX; la trame reçue fait  5 octets ; la trame EEPROM fait  3 octets : 1 [T]+2 [1* int]
      case 302 : // RX: ON VA LIRE L'EEPROM; il y a 0 capteur sur le RX; il y a 2 capteurs sur le TX; la trame reçue fait 11 octets ; la trame EEPROM fait  9 octets : 1 [T]+8 [2* long]
      case 304 : // RX: ON VA LIRE L'EEPROM; il y a 0 capteur sur le RX; il y a 4 capteurs sur le TX; la trame reçue fait 19 octets ; la trame EEPROM fait 17 octets : 1 [T]+16 [4* long]
      case 310 : // RX: ON VA LIRE L'EEPROM; il y a 1 capteur sur le RX; il y a 0 capteurs sur le TX; il n'y a pas de trame reçue   ; la trame EEPROM fait  4 octets : 4 [1* long]
      case 312 : // RX: ON VA LIRE L'EEPROM; il y a 1 capteur sur le RX; il y a 2 capteurs sur le TX; il n'y a pas de trame reçue   ; la trame EEPROM fait 13 octets : 1 [T]+12 [3* long]
      case 320 : // RX: ON VA LIRE L'EEPROM; il y a 2 capteur sur le RX; il y a 0 capteurs sur le TX; il n'y a pas de trame reçue   ; la trame EEPROM fait  8 octets : 4 [2* long]
      case 340 : // RX: ON VA LIRE L'EEPROM; il y a 4 capteur sur le RX; il y a 0 capteurs sur le TX; il n'y a pas de trame reçue   ; la trame EEPROM fait 16 octets : 4 [4* long]
*/
int configuration = 10145; //  Choisir une configuration: 1er chiffre 1->configuration RX, 2->configurationTX, 3->lecture EEPROM/TX ** 2eme chiffre->nb capteurs RX ** 3eme chiffre->nb sur TX
int eeprom=1;              //1 si on veut sauvegarder sur EEPROM du RX, 0 sinon
int economiseur=0;         //1 si on veut utiliser la carte économiseur (active la fonction miseEnSommeil). ATTENTION pour le RX mettre à ZERO, sinon on rajoute tempo_decharge_capa_eco à la boucle
byte l=2;                  //nombre d'octets par mesure envoyée sur LoRa, si c'est un long, l=4,  si c'est un entier, l=2 (cas 10145, 20145, et 3015)

long tempo_local=300;      //tempo entre deux mesures si capteur local seulement, sinon c'est le distant qui pilote
int pin_reed = 9;          // commande Relais Reed pour couper l'alimentation du Arduino sur le TX, ou le RX si on est en mode local économe (sans PC)
int tempo_decharge_capa_eco = 1000;     //temps de décharge de la capa économiseur (mini 300ms)
int tempo_lora_demarrage = 1000;        //le temps que la carte lora soit opérationnelle
int tempo_lora_emission = 3000;         //le temps que la carte lora finisse l'émission
int nombre_point=10;                    //c'est le nombre d'acquisitions faites par le HX711, qui en fait une moyenne appelée mesure
byte b_mesure_par_cycle = 3;            //on fait "b_mesure_par_cycle"  mesures et on envoie "b_mesure_par_cycle" trames avec le même n° "numero_trame" sur l'octet 3eme

#include "EEPROM.h"
int EEPROM_LENGTH=1024;     // l'adresse de la dernière sauvegarde est sauvée sur les 2 premiers octets de l'EEprom (0 et 1),on peut donc lire/écrire jusqu'à 1022 octets
int address = 2;            //adresse pour sauver une trame de données sur l'eeprom RX, on démarre à 2 pour les ecritures
int read_addr = 2;          //adresse pour lire les données sur eeprom, on démarre à 2 pour les lectures
byte premier_octet=3;       //premier octet de lecture_capteur_1 sur la trame reçue
byte octet_par_trame_max=19; //c'est la longueur de trame la plus longue de tous les "cases" programmés, elle sert à programmer les deux tableaux data et data_rcv
byte label=1;         //controle expéditeur sur deux octets
byte numero_trame=0;
byte octet_par_trame=0;//selon case
byte lecture=0;//mode sans lecture par défaut
byte a_max=1;//affichage port serie a est le nb max de mesures par ligne, 
byte a=1;//affichage port serie a est le nb  de mesures par ligne, 
byte b=0;//b est le nombre total de mesures

long lecture_capteur_1 = 0;
long lecture_capteur_2 = 0;
long lecture_capteur_3 = 0;
long lecture_capteur_4 = 0;
byte temperature_distant=0;
float temperature_local=0;
float poids_en_grammes=0;        
float poids_en_gr_total=0; 
long  poids_en_gr_distant=0;
int p=0;//permet de ramener la mesure sur deux octets pour réduire mémoire sur EEPROM (l=2 dans ce cas, config 2014)

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
const float GAIN_distant=0.80;//paramètres de mesure de la température : à régler pour chaque Arduino
const float OFFSET_distant=314;//paramètres de mesure de la température : à régler pour chaque Arduino
const float GAIN_local=1.22;//paramètres de mesure de la température : à régler pour chaque Arduino
const float OFFSET_local=318;//paramètres de mesure de la température : à régler pour chaque Arduino

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
//  EEPROM.write (1023, data[1]);//on écrit le premier numero de trame sur le RX, ou le TX???




  switch (configuration) {


    case 101 : // RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteurs sur le RX; il y a un capteur sur le TX; la trame reçue fait 7 octets : 2 [label]+1 [T]+4 [1 long]
      available = checkifAvailableRXData() ;//on regarde si il y a des paquets LoRa en attente
      octet_par_trame=7;
      while (!available){
        available = checkifAvailableRXData() ;
        delay (100);
      }
      readAvailableRXData(data_rcv , available);
      if ((data_rcv[0]==label)&&(data_rcv[1]==label)){//vérification octets premier et second pour controle destinataire
       transmission=1 ;//transmission déclarée OK
       lecture_capteur_1=lectureLong( premier_octet, data_rcv);
       float poids_en_gr_distant=((lecture_capteur_1-tare_30kg)/mesure_30kg*etalon_30kg);
       temperature_distant=(data_rcv[2]/2.5-30);//octet troisieme
       temperature_local=temperatureArduino(GAIN_local,OFFSET_local)/2.5-30;
       Serial.print("  poids en gr distant:  *");Serial.print(poids_en_gr_distant);Serial.print(" g *");
       Serial.print("Température local: ");Serial.print(temperature_local);Serial.print("*Température distant:  ");Serial.print(temperature_distant);Serial.print("*");
             
         if (eeprom){ 
           address=sauverDistant(address, data_rcv, octet_par_trame );//on sauve la température distante & deux lecture_capteurs_x sur 9 octets à partir de l'adresse "address" puis 
           //la fonction sauver met à jour la nouvelle adresse de sauvegarde, que l'on écrit sur les octets 1 et 2     
         }
       }
          else {
           Serial.println ("erreur transmission");
           }
      miseEnSommeil(); //eteint Arduino
      break;
      
    case 1014 : // RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteurs sur le RX; il y a quatre capteur sur le TX, on calcule poids total en g et on envoie; la trame reçue fait 7 octets : 2 [label/num trame]+1 [T]+4 [1 long]
      available = checkifAvailableRXData() ;//on regarde si il y a des paquets LoRa en attente
      octet_par_trame=7;
      while (!available){
        available = checkifAvailableRXData() ;
        delay (100);
      }
      readAvailableRXData(data_rcv , available);
      if (data_rcv[premier_octet-3]==label) 
     {//vérification octet premier  pour controle destinataire, et controle n° trame pour prendre une seule mesure
       transmission=1 ;//transmission déclarée OK
       lecture_capteur_1        =lectureLong( premier_octet, data_rcv);
       poids_en_gr_distant=lecture_capteur_1;Serial.print(" n°1 ");Serial.print(poids_en_gr_distant);
       numero_trame             =data_rcv[premier_octet-2];//octet deuxieme
       temperature_distant      =(data_rcv[premier_octet-1]/2.5-30);//octet troisieme
       temperature_local        =temperatureArduino(GAIN_local,OFFSET_local)/2.5-30;
       Serial.print(" poids en gr distant: ");Serial.print(poids_en_gr_distant);
       Serial.print(" Température local: ");Serial.print(temperature_local);Serial.print(" Température distant: ");Serial.print(temperature_distant);
       Serial.print (" n° trame: ");Serial.print(numero_trame); 
       if   ((numero_trame - (EEPROM.read(1023)))>1)
          {//si la différence est supérieure à 1, il y a des trames perdues
            Serial.print (" perte trames: "); Serial.println((data_rcv[1]- (EEPROM.read(1023))));
          }   
       if ((eeprom)&&(numero_trame!=EEPROM.read(1023)))
          { 
           address=sauverDistant(address, data_rcv,octet_par_trame);//on sauve la température distante & une lecture_capteur sur 5 octets à partir de l'adresse "address" puis 
           //la fonction sauver met à jour la nouvelle adresse de sauvegarde, que l'on écrit sur les octets 1 et 2   
           EEPROM.write (1023, numero_trame);//on écrit le nouveau numero de trame   
          }    
      }
          else {
           Serial.println ("erreur transmission");
           }
      miseEnSommeil(); //eteint Arduino
      break;     

    case 10145 : // RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteurs sur le RX; il y a quatre capteur sur le TX, on calcule poids total en g et on envoie; la trame reçue fait 5 octets : 2 [label/num trame]+1 [T]+2 [1 int]
      available = checkifAvailableRXData() ;//on regarde si il y a des paquets LoRa en attente
      octet_par_trame=5;
      while (!available){
        available = checkifAvailableRXData() ;
        delay (100);
      }
      readAvailableRXData(data_rcv , available);
      if (data_rcv[premier_octet-3]==label) 
     {//vérification octet premier  pour controle destinataire, et controle n° trame pour prendre une seule mesure
       transmission=1 ;//transmission déclarée OK
       lecture_capteur_1        =lectureInt( premier_octet, data_rcv);
       Serial.print(" poids distant ");Serial.print(lecture_capteur_1);
       numero_trame             =data_rcv[premier_octet-2];//octet deuxieme
       temperature_distant      =(data_rcv[premier_octet-1]/2.5-30);//octet troisieme
       temperature_local        =temperatureArduino(GAIN_local,OFFSET_local)/2.5-30;
       Serial.print(" poids en gr distant: ");Serial.print(lecture_capteur_1);
       Serial.print(" Température local: ");Serial.print(temperature_local);Serial.print(" Température distant: ");Serial.print(temperature_distant);
       Serial.print (" n° trame: ");Serial.print(numero_trame); 
       if   ((numero_trame - (EEPROM.read(1023)))>1)
          {//si la différence est supérieure à 1, il y a des trames perdues
            Serial.print (" perte trames: "); Serial.println((data_rcv[1]- (EEPROM.read(1023))));
          }   
       if ((eeprom)&&(numero_trame!=EEPROM.read(1023)))
          { 
           address=sauverDistant(address, data_rcv,octet_par_trame);//on sauve la température distante & une lecture_capteur sur 3 octets à partir de l'adresse "address" puis 
           //la fonction sauver met à jour la nouvelle adresse de sauvegarde, que l'on écrit sur les octets 1 et 2   
           EEPROM.write (1023, numero_trame);//on écrit le nouveau numero de trame   
          }        
      }
          else {
           Serial.println ("erreur transmission");
           }
      miseEnSommeil(); //eteint Arduino
      break;     

      
    case 102 : // RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteurs sur le RX; il y a deux capteurs sur le TX; la trame reçue fait 11 octets : 2 [label]+1 [T]+8 [2 long]
      available = checkifAvailableRXData() ;//on regarde si il y a des paquets LoRa en attente
      octet_par_trame=11;
      while (!available){
        available = checkifAvailableRXData() ;
        delay (100);
      }
      readAvailableRXData(data_rcv , available);
      if ((data_rcv[0]==label)&&(data_rcv[1]==label)){//vérification octets premier et second pour controle destinataire
       transmission=1 ;//transmission déclarée OK
       lecture_capteur_1=lectureLong( premier_octet, data_rcv);
       lecture_capteur_2=lectureLong( premier_octet+l, data_rcv);
       float poids_en_gr_distant=((lecture_capteur_1-tare_30kg)/mesure_30kg*etalon_30kg)+((lecture_capteur_2-tare_50kg)/mesure_50kg*etalon_50kg);
       temperature_distant=(data_rcv[2]/2.5-30);//octet troisieme
       temperature_local=temperatureArduino(GAIN_local,OFFSET_local)/2.5-30;
       Serial.print("  poids en gr distant:  *");Serial.print(poids_en_gr_distant);Serial.print(" g *");
       Serial.print("Température local: ");Serial.print(temperature_local);Serial.print("*Température distant:  ");Serial.print(temperature_distant);Serial.print("*");
             
         if (eeprom){ 
           address=sauverDistant(address, data_rcv,octet_par_trame);//on sauve la température distante & deux lecture_capteurs_x sur 9 octets à partir de l'adresse "address" puis 
           //la fonction sauver met à jour la nouvelle adresse de sauvegarde, que l'on écrit sur les octets 1 et 2     
         }
       }
          else {
           Serial.println ("erreur transmission");
           }
      miseEnSommeil(); //eteint Arduino
      break;

      
    case 104 : // RX ET TX, ON VA CONFIGURER LE RX; il y a 0 capteurs sur le RX; il y a quatre capteurs sur le TX; la trame reçue fait 19 octets : 1 [label] + 1 [numero_trame] +1 [T]+16 [4 long]
      available = checkifAvailableRXData() ;//on regarde si il y a des paquets LoRa en attente
      octet_par_trame=19;
      while (!available){
        available = checkifAvailableRXData() ;
        delay (100);
      }
      readAvailableRXData(data_rcv , available);
      if (data_rcv[premier_octet-3]==label) 
     {//vérification octet premier  pour controle destinataire, et controle n° trame pour prendre une seule mesure

       transmission=1 ;//transmission déclarée OK
       lecture_capteur_1        =lectureLong( premier_octet, data_rcv);
       float poids_en_gr_distant=((lecture_capteur_1-tare_20kg_1)/mesure_20kg_1*etalon_20kg_1);Serial.print(" n°1 ");Serial.print(poids_en_gr_distant);
       lecture_capteur_2        =lectureLong( premier_octet+l, data_rcv);
       poids_en_gr_distant      =((lecture_capteur_2-tare_20kg_2)/mesure_20kg_2*etalon_20kg_2);Serial.print(" n°2 ");Serial.print(poids_en_gr_distant);
       lecture_capteur_3        =lectureLong( premier_octet+2*l, data_rcv);
       poids_en_gr_distant      =((lecture_capteur_3-tare_20kg_3)/mesure_20kg_3*etalon_20kg_3);Serial.print(" n°3 ");Serial.print(poids_en_gr_distant);
       lecture_capteur_4        =lectureLong( premier_octet+3*l, data_rcv);
       poids_en_gr_distant      =((lecture_capteur_4-tare_20kg_4)/mesure_20kg_4*etalon_20kg_4);Serial.print(" n°4 ");Serial.print(poids_en_gr_distant);
       poids_en_gr_distant      =((lecture_capteur_1-tare_20kg_1)/mesure_20kg_1*etalon_20kg_1)+((lecture_capteur_2-tare_20kg_2)/mesure_20kg_2*etalon_20kg_2)+((lecture_capteur_3-tare_20kg_3)/mesure_20kg_3*etalon_20kg_3)+((lecture_capteur_4-tare_20kg_4)/mesure_20kg_4*etalon_20kg_4);
       numero_trame             =data_rcv[premier_octet-2];//octet deuxieme
       temperature_distant      =(data_rcv[premier_octet-1]/2.5-30);//octet troisieme
       temperature_local        =temperatureArduino(GAIN_local,OFFSET_local)/2.5-30;
       Serial.print(" poids en gr distant: ");Serial.print(poids_en_gr_distant);
       Serial.print(" Température local: ");Serial.print(temperature_local);Serial.print(" Température distant: ");Serial.print(temperature_distant);
       Serial.print (" n° trame: ");Serial.print(numero_trame); 
       if   ((numero_trame - (EEPROM.read(1023)))>1)
          {//si la différence est supérieure à 1, il y a des trames perdues
            Serial.print (" perte trames: "); Serial.println((data_rcv[1]- (EEPROM.read(1023))));
          }   
       if ((eeprom)&&(numero_trame!=EEPROM.read(1023)))
          { 
           address=sauverDistant(address, data_rcv,octet_par_trame);//on sauve la température distante & quatre lecture_capteurs_x sur 17 octets à partir de l'adresse "address" puis 
           //la fonction sauver met à jour la nouvelle adresse de sauvegarde, que l'on écrit sur les octets 1 et 2   
           EEPROM.write (1023, numero_trame);//on écrit le nouveau numero de trame   
          }

         
      }
          else {
           Serial.println ("erreur transmission");
           }
      miseEnSommeil(); //eteint Arduino
      break;   

 
    case 110 : // RX SEULEMENT PAS DE TX , UN SEUL CAPTEUR SUR LE RX, ON VA CONFIGURER LE RX
      delay (tempo_local);//tempo des cycles d'acquisitions pilotée en local
      transmission=1 ;//la transmission est déclarée bonne puisqu'il n'y en a pas!
//      lecture_capteur_1=acquisitionCapteur10kg(tare_10kg,mesure_10kg,etalon_10kg,nombre_point);//fait l'acquisition sur le capteur 10 kg sur une moyenne de nombre_point
//      lecture_capteur_1=acquisitionCapteur20kg_1(tare_20kg_1,mesure_20kg_1,etalon_20kg_1,nombre_point);//fait l'acquisition sur le capteur n°1-20 kg sur une moyenne de nombre_point
//      lecture_capteur_1=acquisitionCapteur20kg_2(tare_20kg_2,mesure_20kg_2,etalon_20kg_2,nombre_point);//fait l'acquisition sur le capteur n°2-20 kg sur une moyenne de nombre_point
      lecture_capteur_1=acquisitionCapteur20kg_3(tare_20kg_3,mesure_20kg_3,etalon_20kg_3,nombre_point);//fait l'acquisition sur le capteur n°3-20 kg sur une moyenne de nombre_point
//      lecture_capteur_1=acquisitionCapteur20kg_4(tare_20kg_4,mesure_20kg_4,etalon_20kg_4,nombre_point);//fait l'acquisition sur le capteur n°4-20 kg sur une moyenne de nombre_point
//      lecture_capteur_1=acquisitionCapteur50kg(tare_50kg,mesure_50kg,etalon_50kg,nombre_point);//fait l'acquisition sur le capteur 50 kg sur une moyenne de nombre_point
//      lecture_capteur_1=acquisitionCapteur30kg(tare_30kg,mesure_30kg,etalon_30kg,nombre_point);//fait l'acquisition sur le capteur 30 kg sur une moyenne de nombre_point
       if (eeprom) {
        address=sauverEntier(address, lecture_capteur_1);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
       }
      miseEnSommeil(); //eteint Arduino
      break;
    

    case 120 : // RX SEULEMENT PAS DE TX , DEUX CAPTEURS SUR LE RX, ON VA CONFIGURER LE RX
      delay (tempo_local);//tempo des cycles d'acquisitions pilotée en local
      transmission=1 ;//la transmission est déclarée bonne puisqu'il n'y en a pas!
      lecture_capteur_2=acquisitionCapteur30kg(tare_30kg,mesure_30kg,etalon_30kg,nombre_point);//fait l'acquisition sur le capteur 30 kg sur une moyenne de nombre_point
      lecture_capteur_1=acquisitionCapteur50kg(tare_50kg,mesure_50kg,etalon_50kg,nombre_point);//fait l'acquisition sur le capteur 50 kg sur une moyenne de nombre_point
       if (eeprom) {
        address=sauverEntier(address, lecture_capteur_1);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
        address=sauverEntier(address, lecture_capteur_2);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
       }
      miseEnSommeil(); //eteint Arduino
      break; 
      
    case 130 : // RX SEULEMENT PAS DE TX , DEUX CAPTEURS SUR LE RX, ON VA CONFIGURER LE RX
      delay (tempo_local);//tempo des cycles d'acquisitions pilotée en local
      transmission=1 ;//la transmission est déclarée bonne puisqu'il n'y en a pas!
      lecture_capteur_1=acquisitionCapteur20kg_1(tare_20kg_1,mesure_20kg_1,etalon_20kg_1,nombre_point);//fait l'acquisition sur le capteur n°1-20 kg sur une moyenne de nombre_point
      lecture_capteur_2=acquisitionCapteur20kg_2(tare_20kg_2,mesure_20kg_2,etalon_20kg_2,nombre_point);//fait l'acquisition sur le capteur n°2-20 kg sur une moyenne de nombre_point
      lecture_capteur_3=acquisitionCapteur20kg_4(tare_20kg_4,mesure_20kg_4,etalon_20kg_4,nombre_point);//fait l'acquisition sur le capteur n°4-20 kg sur une moyenne de nombre_point
       if (eeprom) {
        address=sauverEntier(address, lecture_capteur_1);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
        address=sauverEntier(address, lecture_capteur_2);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
        address=sauverEntier(address, lecture_capteur_3);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
       }
      miseEnSommeil(); //eteint Arduino
      break; 
      
    case 140 : // RX SEULEMENT PAS DE TX , quatre CAPTEURS SUR LE RX, ON VA CONFIGURER LE RX
      delay (tempo_local);//tempo des cycles d'acquisitions pilotée en local, NB : si utilisation de la carte économiseur pas de stockage sur EEPROM! on remet adresse à zéro à chaque arrêt.
      transmission=1 ;//la transmission est déclarée bonne puisqu'il n'y en a pas!
      lecture_capteur_1=acquisitionCapteur20kg_1(tare_20kg_1,mesure_20kg_1,etalon_20kg_1,nombre_point);//fait l'acquisition sur le capteur n°1-20 kg sur une moyenne de nombre_point
      poids_en_grammes=(lecture_capteur_1-tare_20kg_1)/mesure_20kg_1*etalon_20kg_1;
      lecture_capteur_2=acquisitionCapteur20kg_2(tare_20kg_2,mesure_20kg_2,etalon_20kg_2,nombre_point);//fait l'acquisition sur le capteur n°2-20 kg sur une moyenne de nombre_point
      poids_en_grammes=poids_en_grammes + (lecture_capteur_2-tare_20kg_2)/mesure_20kg_2*etalon_20kg_2;
      lecture_capteur_3=acquisitionCapteur20kg_3(tare_20kg_3,mesure_20kg_3,etalon_20kg_3,nombre_point);//fait l'acquisition sur le capteur n°3-20 kg sur une moyenne de nombre_point
      poids_en_grammes=poids_en_grammes + (lecture_capteur_3-tare_20kg_3)/mesure_20kg_3*etalon_20kg_3;
      lecture_capteur_4=acquisitionCapteur20kg_4(tare_20kg_4,mesure_20kg_4,etalon_20kg_4,nombre_point);//fait l'acquisition sur le capteur n°4-20 kg sur une moyenne de nombre_point
      poids_en_grammes=poids_en_grammes + (lecture_capteur_4-tare_20kg_4)/mesure_20kg_4*etalon_20kg_4;
     Serial.print("  poids_en_grammes_total   "); Serial.print(poids_en_grammes);Serial.print("  ");
       if (eeprom) {
        address=sauverEntier(address, lecture_capteur_1);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
        address=sauverEntier(address, lecture_capteur_2);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
        address=sauverEntier(address, lecture_capteur_3);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
        address=sauverEntier(address, lecture_capteur_4);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
       }
      miseEnSommeil(); //eteint Arduino
      break;
      
      case 112 : // RX ET TX ON VA CONFIGURER LE RX; il y a 1 capteur sur le RX; il y a deux capteurs sur le TX; la trame reçue fait 11 octets : 2 [label]+1 [T]+8 [2 long]
      octet_par_trame=11; 
      available = checkifAvailableRXData() ;//debut de cycle piloté par le distant, on attend réception paquet LoRa pour démarrer le cycle
      while (!available){
        available = checkifAvailableRXData() ;
        delay (100);
      }
      readAvailableRXData(data_rcv , available);
      if ((data_rcv[0]==label)&&(data_rcv[1]==label)){//vérification octets premier et second pour controle destinataire
        transmission=1 ;//transmission OK
        lecture_capteur_1=lectureLong( premier_octet,   data_rcv);
        lecture_capteur_2=lectureLong( premier_octet+l, data_rcv);
        float poids_en_gr_distant=((lecture_capteur_1-tare_30kg)/mesure_30kg*etalon_30kg)+((lecture_capteur_2-tare_50kg)/mesure_50kg*etalon_50kg);
        temperature_distant=(data_rcv[premier_octet-1]/2.5-30);//octet troisieme
        temperature_local=temperatureArduino(GAIN_local,OFFSET_local)/2.5-30;
        Serial.print("  poids en gr distant:  *");Serial.print(poids_en_gr_distant);Serial.print(" g *");
        Serial.print("Température local: ");Serial.print(temperature_local);Serial.print("*Température distant:  ");Serial.print(temperature_distant);Serial.print("*");
             
         if (eeprom){ 
           address=sauverDistant(address, data_rcv,octet_par_trame);//on sauve la température distante & deux lecture_capteurs_x sur 9 octets à partir de l'adresse "address" puis 
           //la fonction sauver met à jour la nouvelle adresse de sauvegarde, que l'on écrit sur les octets 1 et 2     
         }
       }
          else {
           Serial.print ("erreur transmission");
           }
      lecture_capteur_1=acquisitionCapteur50kg(tare_50kg,mesure_50kg,etalon_50kg,nombre_point);//fait l'acquisition sur le capteur 50 kg sur une moyenne de nombre_point
    //lecture_capteur_1=acquisitionCapteur30kg(tare_30kg,mesure_30kg,etalon_30kg,nombre_point);//fait l'acquisition sur le capteur 30 kg sur une moyenne de nombre_point
       if (eeprom) {
        address=sauverEntier(address, lecture_capteur_1);//on sauve le poids sur les 4  octets  a partir de l'@ 2    si address<1024, sinon non et on continue à incrémenter address
       }
    miseEnSommeil(); //eteint Arduino
    break;

      case 122 : // RX ET TX ON VA CONFIGURER LE RX; il y a 2 capteurs sur le RX; il y a deux capteurs sur le TX; la trame reçue fait 11 octets : 2 [label]+1 [T]+8 [2 long]
      octet_par_trame=11;
      available = checkifAvailableRXData() ;//debut de cycle piloté par le distant, on attend réception paquet LoRa pour démarrer le cycle
      while (!available){
        available = checkifAvailableRXData() ;
        delay (100);
      }
      readAvailableRXData(data_rcv , available);
      if ((data_rcv[0]==label)&&(data_rcv[1]==label)){//vérification octets premier et second pour controle destinataire
        transmission=1 ;//transmission OK
        lecture_capteur_1=lectureLong( premier_octet,   data_rcv);
        lecture_capteur_2=lectureLong( premier_octet+l, data_rcv);
        long poids_en_gr_distant=((lecture_capteur_1-tare_30kg)/mesure_30kg*etalon_30kg)+((lecture_capteur_2-tare_50kg)/mesure_50kg*etalon_50kg);
        temperature_distant=(data_rcv[premier_octet-1]/2.5-30);//octet troisieme
        temperature_local=temperatureArduino(GAIN_local,OFFSET_local)/2.5-30;
        Serial.print("  poids en gr distant:  *");Serial.print(poids_en_gr_distant);Serial.print(" g *");
        Serial.print("Température local: ");Serial.print(temperature_local);Serial.print("*Température distant:  ");Serial.print(temperature_distant);Serial.print("*");
             
         if (eeprom){ 
           address=sauverDistant(address, data_rcv,octet_par_trame);//on sauve la température distante & deux lecture_capteurs_x sur 9 octets à partir de l'adresse "address" puis 
           //la fonction sauver met à jour la nouvelle adresse de sauvegarde, que l'on écrit sur les octets 1 et 2     
         }
       }
          else {
           Serial.print ("erreur transmission");
           }
      lecture_capteur_1=acquisitionCapteur50kg(tare_50kg,mesure_50kg,etalon_50kg,nombre_point);//fait l'acquisition sur le capteur 50 kg sur une moyenne de nombre_point
      lecture_capteur_2=acquisitionCapteur30kg(tare_30kg,mesure_30kg,etalon_30kg,nombre_point);//fait l'acquisition sur le capteur 30 kg sur une moyenne de nombre_point
       if ((eeprom) && (transmission)) {
        address=sauverEntier(address, lecture_capteur_1);//on sauve le poids sur les 4  octets  a partir de l'@ courante   si address<1024, sinon non et on continue à incrémenter address
        address=sauverEntier(address, lecture_capteur_2);//on sauve le poids sur les 4  octets  a partir de l'@ courante   si address<1024, sinon non et on continue à incrémenter address
       }
      miseEnSommeil(); //eteint Arduino
      break;  
      
      case 201 : // RX ET TX ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a un capteur sur le TX; la trame émise fait 7 octets : 2 [label]+1 [T]+4 [1* long]
        octet_par_trame=7;
        b+=1;
        delay(tempo_lora_demarrage);//le temps que la carte LoRa se mette en marche
        lecture_capteur_1=acquisitionCapteur50kg(tare_50kg,mesure_50kg,etalon_50kg,nombre_point);//fait l'acquisition sur le capteur 50 kg sur une moyenne de nombre_point
      //  lecture_capteur_2=acquisitionCapteur30kg(tare_30kg,mesure_30kg,etalon_30kg,nombre_point);//fait l'acquisition sur le capteur 30 kg sur une moyenne de nombre_point

        data[0] = label; 
        data[1] = EEPROM.read(1023); //numero trame
        data[2] = temperatureArduino(GAIN_distant,OFFSET_distant);//mesure de la température du TX
        data[3] =  lecture_capteur_1 >> 24; // il faut decomposer lecture_capteur_1  en ses 4 octets pour les passer au shield LoRa
        data[4] = (lecture_capteur_1 >> 16) & 0xFF;
        data[5] = (lecture_capteur_1 >>  8) & 0xFF;
        data[6] = (lecture_capteur_1      ) & 0xFF; 
 
        arduinoLoraTXWrite (data,octet_par_trame);
        Serial.print (" T°C :  ");Serial.print (data[2]/2.5-30);Serial.print ("  ");Serial.println (b);
        delay(tempo_lora_emission);
      miseEnSommeil(); //eteint Arduino
      break; 
  
  case 20115 : // RX ET TX ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a un capteur sur le TX; la trame émise fait 5 octets : 2 [label]+1 [T]+2 [1* int]
        octet_par_trame=5;
        b+=1;
        delay(tempo_lora_demarrage);//le temps que la carte LoRa se mette en marche
        lecture_capteur_1=acquisitionCapteur50kg(tare_50kg,mesure_50kg,etalon_50kg,nombre_point);//fait l'acquisition sur le capteur 50 kg sur une moyenne de nombre_point
      //  lecture_capteur_2=acquisitionCapteur30kg(tare_30kg,mesure_30kg,etalon_30kg,nombre_point);//fait l'acquisition sur le capteur 30 kg sur une moyenne de nombre_point

        data[0] = label; 
        data[1] = EEPROM.read(1023); //numero trame
        data[2] = temperatureArduino(GAIN_distant,OFFSET_distant);//mesure de la température du TX
        //data[3] =  lecture_capteur_1 >> 24; // il faut decomposer lecture_capteur_1  en ses 4 octets pour les passer au shield LoRa
        //data[4] = (lecture_capteur_1 >> 16) & 0xFF;
        data[3] = (lecture_capteur_1 >>  8) & 0xFF;// il faut decomposer lecture_capteur_1  en ses 2 octets pour les passer au shield LoRa
        data[4] = (lecture_capteur_1      ) & 0xFF; 
 
        arduinoLoraTXWrite (data,octet_par_trame);
        Serial.print (" T°C :  ");Serial.print (data[2]/2.5-30);Serial.print ("  ");Serial.println (b);
        delay(tempo_lora_emission);
      miseEnSommeil(); //eteint Arduino
      break; 
      
  case 2014 : // RX ET TX ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a quatre capteurs sur le TX mais on ne renvoie que la somme en grammes; la trame émise fait 7 octets : 2 [label/trame]+1 [T]+4 [1 long]
        octet_par_trame=7;
       while (b < b_mesure_par_cycle) 
       { //on va envoyer b mesures pour savoir pourquoi la première mesure est fausse, sur capteurs 4 & 3 en particulier
        b+=1;
        poids_en_gr_total = 0;
        delay(tempo_lora_demarrage);//le temps que la carte LoRa se mette en marche
        lecture_capteur_1=acquisitionCapteur20kg_1(tare_20kg_1,mesure_20kg_1,etalon_20kg_1,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        lecture_capteur_2=acquisitionCapteur20kg_2(tare_20kg_2,mesure_20kg_2,etalon_20kg_2,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        lecture_capteur_3=acquisitionCapteur20kg_3(tare_20kg_3,mesure_20kg_3,etalon_20kg_3,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        lecture_capteur_4=acquisitionCapteur20kg_4(tare_20kg_4,mesure_20kg_4,etalon_20kg_4,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        poids_en_gr_total =(lecture_capteur_1-tare_20kg_1)/mesure_20kg_1*etalon_20kg_1+(lecture_capteur_2-tare_20kg_2)/mesure_20kg_2*etalon_20kg_2+(lecture_capteur_3-tare_20kg_3)/mesure_20kg_3*etalon_20kg_3+(lecture_capteur_4-tare_20kg_4)/mesure_20kg_4*etalon_20kg_4;
        p=abs(poids_en_gr_total);
        Serial.print (" poids_en_gr_total : ");  Serial.print (poids_en_gr_total);  Serial.print (" poids_int : ");Serial.print (p);
        data[0] = label; 
        data[1] = EEPROM.read(1023); //numero trame
        data[2] = temperatureArduino(GAIN_distant,OFFSET_distant);//mesure de la température du TX
        data[3] =  p >> 24; // il faut decomposer poids_en_gr_total  en ses 4 octets pour les passer au shield LoRa
        data[4] = (p >> 16) & 0xFF;
        data[5] = (p >>  8) & 0xFF;
        data[6] = (p      ) & 0xFF; 
        //Serial.print (" data3: ");Serial.print (data[3]);Serial.print (" data4: ");Serial.print (data[4]);Serial.print (" data5: ");Serial.print (data[5]);Serial.print (" data6: ");Serial.print (data[6]);  
        arduinoLoraTXWrite (data,octet_par_trame);
        delay(tempo_lora_emission);
        Serial.print (" T°C: ");Serial.print (data[2]/2.5-30);Serial.print(" numero_trame: ");Serial.print(EEPROM.read(1023));Serial.print (" b: ");Serial.println (b);
       }
      EEPROM.write (1023, data[1] + 1);
      b=0;
      miseEnSommeil(); //eteint Arduino  
      break; 
 
  case 20145 : // RX ET TX ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a quatre capteurs sur le TX mais on ne renvoie que la somme en grammes; la trame émise fait 5 octets : 2 [label]+1 [T]+2 [1* int]
        octet_par_trame=5;
       while (b < b_mesure_par_cycle) 
       { //on va envoyer b mesures pour savoir pourquoi la première mesure est fausse, sur capteurs 4 & 3 en particulier
        b+=1;
        poids_en_gr_total = 0;
        delay(tempo_lora_demarrage);//le temps que la carte LoRa se mette en marche
        lecture_capteur_1=acquisitionCapteur20kg_1(tare_20kg_1,mesure_20kg_1,etalon_20kg_1,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        lecture_capteur_2=acquisitionCapteur20kg_2(tare_20kg_2,mesure_20kg_2,etalon_20kg_2,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        lecture_capteur_3=acquisitionCapteur20kg_3(tare_20kg_3,mesure_20kg_3,etalon_20kg_3,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        lecture_capteur_4=acquisitionCapteur20kg_4(tare_20kg_4,mesure_20kg_4,etalon_20kg_4,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        poids_en_gr_total =(lecture_capteur_1-tare_20kg_1)/mesure_20kg_1*etalon_20kg_1+(lecture_capteur_2-tare_20kg_2)/mesure_20kg_2*etalon_20kg_2+(lecture_capteur_3-tare_20kg_3)/mesure_20kg_3*etalon_20kg_3+(lecture_capteur_4-tare_20kg_4)/mesure_20kg_4*etalon_20kg_4;
        p=abs(poids_en_gr_total);
        Serial.print (" poids_en_gr_total : ");  Serial.print (poids_en_gr_total);  Serial.print (" poids_int : ");Serial.print (p);
        data[0] = label; 
        data[1] = EEPROM.read(1023); //numero trame
        data[2] = temperatureArduino(GAIN_distant,OFFSET_distant);//mesure de la température du TX
        //data[3] =  p >> 24; // il faut decomposer poids_en_gr_total  en ses 4 octets pour les passer au shield LoRa
        //data[4] = (p >> 16) & 0xFF;
        data[3] = (p >>  8) & 0xFF;// il faut decomposer p  en ses 2 octets pour les passer au shield LoRa
        data[4] = (p      ) & 0xFF; 
        arduinoLoraTXWrite (data,octet_par_trame);
        delay(tempo_lora_emission);
        Serial.print (" T°C: ");Serial.print (data[2]/2.5-30);Serial.print(" numero_trame: ");Serial.print(EEPROM.read(1023));Serial.print (" b: ");Serial.println (b);
       }
      EEPROM.write (1023, data[1] + 1);
      b=0;
      miseEnSommeil(); //eteint Arduino  
      break;
 
      
  case 202 : // RX ET TX ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a deux capteurs sur le TX; la trame émise fait 11 octets : 2 [label]+1 [T]+8 [2 long]
        octet_par_trame=11;
        b+=1;
        delay(tempo_lora_demarrage);//le temps que la carte LoRa se mette en marche
        lecture_capteur_1=acquisitionCapteur50kg(tare_50kg,mesure_50kg,etalon_50kg,nombre_point);//fait l'acquisition sur le capteur 50 kg sur une moyenne de nombre_point
        lecture_capteur_2=acquisitionCapteur30kg(tare_30kg,mesure_30kg,etalon_30kg,nombre_point);//fait l'acquisition sur le capteur 30 kg sur une moyenne de nombre_point

        data[0] = label; 
        data[1] = EEPROM.read(1023); //numero trame
        data[2] = temperatureArduino(GAIN_distant,OFFSET_distant);//mesure de la température du TX
        data[3] =  lecture_capteur_1 >> 24; // il faut decomposer lecture_capteur_1  en ses 4 octets pour les passer au shield LoRa
        data[4] = (lecture_capteur_1 >> 16) & 0xFF;
        data[5] = (lecture_capteur_1 >>  8) & 0xFF;
        data[6] = (lecture_capteur_1      ) & 0xFF; 
        data[7] =  lecture_capteur_2 >> 24; // il faut decomposer lecture_capteur_2  en ses 4 octets pour les passer au shield LoRa
        data[8] = (lecture_capteur_2 >> 16) & 0xFF;
        data[9] = (lecture_capteur_2 >>  8) & 0xFF;
        data[10]= (lecture_capteur_2      ) & 0xFF;
 
        arduinoLoraTXWrite (data,octet_par_trame);
        Serial.print (" T°C :  ");Serial.print (data[2]/2.5-30);Serial.print ("  ");Serial.println (b);
        delay(tempo_lora_emission);
      miseEnSommeil(); //eteint Arduino  
      break; 
      
      
      case 204 : // RX ET TX ON VA CONFIGURER LE TX; il y a x capteurs sur le RX; il y a quatre capteurs sur le TX; la trame émise fait 19 octets : 2 [label]+1 [T]+16 [4 long]
        octet_par_trame=19;
       while (b < b_mesure_par_cycle) 
       { //on va envoyer b mesures pour savoir pourquoi la première mesure est fausse, sur capteurs 4 & 3 en particulier
        b+=1;
        delay(tempo_lora_demarrage);//le temps que la carte LoRa se mette en marche
        //lecture_capteur_1=acquisitionCapteur50kg(tare_50kg,mesure_50kg,etalon_50kg,nombre_point);//fait l'acquisition sur le capteur 50 kg sur une moyenne de nombre_point
        //lecture_capteur_2=acquisitionCapteur30kg(tare_30kg,mesure_30kg,etalon_30kg,nombre_point);//fait l'acquisition sur le capteur 30 kg sur une moyenne de nombre_point
        lecture_capteur_1=acquisitionCapteur20kg_1(tare_20kg_1,mesure_20kg_1,etalon_20kg_1,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        lecture_capteur_2=acquisitionCapteur20kg_2(tare_20kg_2,mesure_20kg_2,etalon_20kg_2,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        lecture_capteur_3=acquisitionCapteur20kg_3(tare_20kg_3,mesure_20kg_3,etalon_20kg_3,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        lecture_capteur_4=acquisitionCapteur20kg_4(tare_20kg_4,mesure_20kg_4,etalon_20kg_4,nombre_point);//fait l'acquisition sur le capteur 20 kg sur une moyenne de nombre_point
        data[0] = label; 
        //data[1] = label; 
        data[1] = EEPROM.read(1023); //numero trame
        data[2] = temperatureArduino(GAIN_distant,OFFSET_distant);//mesure de la température du TX
       // data[2] = b;
        data[3] =  lecture_capteur_1 >> 24; // il faut decomposer lecture_capteur_1  en ses 4 octets pour les passer au shield LoRa
        data[4] = (lecture_capteur_1 >> 16) & 0xFF;
        data[5] = (lecture_capteur_1 >>  8) & 0xFF;
        data[6] = (lecture_capteur_1      ) & 0xFF; 
        data[7]  =  lecture_capteur_2 >> 24; // il faut decomposer lecture_capteur_2  en ses 4 octets pour les passer au shield LoRa
        data[8]  = (lecture_capteur_2 >> 16) & 0xFF;
        data[9]  = (lecture_capteur_2 >>  8) & 0xFF;
        data[10] = (lecture_capteur_2      ) & 0xFF;
        data[11] =  lecture_capteur_3 >> 24; // il faut decomposer lecture_capteur_2  en ses 4 octets pour les passer au shield LoRa
        data[12] = (lecture_capteur_3 >> 16) & 0xFF;
        data[13] = (lecture_capteur_3 >>  8) & 0xFF;
        data[14] = (lecture_capteur_3     ) & 0xFF; 
        data[15] =  lecture_capteur_4 >> 24; // il faut decomposer lecture_capteur_2  en ses 4 octets pour les passer au shield LoRa
        data[16] = (lecture_capteur_4 >> 16) & 0xFF;
        data[17] = (lecture_capteur_4 >>  8) & 0xFF;
        data[18] = (lecture_capteur_4     ) & 0xFF;
        arduinoLoraTXWrite (data,octet_par_trame);
        delay(tempo_lora_emission);
        Serial.print (" T°C: ");Serial.print (data[2]/2.5-30);Serial.print(" numero_trame: ");Serial.print(EEPROM.read(1023));Serial.print (" b: ");Serial.println (b);
       }
      EEPROM.write (1023, data[1] + 1);
      b=0;
      miseEnSommeil(); //eteint Arduino  
      break; 
      
      case 301 : // RX: ON VA LIRE L'EEPROM; il y a 0 capteur sur le RX; il y a un capteur sur le TX; la trame EEPROM fait 5 octets : 1[T]+4 [1* long]
 //version 7 octets : label, label, temp, capteur-1#octet_3 ->6
      octet_par_trame=5;
      lecture=lecture+1;//mode lecture
      delay (5000);
      address = adresseCourante();
         if (lecture==1) {
           Serial.print("Addresse:");Serial.print(address);
              if (address+2+octet_par_trame  > EEPROM_LENGTH){
                 address=1022;
                 Serial.print("débordement eeprom");
              }
           Serial.println("");
         }
       while (read_addr < address) {         
         read_addr =  lectureEeprom(read_addr, buf,octet_par_trame);
         int j = 0;
         temperature_distant = buf[j];    Serial.print("temp_TX: ");    Serial.println(temperature_distant);
         
         j=j+1;//on décale de un octet
         long lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= (long)buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_30kg: ");    Serial.println(lecture_capteur);    
     }
      break;

      case 30145 : // RX: ON VA LIRE L'EEPROM; il y a 0 capteur sur le RX; il y a x capteurs sur le TX; la trame EEPROM fait 3 octets : 1[T]+2 [1* int]
 //version 7 octets : label, label, temp, capteur-1#octet_3 ->4
      octet_par_trame=3;
      lecture=lecture+1;//mode lecture
      delay (5000);
      address = adresseCourante();
         if (lecture==1) {
           Serial.print("Addresse:");Serial.print(address);
              if (address+2+octet_par_trame  > EEPROM_LENGTH){
                 address=1022;
                 Serial.print("débordement eeprom");
              }
           Serial.println("");
         }
       while (read_addr < address) {         
         read_addr =  lectureEeprom(read_addr, buf,octet_par_trame);
         int j = 0;
         temperature_distant = buf[j];    Serial.print("temp_TX: ");    Serial.println(temperature_distant);
         
         j=j+1;//on décale de un octet
         long lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= (long)buf[i] << (8*(l-1) - (8*(i-j)));//on recompose le long en concaténant les l octets
           }
       Serial.print("poids en grammes: ");    Serial.println(lecture_capteur);    
     }
      break;
      
      case 302 : // RX: ON VA LIRE L'EEPROM; il y a 0 capteur sur le RX; il y a deux capteurs sur le TX; la trame EEPROM fait 9 octets : 1 [T]+8 [2* long]
 //version 11 octets : label, label, temp, capteur-1#octet_3 ->6, capteur_2#octet_7->10 
      octet_par_trame=9;
      lecture=lecture+1;//mode lecture
      delay (5000);
      address = adresseCourante();
         if (lecture==1) {
           Serial.print("Addresse:");Serial.print(address);
              if (address+2+octet_par_trame  > EEPROM_LENGTH){
               //  address=1022;
                 Serial.print("débordement eeprom");
              }
           Serial.println("");
         }
       while (read_addr < address) {
         read_addr =  lectureEeprom(read_addr, buf,octet_par_trame);
         int j = 0;
         temperature_distant = buf[j];    Serial.print("temp_TX: ");    Serial.println(temperature_distant);
         j=j+1;//on décale de un octet
         long lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= (long)buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_30kg: ");    Serial.println(lecture_capteur);
       j=j+l;//on décale de l(4) octets
       lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= (long)buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_50kg: ");     Serial.println(lecture_capteur);     
     }
      break;


      
      case 304 : // RX: ON VA LIRE L'EEPROM; il y a 0 capteur sur le RX; il y a quatre capteurs sur le TX; la trame EEPROM fait 17 octets : 1 [T]+16 [4* long]
 //version 11 octets : label, label, temp, capteur-1#octet_3 ->6, capteur_2#octet_7->10 
      octet_par_trame=17;
      lecture=lecture+1;//mode lecture
      delay (5000);
      address = adresseCourante();
         if (lecture==1) {
           Serial.print("Adresse ");Serial.print(address);
              if (address+2+octet_par_trame  > EEPROM_LENGTH){
          //       address=1022;
                 Serial.print(": debordement eeprom ");
              }
           Serial.println("");
         }
       while (read_addr < address) {
         read_addr =  lectureEeprom(read_addr, buf,octet_par_trame);
         int j = 0;
         temperature_distant = buf[j];    Serial.print("temp_TX: ");    Serial.println(temperature_distant);
         j=j+1;//on décale de un octet
         long lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= (long)buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_20kg_1: ");    Serial.println(lecture_capteur);
       j=j+l;//on décale de l(4) octets
       lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= (long)buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_20kg_2: ");     Serial.println(lecture_capteur);     
        j=j+l;//on décale de l(4) octets
       lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= (long)buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_20kg_3: ");     Serial.println(lecture_capteur); 
       j=j+l;//on décale de l(4) octets
       lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= (long)buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_20kg_4: ");     Serial.println(lecture_capteur); 
     }
      break;

      case 310 : // RX: ON VA LIRE L'EEPROM; il y a 1 capteur sur le RX; il y a 0 capteur sur le TX; la trame EEPROM fait 4 octets : 4 [1* long]
 //version 7 octets : label, label, temp, capteur-1#octet_3 ->6
      octet_par_trame=4;
      lecture=lecture+1;//mode lecture
      delay (5000);
      address = adresseCourante();
         if (lecture==1) {
           Serial.print("Addresse:");Serial.print(address);
              if (address+2+octet_par_trame  > EEPROM_LENGTH){
               //  address=1022;
                 Serial.print("débordement eeprom");
              }
           Serial.println("");
   
         }
       while (read_addr < address) {
         read_addr =  lectureEeprom(read_addr, buf,octet_par_trame);
         int j = 0;
         long lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= (long)buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_10kg: ");    Serial.println(lecture_capteur);    
     }
      break;
      
      
      case 312 : // RX: ON VA LIRE L'EEPROM; il y a 1 capteur sur le RX; il y a deux capteurs sur le TX; la trame EEPROM fait 13 octets : 1 [T]+12 [3* long]
                 //version 15 octets : label, label, temp->2, capteur_1#octet_3 ->6, capteur_2#octet_7->10 , capteur_3#octet_11->14
      octet_par_trame=13;
      lecture=lecture+1;//mode lecture
      delay (5000);
      address = adresseCourante();
         if (lecture==1) {
           Serial.print("Addresse:");Serial.print(address);
              if (address+2+octet_par_trame  > EEPROM_LENGTH){
               //  address=1022;
                 Serial.print("débordement eeprom");
              }
           Serial.println("");
         }
       while (read_addr < address) {
          read_addr =  lectureEeprom(read_addr, buf,octet_par_trame);
          int j = 0;
          temperature_distant = buf[j];    
          Serial.print("temp_TX: ");    Serial.println(temperature_distant);
    
          j=j+1;//on décale de un octet
          long lecture_capteur = buf[j];
             for (uint8_t i=j;i<l+j;i++) {
              lecture_capteur |= (long)buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
             }
          Serial.print("l_30kg: ");    Serial.println(lecture_capteur);
    
          j=j+l;//on décale de l(4) octets
          lecture_capteur = buf[j];
             for (uint8_t i=j;i<l+j;i++) {
                 lecture_capteur |= (long)buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
             }
          Serial.print("l_50kg: ");     Serial.println(lecture_capteur);
     
          j=j+l;//on décale de l(4) octets
          lecture_capteur = buf[j];
             for (uint8_t i=j;i<l+j;i++) {
                lecture_capteur |= (long)buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
             }
          Serial.print("l_10kg: ");     Serial.println(lecture_capteur);  
      }
    break; 
    

      case 320 : // RX: ON VA LIRE L'EEPROM; il y a 2 capteurS sur le RX; il y a 0 capteur sur le TX; la trame EEPROM fait 8 octets : 4 [2* long]
      octet_par_trame=8;
      lecture=lecture+1;//mode lecture
      delay (5000);
      address = adresseCourante();
         if (lecture==1) {
           Serial.print("Addresse:");Serial.print(address);
              if (address+2+octet_par_trame  > EEPROM_LENGTH){
           //      address=1022;
                 Serial.print("débordement eeprom");
              }
           Serial.println("");
   
         }
       while (read_addr < address) {
         read_addr =  lectureEeprom(read_addr, buf,octet_par_trame);
         int j = 0;
         long lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= (long)buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_50kg: ");    Serial.println(lecture_capteur); 
       
         j = l+j;
         lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_30kg: ");    Serial.println(lecture_capteur);       
     }
      break;
     

      case 340 : // RX: ON VA LIRE L'EEPROM; il y a 4 capteurS sur le RX; il y a 0 capteur sur le TX; la trame EEPROM fait 16 octets : 4 [4* long]
      octet_par_trame=16;
      lecture=lecture+1;//mode lecture
      delay (5000);
      address = adresseCourante();
         if (lecture==1) {
           Serial.print("Adresse:");Serial.print(address);
              if (address+2+octet_par_trame  > EEPROM_LENGTH){
           //      address=1022;
                 Serial.print("debordement eeprom");
              }
           Serial.println("");
   
         }
       while (read_addr < address) {
         read_addr =  lectureEeprom(read_addr, buf,octet_par_trame);
         int j = 0;
         long lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= (long)buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_20kg_1: ");    Serial.println(lecture_capteur); 
       
         j = l+j;
         lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_20kg_2: ");    Serial.println(lecture_capteur);       
         j = l+j;
         lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_20kg_3: ");    Serial.println(lecture_capteur);   
         j = l+j;
         lecture_capteur = buf[j];
           for (uint8_t i=j;i<l+j;i++) {
             lecture_capteur |= buf[i] << (24 - (8*(i-j)));//on recompose le long en concaténant les 4 octets
           }
       Serial.print("l_20kg_4: ");    Serial.println(lecture_capteur);   
     }
      break;   
    
    
    
    
    
 }
Serial.println(" trame suivante ");

}



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

long lectureLong(byte premier_octet, byte data_rcv[4]){//on lit 4 octets avec lesquels on refait un long 
  
        long lecture_capteur = data_rcv[premier_octet];
        for (uint8_t i=premier_octet;i<premier_octet+l;i++) {
            lecture_capteur |= (long)data_rcv[i] << (24 - (8*(i-premier_octet)));//on recompose le long en concaténant les 4 premiers octets
         }
         return lecture_capteur;
}   

long lectureInt(byte premier_octet, byte data_rcv[4]){//on lit 2 octets avec lesquels on refait un int 
  
        int lecture_capteur = data_rcv[premier_octet];
        for (uint8_t i=premier_octet;i<premier_octet+l;i++) {
            lecture_capteur |= (int)data_rcv[i] << (8 - (8*(i-premier_octet)));//on recompose le long en concaténant les 2 premiers octets
         }
         return lecture_capteur;
}

int adresseCourante() {//adresse d'une trame EEPROM, On la lit sur les 2 premiers octets EEPROM
  address = EEPROM.read(0);
  address *= 256; // <=> addresse<<8
  address += EEPROM.read(1); // <=> adress |= EEPROM...
  return address;
}

int lectureEeprom(int adresse, uint8_t buf[19],int octet_par_cycle) {//on lit une trame EEPROM qu'on met dans le tableau buf
  uint8_t i;
  for(i=0;i< octet_par_cycle;i++) {
    buf[i] = EEPROM.read(adresse+i);
   }
    return adresse+i;
}

int sauverOctet(int adresse, uint8_t buf[4]) {// //fonction d'écriture d'un tableau de 4 octets en mémoire EEPROM,retourne la prochaine adresse libre sauf si dépassement
  uint8_t i=0;
    if (adresse+3 <= EEPROM_LENGTH) {
       for(i;i<4;i++) {
        EEPROM.write(adresse+i, buf[i]);
       }
       i=4;
    }   
  EEPROM.write (0, ((adresse+i)>>8) & 0xFF);
  EEPROM.write (1, (adresse+i) & 0xFF);
  return adresse+i;
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
  
  int sauverDistant(int adresse, uint8_t buf[19],int octet_par_trame ) {//fonction d'écriture de octet_par_trame octets (1 temperature, 4 capteur_1, 4 capteur_2, ...) octets en mémoire EEPROM,retourne la prochaine adresse libre sauf si dépassement
  uint8_t i=2;
    if (adresse+octet_par_trame-2 >= EEPROM_LENGTH) {
      i=octet_par_trame;
    }
    for(i;i<octet_par_trame;i++) {//ne stocke pas les deux premiers octets (label)
      EEPROM.write(adresse+i-2, buf[i]);
     }
    EEPROM.write (0, (adresse>>8) & 0xFF);//on sauve l'@ sur octets 0 & 1
    EEPROM.write (1, adresse & 0xFF);
    Serial.print(" adresse: ");Serial.println(adresse); 
    return adresse+octet_par_trame-2;
  }

  int sauverLocal(int adresse, uint8_t buf[4]) {// //fonction d'écriture de quatre (1 capteur_local) octets en mémoire EEPROM,retourne la prochaine adresse libre sauf si dépassement
  uint8_t i=0;
    if (adresse+4+2 >= EEPROM_LENGTH) {
      i=4;
    }
    for(i;i<4;i++) {
      EEPROM.write(adresse+i, buf[i]);
  }
  return adresse+i;
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


