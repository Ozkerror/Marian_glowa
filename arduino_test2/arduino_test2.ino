// Piny PWM, DZIAŁA
#define pin_serwo 11
#include <Servo.h>
// Bufor na dane
uint8_t pozycja[5];
Servo serwo;
Servo serwo2;
void setup() {
  Serial.begin(9600);
  
  serwo.attach(pin_serwo);
  serwo2.attach(12);
  Serial.println("START");
}

void loop() {
  // Sprawdzamy, czy są dostępne dane
  if (Serial.available() >= 5) {
    // Odczytaj 3 bajty danych, dziala poniewaz przesylamy dane ktore nie przekraczaja 255
    for (int i = 0; i < 5; i++) {
      pozycja[i] = Serial.read();
    }
    
    // ustawienie 3 kolejnych pozycji serwa
    for(int i=0; i<5; i++){
      serwo.write(pozycja[i]);
      serwo2.write(pozycja[i]);
      delay(1000);
    }
    
    // ten fragment jest po to aby sprawdzic czy dane zostaly przeslane prawidlowo
    Serial.print("Otrzymano dane: ");
    Serial.print(pozycja[0]);
    Serial.print(", ");
    Serial.print(pozycja[1]);
    Serial.print(", ");
    Serial.print(pozycja[2]);
    Serial.print(", ");
    Serial.print(pozycja[3]);
    Serial.print(", ");
    Serial.println(pozycja[4]);
    
    // Wysłanie potwierdzenia do Python
    Serial.println("OK");
    
    // Wysyłanie informacji o gotowości do odbioru kolejnych danych
    delay(50);  // Opcjonalne opóźnienie dla stabilności
    Serial.println("START");
  }
}
