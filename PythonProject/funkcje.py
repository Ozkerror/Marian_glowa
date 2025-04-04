from enum import Enum
import time

#stworzenie pomocniczego typu danych dla wiekszej przejrzystosci funkcji sprawdz.sektor
class Sektor(Enum):
    SS=1
    SD=2
    SG=3
    LS=4
    LD=5
    LG=6
    PS=7
    PD=8
    PG=9

#funkcja ktora zatrzymuje program i wykonuje sie w kolko poki nie przeslemy przez serial oczekiwanej wiadomosci, dodatkowo sluzy troche jak debuger(sprawdza przeslane wartosci)
def potwierdzenie(rduino, oczekiwana_wiadomosc):
    wiadomosc=""
    while True:
        if rduino.in_waiting > 0: #jesli w buforze odbiorczym znajduja sie jakiekolwiek dane to warunek spelniony
            wiadomosc = rduino.readline().decode().strip() #odczytujemy te dane, dekodujemy ciag bajtow na stringa, usuwamy biale znaki czyli spacje, /r, /n
            print(wiadomosc) #linijka ktora w polaczeniu z programem w C pozwala na sprawdzenie czy dane zostaly przeslane poprawnie.
        if wiadomosc == oczekiwana_wiadomosc:
            break
        time.sleep(0.01) #podobno pomoze uniknac niepotrzebnego obciazenia CPU

#funkcja ktora zajmuje sie przeslaniem danych do arduino
def komunikacja_arduino(arduino, glowa_x, glowa_y, oczy_x, oczy_y, wiad_start, wiad_potwierdzajaca):
    potwierdzenie(arduino, wiad_start) #oczekiwanie na gotowosc arduino
    dane=[glowa_x, glowa_y, oczy_x, oczy_y]
    arduino.write(bytearray(dane)) #przeslanie ciagu bajtow , 1 bajt to jedna pozycja serwa poniewa zawieraja sie one w zakresie od 0 do 255
    potwierdzenie(arduino, wiad_potwierdzajaca) #oczekiwanie na potwierdzenie odbioru danych

#wyznaczanie pozycji serwa ktore steruje oczami
def ruch_oczu(wymiar_twarzy, wymiar_kamery, wspolrzedna_twarzy, wspolczynnik,minimumm, maximum):
    proporcja=(wspolrzedna_twarzy+(wymiar_twarzy/2))/wymiar_kamery
    pozycja=minimumm+(proporcja*(180-minimumm-maximum))
    return int(wspolczynnik*pozycja)

 #wyznaczanie pozycji serwa ktore steruje glowa, jest ona bardziej skomplikowana bo musi wyznaczyc najpierw o ile ma sie przesunac serwo wzgledem poprzedniej pozycji
def ruch_glowy(wymiar_twarzy, wymiar_kamery, wspolrzedna_twarzy, wspolczynnik, poprzednia_pozycja, minimum_pozycja, maximum_pozycja):
    odlegosc_od_srodka=wymiar_kamery/2-(wspolrzedna_twarzy+(wymiar_twarzy/2)) #odleglosc glowy od srodka, ujemna to glowa w prawej polowce, dodatnia to glowa w lewej polowec(analogicznie gora-dol)
    proporcja=odlegosc_od_srodka/(wymiar_kamery/2) #proporcja odleglosc glowy od srodka do wymiaru polowy kamery
    przesuniecie=wspolczynnik*proporcja*90 #wyznaczanie o ile ma sie zmienic pozycja serwa
    if(poprzednia_pozycja+przesuniecie)<minimum_pozycja: #jesli serwo juz sie nie bedzie moglo bardziej przesunac to ustawiamy skrajna wartosc
        return minimum_pozycja
    elif (poprzednia_pozycja+przesuniecie)>maximum_pozycja: #analogia tylko w druga strone
        return maximum_pozycja
    else:
        return int(poprzednia_pozycja+przesuniecie) #jesli wszystko git to pozycja serwa to poprzednia pozycja plus zmiana

#funkcja pomocnicza wyznaczajaca stosunek srodka twarzy do calej dlugosci obrazu
def proporcja_x(x, sz_kamery, sz_glowy):
    srodek_glowy_x = x + (sz_glowy / 2)
    prop_x = srodek_glowy_x / sz_kamery
    return prop_x

#analogia
def proporcja_y(y, w_kamery, w_glowy):
    srodek_glowy_y = y + (w_glowy / 2)
    prop_y = srodek_glowy_y / w_kamery
    return prop_y

    #sprawdzanie czy twarz znajduje sie w konkretnych polach siatki
def sprawdz_sektor(x, sz_kamery, sz_glowy, y, wys_kamery, wys_glowy):
    prop_x=proporcja_x(x, sz_kamery, sz_glowy)
    prop_y=proporcja_y(y, wys_kamery, wys_glowy)
    if(0.2 < prop_x < 0.8 and 0.2 < prop_y < 0.8):
        return Sektor.SS
    if(0.2 < prop_x < 0.8 and prop_y > 0.8):
        return Sektor.SG
    if(0.2 < prop_x < 0.8 and prop_y < 0.2):
        return Sektor.SD
    if(prop_x < 0.2 and 0.2 < prop_y < 0.8):
        return Sektor.LS
    if(prop_x < 0.2 and prop_y > 0.8):
        return Sektor.LG
    if(prop_x < 0.2 and prop_y < 0.2):
        return Sektor.LD
    if(prop_x > 0.8 and 0.2 < prop_y < 0.8):
        return Sektor.PS
    if(prop_x > 0.8 and prop_y > 0.8):
        return Sektor.PG
    if(prop_x > 0.8 and prop_y < 0.2):
        return Sektor.PD