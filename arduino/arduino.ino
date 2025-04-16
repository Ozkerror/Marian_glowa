#define pin_glowa_x 9
#define pin_glowa_y1 10
#define pin_glowa_y2 11
#define pin_oczy_x 12
#define pin_oczy_y 13

#include <Servo.h>

uint8_t pozycja_docelowa[5];
uint8_t pozycja_aktualna[5];

Servo glowa_x;
Servo glowa_y1;
Servo glowa_y2;
Servo oczy_x;
Servo oczy_y;

void ustaw_serwa(void){
  glowa_x.write(pozycja_aktualna[0]);
  glowa_y1.write(pozycja_aktualna[1]);
  glowa_y2.write(pozycja_aktualna[2]);
  oczy_x.write(pozycja_aktualna[3]);
  oczy_y.write(pozycja_aktualna[4]);
}

void wypisz_pozycje(void){
  Serial.print("Otrzymano dane: ");
  Serial.print(pozycja_aktualna[0]);
  Serial.print(", ");
  Serial.print(pozycja_aktualna[1]);
  Serial.print(", ");
  Serial.print(pozycja_aktualna[2]);
  Serial.print(", ");
  Serial.print(pozycja_aktualna[3]);
  Serial.print(", ");
  Serial.println((pozycja_aktualna[4]));
}

void setup() {
  Serial.begin(9600);
  glowa_x.attach(pin_glowa_x);
  glowa_y1.attach(pin_glowa_y1);
  glowa_y2.attach(pin_glowa_y2);
  oczy_x.attach(pin_oczy_x);
  oczy_y.attach(pin_oczy_y);
  glowa_x.write(103);
  glowa_y1.write(95);
  glowa_y2.write(95);
  oczy_x.write(90);
  oczy_y.write(90);
  Serial.println("START");
}

void loop() {
  if (Serial.available() >= 5) {
    Serial.readBytes(pozycja_docelowa, 5);
    bool ruch=true;
    while(ruch){
      ruch=false;
      for(int i=0;i<5;i++){
        if(pozycja_aktualna[i]<pozycja_docelowa[i]){
          pozycja_aktualna[i]++;
          ruch=true;
        }else if(pozycja_aktualna[i]>pozycja_docelowa[i]){
          pozycja_aktualna[i]--;
          ruch=true;
        }
      }
      ustaw_serwa();
      delay(30);
    }
    wypisz_pozycje();
    Serial.println("OK");
    Serial.println("START");
  }
}
