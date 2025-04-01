
// Piny serwo
#define pin_glowa_x 9
#define pin_glowa_y 10
#define pin_oczy_x 11
#define pin_oczy_y 12

#include <Servo.h>
//tablica ktora bedzie przechowywac pozcyje serwo
uint8_t pozycja_docelowa[4];
uint8_t pozycja_aktualna[4]; 
//zmienne pomocnicze
uint8_t pozycja_oczy_x;
uint8_t pozycja_oczy_y;
uint8_t pozycja_glowa_x;
uint8_t pozycja_glowa_y;
//tworzenie obiektow serwomechanizmow
Servo glowa_x;
Servo glowa_y;
Servo oczy_x;
Servo oczy_y;

void setup() {
  Serial.begin(9600);
  //przypisanie pinow do serwo
  glowa_x.attach(pin_glowa_x);
  glowa_y.attach(pin_glowa_y);
  oczy_x.attach(pin_oczy_x);
  oczy_y.attach(pin_oczy_y);
  //przypisanie pozycji bazowych, trzeba jescze sie nad tym zastanowic
  glowa_x.write(90);
  glowa_y.write(90);
  oczy_x.write(90);
  oczy_y.write(90);
  //wysalnie wiadomosci ze arduino gotowe do przyjecia danych
  Serial.println("START");
}

void loop() {
  // Sprawdzamy, czy są dostępne dane
  if (Serial.available() >= 4) {
    // Odczytaj 3 bajty danych, dziala poniewaz przesylamy dane ktore nie przekraczaja 255
    Serial.readBytes(pozycja_docelowa, 4);
    // ustawienie pozycji serw
    bool ruch=true;
    while(ruch){
      ruch=false;
        for(int i=0;i<4;i++){
          if(pozycja_aktualna[i]<pozycja_docelowa[i]){
            pozycja_aktualna[i]++;
            ruch=true;
          }else if(pozycja_aktualna[i]>pozycja_docelowa[i]){
            pozycja_aktualna[i]--;
            ruch=true;
          }
        }
        glowa_x.attach(pozycja_aktualna[0]);
        glowa_y.attach(pozycja_aktualna[1]);
        oczy_x.attach(pozycja_aktualna[2]);
        oczy_y.attach(pozycja_aktualna[3]);
    }
  
    //czekamy chwile, nie wiem czy potrzebne?
    delay(50);
    // ten fragment jest po to aby sprawdzic czy dane zostaly przeslane prawidlowo
    Serial.print("Otrzymano dane: ");
    Serial.print(pozycja_aktualna[0]);
    Serial.print(", ");
    Serial.print(pozycja_aktualna[1]);
    Serial.print(", ");
    Serial.print(pozycja_aktualna[2]);
    Serial.print(", ");
    Serial.println(pozycja_aktualna[3]);
    // Wysłanie potwierdzenia do Python
    Serial.println("OK");
    
    // Wysyłanie informacji o gotowości do odbioru kolejnych danych
    delay(50);  // Opcjonalne opóźnienie dla stabilności
    Serial.println("START");
  }
}
