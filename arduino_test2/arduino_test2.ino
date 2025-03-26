// Piny PWM
#define pin_serwo 11
#include <Servo.h>
// Bufor na dane
uint8_t pozycja[3];
Servo serwo;
void setup() {
  Serial.begin(9600);
  
  serwo.attach(pin_serwo);
  Serial.println("START");
}

void loop() {
  // Sprawdzamy, czy są dostępne dane
  if (Serial.available() >= 3) {
    // Odczytaj 3 bajty danych, dziala poniewaz przesylamy dane ktore nie przekraczaja 255
    for (int i = 0; i < 3; i++) {
      pozycja[i] = Serial.read();
    }
    
    // ustawienie 3 kolejnych pozycji serwa
    for(int i=0; i<3; i++){
      serwo.write(pozycja[i]);
      delay(1000);
    }
    
    // ten fragment jest po to aby sprawdzic czy dane zostaly przeslane prawidlowo
    Serial.print("Otrzymano dane: ");
    Serial.print(pozycja[0]);
    Serial.print(", ");
    Serial.print(pozycja[1]);
    Serial.print(", ");
    Serial.println(pozycja[2]);
    
    // Wysłanie potwierdzenia do Python
    Serial.println("OK");
    
    // Wysyłanie informacji o gotowości do odbioru kolejnych danych
    delay(50);  // Opcjonalne opóźnienie dla stabilności
    Serial.println("START");
  }
}
