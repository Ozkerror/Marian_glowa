

def srodek(x, sz_twarzy):
    wspolrzedna = x + sz_twarzy / 2
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

def sprawdz_ss(prop_x, prop_y):
    return 0.2 < prop_x < 0.8 and 0.2 < prop_y < 0.8

def sprawdz_sg(prop_x, prop_y):
    return 0.2 < prop_x < 0.8 and prop_y > 0.8

def sprawdz_sd(prop_x, prop_y):
    return 0.2 < prop_x < 0.8 and prop_y < 0.2

def sprawdz_ls(prop_x, prop_y):
    return prop_x < 0.2 and 0.2 < prop_y < 0.8

def sprawdz_lg(prop_x, prop_y):
    return prop_x < 0.2 and prop_y > 0.8

def sprawdz_ld(prop_x, prop_y):
    return prop_x < 0.2 and prop_y < 0.2

def sprawdz_ps(prop_x, prop_y):
    return prop_x > 0.8 and 0.2 < prop_y < 0.8

def sprawdz_pg(prop_x, prop_y):
    return prop_x > 0.8 and prop_y > 0.8

def sprawdz_pd(prop_x, prop_y):
    return prop_x > 0.8 and prop_y < 0.2

def sprawdz_cokolwiek(m, n, o, p, r, s, t, u, w):
    return o or p or r or s or t or u or w or m or n

def centrowanie(arduino, kat_ser_lp, kat_ser_gd, kat_ser_oko_lp, kat_ser_oko_gd, wiadomosc_potwierdzajaca):
    komunikacja_arduino(arduino, kat_ser_lp, kat_ser_gd, kat_ser_oko_lp, kat_ser_oko_gd, wiadomosc_potwierdzajaca)

def ruch_oczu(wspolczynnik_lp, wspolczynnik_gd, prop_x, prop_y):
    kat_lp = prop_x * 180 * wspolczynnik_lp
    kat_gd = prop_y * 180 * wspolczynnik_gd
    return kat_lp, kat_gd

def ruch_glowy(wspolczynnik_lp, wspolczynnik_gd, l_kamery, w_kamery, x_twarzy, y_twarzy):
    odleglosc_x = x_twarzy - l_kamery / 2
    kat_lp = wspolczynnik_lp * odleglosc_x
    odleglosc_y = y_twarzy - w_kamery / 2
    kat_gd = wspolczynnik_gd * odleglosc_y
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
    string_dane = ",".join(map(str, dane)) + "\n" #tworze jednego stringa ktory zawiera kolejne elementy tablicy dane i odziela te dane przecinkami, konczy stringa \n
    arduino.write(string_dane.encode()) #przeslanie stringa przez serial
    potwierdzenie(arduino, wiadomosc_potwierdzajaca)
