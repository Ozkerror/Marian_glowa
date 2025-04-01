// Piny PWM, DZIAŁA
#define pin_serwo_x 8
#define pin_serwo_y 9
#include <Servo.h>
// Bufor na dane
uint8_t pozycja[2]; //tablica ktora bedzie przechowywac pozcyje serwo
Servo serwo_x;
Servo serwo_y;
void setup() {
  Serial.begin(9600);
  serwo_x.attach(pin_serwo_x);
  serwo_y.attach(pin_serwo_y);
  serwo_x.write(90);
  serwo_y.write(90);
  Serial.println("START");
}

void loop() {
  // Sprawdzamy, czy są dostępne dane
  if (Serial.available() >= 2) {
    // Odczytaj 3 bajty danych, dziala poniewaz przesylamy dane ktore nie przekraczaja 255
    for (int i = 0; i < 2; i++) {
      pozycja[i] = Serial.read();
    }
    
    // ustawienie 3 kolejnych pozycji serwa
    serwo_x.write(pozycja[0]);
    serwo_y.write(pozycja[1]);
    delay(300);
    // ten fragment jest po to aby sprawdzic czy dane zostaly przeslane prawidlowo
    Serial.print("Otrzymano dane: ");
    Serial.print(pozycja[0]);
    Serial.print(", ");
    Serial.println(pozycja[1]);
    // Wysłanie potwierdzenia do Python
    Serial.println("OK");
    
    // Wysyłanie informacji o gotowości do odbioru kolejnych danych
    delay(50);  // Opcjonalne opóźnienie dla stabilności
    Serial.println("START");
  }
}
