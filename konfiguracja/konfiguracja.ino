#include <Servo.h>

#define g_x_pin 8
#define g_y_pin1 9
#define g_y_pin2 10
#define o_x_pin 11
#define o_y_pin 12
#define poten_pin 6
#define butt_pin 5
uint8_t pozycja_g_x=90;
uint8_t pozycja_g_y1=90;
uint8_t pozycja_g_y2=90;
uint8_t pozycja_o_x=90;
uint8_t pozycja_o_y=90;
uint8_t pozycja_pot=0;
String wiadomosc="";
unsigned long czas=0;
Servo g_x;
Servo g_y1;
Servo g_y2;
Servo o_x;
Servo o_y;

uint8_t wyznacz_pozycje(void){
  uint8_t pozycja = analogRead(poten_pin)*180/1023;
  return pozycja;
}
void wyswietl_pozycje() {
  Serial.println("g_x = " + String(pozycja_g_x));
  Serial.println("g_y1 = " + String(pozycja_g_y1));
  Serial.println("g_y2 = " + String(pozycja_g_y2));
  Serial.println("o_x = " + String(pozycja_o_x));
  Serial.println("o_y = " + String(pozycja_o_y));
}
void ustaw_serwa() {
  g_x.write(pozycja_g_x);
  g_y1.write(pozycja_g_y1);
  g_y2.write(pozycja_g_y2);
  o_x.write(pozycja_o_x);
  o_y.write(pozycja_o_y);
}
void setup() {
  g_x.attach(g_x_pin);
  g_y1.attach(g_y_pin1);
  g_y2.attach(g_y_pin2);
  o_x.attach(o_x_pin);
  o_y.attach(o_y_pin);
  g_x.write(90);
  g_y1.write(90);
  g_y2.write(90);
  o_x.write(90);
  o_y.write(90);
  Serial.begin(9600);
  pinMode(butt_pin, INPUT_PULLUP);
}

void loop() {
  if(millis()-czas>1000){
    wyswietl_pozycje();
    czas=millis();
  }
  if(Serial.available()>0){
    wiadomosc=Serial.readStringUntil('\n');
    wiadomosc.trim(); //po to aby usunac potencjalne biale znaki takie jak /r ktore moga 
    while(1){
      pozycja_pot=wyznacz_pozycje();
      if(wiadomosc=="gx"){
        pozycja_g_x=pozycja_pot;
      }
      else if (wiadomosc=="gy1"){
        pozycja_g_y1=pozycja_pot;
      }
      else if (wiadomosc=="gy2"){
        pozycja_g_y2=pozycja_pot;
      }
      else if (wiadomosc=="ox"){
        pozycja_o_x=pozycja_pot;
      }
      else if (wiadomosc=="oy"){
        pozycja_o_y=pozycja_pot;
      }
      else break;
      if(millis()-czas>1000){
        wyswietl_pozycje();
        czas=millis();
      }
      ustaw_serwa();
      if(!digitalRead(butt_pin)) break;
    }
  }
}
