#include <SoftwareSerial.h> //use for connecting to Bluetooth 
#define ANApin A0 // select the analoge pin connected to sensor, pin A0  
#define Rx 0 //select the reading pin in serial cominucation, pin 1
#define Tx 1 //select the transmiting pin in serial cominucation, pin 0
#define red 11 //pin 11 is connected to red LED
#define infr 12 //pin 12 is connected to infrared LED 

int count[2000];
int value;

// 1000 = 1s

SoftwareSerial Bluetooth(Rx, Tx); //configure the selected pins
void setup() {
  pinMode(red, OUTPUT); //configure pin 11 as an output to connect to the Red LED
  pinMode(infr, OUTPUT); //configure pin 12 as an output to connect to the infrared LED
  digitalWrite(red, LOW); //initially red LED is on
  digitalWrite(infr, LOW); //initially infrared LED is off
  BluetoothSetup(); //setup bluetooth
  Serial.begin(9600); //since we are senidng 10 bits/s thus buad rate = 9600
}

void BluetoothSetup() {
  Bluetooth.begin(9600); //set baud rate of bluetooth or set it to 9600
}

void loop() {
  // put your main code here, to run repeatedly:
  //if (Bluetooth.available())
  //{
    //while (1){
      digitalWrite(infr, LOW); //turn off IR LED
      digitalWrite(red, HIGH); //turn on red LED
      for(int i=0; i<2000; i++) //Collects data for 2s
      {
        count[i] = analogRead(ANApin); 
        value = count[i];
        Serial.println(value);
        }
       
      digitalWrite(infr, HIGH); //turn ON IR LED
      digitalWrite(red, LOW); //turn off red LED
      for(int i=0; i<2000; i++) //Collects data for 2s
      {
        count[i] = analogRead(ANApin); 
        value = count[i];
        Serial.println(value);
        }
       //}
     //}
   }
