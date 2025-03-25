#include <Servo.h>

char tablica[100];
int tablica_int[5];
bool wiadomoscPrzetworzona=false;
uint8_t idx=0;
#define pin_serwo1 11
Servo serwo1;
void setup() {
  Serial.begin(9600);
  serwo1.attach(pin_serwo1);

}

void loop() {
  
      char *wiadomosc = odbierz_wiadomosc();
      if(wiadomosc != NULL){
      przetworz_wiadomosc(wiadomosc);
      for(int i=0; i<5; i++){
        serwo1.write(tablica_int[i]);
        delay(1000);
      }
      Serial.println("OK");
  }
}
char *odbierz_wiadomosc(){
  if(Serial.available()>0){
    char znak= Serial.read();
    idx=0;
    while(znak!='\n'&&Serial.available()>0){
      tablica[idx]=znak;
      znak=Serial.read();
      idx++;
    }
    tablica[idx]='\0';
    return tablica;
  }else return NULL;
}
void przetworz_wiadomosc(char  *wiadomosc){
  uint8_t idx_wew=0;
  char* token = strtok(wiadomosc, ",");
  while(token!= NULL&&idx_wew<idx){
    tablica_int[idx_wew]=atoi(token);
    idx_wew++;
    token=strtok(NULL, ",");
  }
}