import cv2
import serial
import time


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

def centrowanie(arduino, ser_lp, kat_ser_lp, ser_gd, kat_ser_gd, ser_oko_lp, ser_oko_gd, kat_ser_oko_lp, kat_ser_oko_gd):
    arduino.write(f"{ser_lp}\n".encode())
    potwierdzenie(arduino, "serwo_g_lp")
    time.sleep(0.2)
    arduino.write(f"{kat_ser_lp}\n".encode())
    potwierdzenie(arduino, "kont_g_lp")
    time.sleep(1)

    arduino.write(f"{ser_gd}\n".encode())
    potwierdzenie(arduino, "serwo_g_gd1")
    time.sleep(0.2)
    arduino.write(f"{kat_ser_gd}\n".encode())
    potwierdzenie(arduino, "kont_g_gd1")
    time.sleep(0.2)

    arduino.write(f"{ser_oko_lp}\n".encode())
    potwierdzenie(arduino, "serwo_o_lp")
    time.sleep(0.2)
    arduino.write(f"{kat_ser_oko_lp}\n".encode())
    potwierdzenie(arduino, "kont_o_lp")
    time.sleep(0.2)

    arduino.write(f"{ser_oko_gd}\n".encode())
    potwierdzenie(arduino, "serwo_o_gd")
    time.sleep(0.2)
    arduino.write(f"{kat_ser_oko_gd}\n".encode())
    potwierdzenie(arduino, "kont_o_gd")

def ruch_oczu(wspolczynnik_lp, wspolczynnik_gd, prop_x, prop_y, arduino, oczy_gd, oczy_lp):
    kat_lp = prop_x * 180 * wspolczynnik_lp
    kat_gd = prop_y * 180 * wspolczynnik_gd
    arduino.write(f"{oczy_lp}\n".encode())
    potwierdzenie(arduino, "serwo_o_lp")
    arduino.write(f"{kat_lp}\n".encode())
    potwierdzenie(arduino, "kont_o_lp")
    time.sleep(0.2)
    arduino.write(f"{oczy_gd}\n".encode())
    potwierdzenie(arduino, "serwo_o_gd")
    arduino.write(f"{kat_gd}\n".encode())
    potwierdzenie(arduino, "kont_o_gd")
    time.sleep(0.2)

def ruch_glowy(arduino, wspolczynnik_lp, wspolczynnik_gd, l_kamery, w_kamery, x_twarzy, y_twarzy, serwo_lp, serwo_gd):
    odleglosc_x = x_twarzy - l_kamery / 2
    kat_lp = wspolczynnik_lp * odleglosc_x
    odleglosc_y = y_twarzy - w_kamery / 2
    kat_gd = wspolczynnik_gd * odleglosc_y

    arduino.write(f"{serwo_lp}\n".encode())
    potwierdzenie(arduino, "serwo_g_lp")
    arduino.write(f"{kat_lp}\n".encode())
    potwierdzenie(arduino, "kont_g_lp")
    time.sleep(0.2)
    arduino.write(f"{serwo_gd}\n".encode())
    potwierdzenie(arduino, "serwo_g_gd")
    arduino.write(f"{kat_gd}\n".encode())
    potwierdzenie(arduino, "kont_g_gd")

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
