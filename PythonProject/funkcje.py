from enum import Enum
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


#wyznaczanie wspolrzednej srodka twarzy,
def srodek(x, wymiar_twarzy):
    wspolrzedna = x + wymiar_twarzy / 2
    return wspolrzedna

def potwierdzenie(arduino, oczekiwana_wiadomosc):
    wiadomosc=""
    while True:
        if arduino.in_waiting() > 0:
            wiadomosc = arduino.readline().decode().strip()
        if wiadomosc == oczekiwana_wiadomosc:
            break

def pozycja_x(x, sz_kamery, sz_glowy):
    srodek_glowy_x = x + (sz_glowy / 2)
    proporcja_x = srodek_glowy_x / sz_kamery
    return proporcja_x

def pozycja_y(y, w_kamery, w_glowy):
    srodek_glowy_y = y + w_glowy / 2
    proporcja_y = srodek_glowy_y / w_kamery
    return proporcja_y

    #sprawdzanie czy twarz znajduje sie w konkretnych polach siatki
def sprawdz_sektor(prop_x, prop_y):
    if(0.2 < prop_x < 0.8 and prop_y > 0.8):
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
#troche niepotrzebna funkcja, ale polega ona na wpisaniu konkretnych polozen serw na sztywno
def centrowanie(arduino, kat_ser_lp, kat_ser_gd, kat_ser_oko_lp, kat_ser_oko_gd, wiadomosc_potwierdzajaca):
    komunikacja_arduino(arduino, kat_ser_lp, kat_ser_gd, kat_ser_oko_lp, kat_ser_oko_gd, wiadomosc_potwierdzajaca)

def ruch_oczu(wspolczynnik_lp, wspolczynnik_gd, prop_x, prop_y):
    kat_lp = int(prop_x * 180 * wspolczynnik_lp)
    kat_gd = int(prop_y * 180 * wspolczynnik_gd)
    return kat_lp, kat_gd

def ruch_glowy(wspolczynnik_lp, wspolczynnik_gd, l_kamery, w_kamery, x_twarzy, y_twarzy):
    odleglosc_x = (x_twarzy - l_kamery / 2)/(l_kamery/2)#liczymy odleglosc twarzy od srodka kamery
    kat_lp = int(wspolczynnik_lp * odleglosc_x*180)
    odleglosc_y = (y_twarzy - w_kamery / 2)/(w_kamery/2)
    kat_gd = int(wspolczynnik_gd * odleglosc_y*180)
    return kat_lp, kat_gd

def skrajne_l(x, sz_kamery, przedzial):
    polozenie = x / sz_kamery
    return polozenie < przedzial

def skrajne_p(x, sz_twarzy, sz_kamery, przedzial):
    polozenie = (x + sz_twarzy) / sz_kamery
    return polozenie > przedzial

def skrajne_g(y, wys_kamery, przedzial):
    polozenie = y / wys_kamery
    return polozenie < przedzial

def skrajne_d(y, wys_twarzy, wys_kamery, przedzial):
    polozenie = (y + wys_twarzy) / wys_kamery
    return polozenie > przedzial
def komunikacja_arduino(arduino, glowa_lp, glowa_gd, oczy_lp, oczy_gd, wiadomosc_potwierdzajaca):
    dane=[glowa_lp, glowa_gd, oczy_lp, oczy_gd]
    arduino.write(bytearray(dane)) #przeslanie ciagu bajtow
    potwierdzenie(arduino, wiadomosc_potwierdzajaca)
