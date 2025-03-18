import cv2
import serial
import time


def srodek(x, sz_twarzy):
    wspolrzedna=x+sz_twarzy/2
    return wspolrzedna

def potwierdzenie(arduino, oczekiwana_wiadomosc):
    while True:
        if arduino.in_waiting()>0:
            wiadomosc=arduino.readline().decode().strip()
        if wiadomosc==oczekiwana_wiadomosc:
            break





def pozycja_x(x, sz_kamery, sz_glowy):
    srodek_glowy_X=x+(sz_glowy/2)
    proporcja_X=srodek_glowy_X/sz_kamery
    return proporcja_X
def pozycja_y(y, w_kamery, w_glowy):
    srodek_glowy_Y=y+w_glowy/2
    proporcja_Y=srodek_glowy_Y/w_kamery
    return proporcja_Y
def sprawdz_ss(prop_X, prop_Y):
    return 0.2<prop_X<0.8 and 0.2<prop_Y<0.8
def sprawdz_sg(prop_X, prop_Y):
    return 0.2<prop_X<0.8 and prop_Y>0.8
def sprawdz_sd(prop_X, prop_Y):
    return 0.2<prop_X<0.8 and prop_Y<0.2
def sprawdz_ls(prop_X, prop_Y):
    return prop_X<0.2 and 0.2<prop_Y<0.8
def sprawdz_lg(prop_X, prop_Y):
    return prop_X<0.2 and prop_Y>0.8
def sprawdz_ld(prop_X, prop_Y):
    return prop_X<0.2 and prop_Y<0.2
def sprawdz_ps(prop_X, prop_Y):
    return prop_X>0.8 and 0.2<prop_Y<0.8
def sprawdz_pg(prop_X, prop_Y):
    return prop_X>0.8 and prop_Y>0.8
def sprawdz_pd(prop_X, prop_Y):
    return prop_X>0.8 and prop_Y<0.2
def sprawdz_cokolwiek(M,N,O,P,R,S,T,U,W):
    return O or P or R or S or T or U or W or M or N

def centrowanie(Arduino,ser_LP, kat_ser_LP, ser_GD, kat_ser_GD, ser_oko_LP, ser_oko_GD, kat_ser_oko_LP, kat_ser_oko_GD):
    Arduino.write(f"{ser_LP}\n".encode())
    potwierdzenie(Arduino, "serwo_g_LP")
    time.sleep(0.2)
    Arduino.write(f"{kat_ser_LP}\n".encode())
    potwierdzenie(Arduino, "kont_g_LP")
    time.sleep(1)

    Arduino.write(f"{ser_GD}\n".encode())
    potwierdzenie(Arduino, "serwo_g_GD1")
    time.sleep(0.2)
    Arduino.write(f"{kat_ser_GD}\n".encode())
    potwierdzenie(Arduino, "kont_g_GD1")
    time.sleep(0.2)



    Arduino.write(f"{ser_oko_LP}\n".encode())
    potwierdzenie(Arduino, "serwo_o_LP")
    time.sleep(0.2)
    Arduino.write(f"{kat_ser_oko_LP}\n".encode())
    potwierdzenie(Arduino, "kont_o_LP")
    time.sleep(0.2)

    Arduino.write(f"{ser_oko_GD}\n".encode())
    potwierdzenie(Arduino, "serwo_o_GD")
    time.sleep(0.2)
    Arduino.write(f"{kat_ser_oko_GD}\n".encode())
    potwierdzenie(Arduino, "kont_o_GD")

def ruch_oczu(wspolczynnik_LP, wspolczynnik_GD, prop_X, prop_Y, arduino, oczy_gd, oczy_lp):
    kat_LP=prop_X*180*wspolczynnik_LP
    kat_GD=prop_Y*180*wspolczynnik_GD
    arduino.write(f"{oczy_lp}\n".encode())
    potwierdzenie(arduino, "serwo_o_LP")
    arduino.write(f"{kat_LP}\n".encode())
    potwierdzenie(arduino, "kont_o_LP")
    time.sleep(0.2)
    arduino.write(f"{oczy_gd}\n".encode())
    potwierdzenie(arduino, "serwo_o_GD")
    arduino.write(f"{kat_GD}\n".encode())
    potwierdzenie(arduino, "kont_o_GD")
    time.sleep(0.2)

def ruch_glowy(arduino, wspolczynnik_LP, wspolczynnik_GD,L_kamery, W_kamery, x_twarzy, y_twarzy, Serwo_LP, Serwo_GD):
    odleglosc_X = x_twarzy - L_kamery/2
    kat_LP= wspolczynnik_LP * odleglosc_X
    odleglosc_Y= y_twarzy-W_kamery/2
    kat_GD= wspolczynnik_GD*odleglosc_Y

    arduino.write(f"{Serwo_LP}\n".encode())
    potwierdzenie(arduino, "serwo_g_LP")
    arduino.write(f"{kat_LP}\n".encode())
    potwierdzenie(arduino, "kont_g_LP")
    time.sleep(0.2)
    arduino.write(f"{Serwo_GD}\n".encode())
    potwierdzenie(arduino, "serwo_g_GD")
    arduino.write(f"{kat_GD}\n".encode())
    potwierdzenie(arduino, "kont_g_GD")



def skrajne_l(x, sz_kamery, przedzial):
    polozenie=x/sz_kamery
    return polozenie<przedzial
def skrajne_p(x, sz_twarzy, sz_kamery, przedzial):
    polozenie=(x+sz_twarzy)/sz_kamery
    return polozenie>przedzial
def skrajne_g(y, wys_kamery, przedzial):
    polozenie=y/wys_kamery
    return polozenie<przedzial
def skrajne_d(y, wys_twarzy, wys_kamery, przedzial):
    polozenie=(y+wys_twarzy)/wys_kamery
    return polozenie>przedzial