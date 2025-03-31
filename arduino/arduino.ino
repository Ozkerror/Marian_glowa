
// Piny serwo
#define pin_glowa_x 9
#define pin_glowa_y 10
#define pin_oczy_x 11
#define pin_oczy_y 12

#include <Servo.h>
//tablica ktora bedzie przechowywac pozcyje serwo
uint8_t pozycja[4]; 
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
    Serial.readBytes(pozycja, 4);
    
    // ustawienie pozycji serw
    glowa_x.write(pozycja[0]);
    glowa_y.write(pozycja[1]);
    oczy_x.write(pozycja[2]);
    oczy_y.write(pozycja[3]);
    //czekamy chwile, nie wiem czy potrzebne?
    delay(50);
    // ten fragment jest po to aby sprawdzic czy dane zostaly przeslane prawidlowo
    Serial.print("Otrzymano dane: ");
    Serial.print(pozycja[0]);
    Serial.print(", ");
    Serial.print(pozycja[1]);
    Serial.print(", ");
    Serial.print(pozycja[2]);
    Serial.print(", ");
    Serial.println(pozycja[3]);
    // Wysłanie potwierdzenia do Python
    Serial.println("OK");
    
    // Wysyłanie informacji o gotowości do odbioru kolejnych danych
    delay(50);  // Opcjonalne opóźnienie dla stabilności
    Serial.println("START");
  }
}
