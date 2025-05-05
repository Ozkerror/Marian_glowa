
// Piny serwo
#define pin_glowa_x 9
#define pin_glowa_y1 10
#define pin_glowa_y2 11
#define pin_oczy_x 12
#define pin_oczy_y 13

#include <Servo.h>
//tablica ktora bedzie przechowywac pozcyje serwo
uint8_t pozycja_docelowa[5]={103, 95, 95, 90, 90} ;
uint8_t pozycja_aktualna[5]={103, 95, 95, 90, 90}; 
//zmienne pomocnicze
uint8_t pozycja_oczy_x;
uint8_t pozycja_oczy_y;
uint8_t pozycja_glowa_x;
uint8_t pozycja_glowa_y1;
uint8_t pozycja_glowa_y2;
uint8_t A=0;
//tworzenie obiektow serwomechanizmow
Servo glowa_x;
Servo glowa_y1;
Servo glowa_y2;
Servo oczy_x;
Servo oczy_y;

void czekaj_na_go(void){
  String dane="";
  while(true){
    if(Serial.available()>0){
      char znak = Serial.read();
      if(znak == '\r' || znak == '\n'){
        dane.trim();
        if(dane=="GO"){
          Serial.println("READY");
          break;
        }else{
          dane="";
        }
      }else{
        dane+=znak;
      }
    }
  }
}

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
  //przypisanie pinow do serwo
  glowa_x.attach(pin_glowa_x);
  glowa_y1.attach(pin_glowa_y1);
  glowa_y2.attach(pin_glowa_y2);
  oczy_x.attach(pin_oczy_x);
  oczy_y.attach(pin_oczy_y);
  //przypisanie pozycji bazowych, trzeba jescze sie nad tym zastanowic
  glowa_x.write(103);
  glowa_y1.write(95);
  glowa_y2.write(95);
  oczy_x.write(90);
  oczy_y.write(90);
  //wysalnie wiadomosci ze arduino gotowe do przyjecia danych
  Serial.println("START");
  czekaj_na_go();
}

void loop() {
  
  // Sprawdzamy, czy są dostępne dane
  if (Serial.available() >= 5) {

    // Odczytaj 5 bajtow danych, dziala poniewaz przesylamy dane ktore nie przekraczaja 255
    Serial.readBytes(pozycja_docelowa, 5);
    // ustawienie pozycji serw
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
    // ten fragment jest po to aby sprawdzic czy dane zostaly przeslane prawidlowo
    wypisz_pozycje();
    // Wysłanie potwierdzenia do Python
    Serial.println("OK");
    // Wysyłanie informacji o gotowości do odbioru kolejnych danych
    delay(50);  // Opcjonalne opóźnienie dla stabilności
    
  }
}
