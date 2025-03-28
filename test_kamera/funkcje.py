import serial
import time




def potwierdzenie(rduino, oczekiwana_wiadomosc): #funkcja ktora zatrzymuje program i wykonuje sie w kolko poki nie przeslemy przez serial oczekiwanej wiadomosci
    wiadomosc=""
    while True:
        if rduino.in_waiting > 0: #jesli w buforze odbiorczym znajduja sie jakiekolwiek dane to warunek spelniony
            wiadomosc = rduino.readline().decode().strip() #odczytujemy te dane, dekodujemy ciag bajtow na stringa, usuwamy biale znaki czyli spacje, /r, /n
            print(wiadomosc) #linijka ktora w polaczeniu z programem w C pozwala na sprawdzenie czy dane zostaly przeslane poprawnie.
        if wiadomosc == oczekiwana_wiadomosc:
            break
        time.sleep(0.01) #podobno pomoze uniknac niepotrzebnego obciazenia CPU

def pozycja_serwo(wspolrzedna_twarzy, wymiar_twarzy, wymiar_kamery):
    proporcja=(wspolrzedna_twarzy+(wymiar_twarzy/2))/wymiar_kamery
    pozycja=180*proporcja
    return pozycja