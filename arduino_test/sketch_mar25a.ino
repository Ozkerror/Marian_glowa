char tablica[100];
int tablica_int[10];
uint8_t idx=0;

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  if(Serial.available()>0){
  przetworz_wiadomosc(odbierz_wiadomosx());
  }
}
char *odbierz_wiadomosx(){
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
void przetworz_wiadomosc(char * wiadomosc){
  uint8_t idx_wew=0;
  char* token = strtok(wiadomosc, ",");
  while(token!= NULL&&idx_wew<idx){
    tablica_int[idx_wew]=atoi(token);
    idx_wew++;
    token=strtok(NULL, ",");
  }
}