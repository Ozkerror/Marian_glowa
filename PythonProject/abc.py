
import cv2
import serial
import time
import funkcje
from funkcje import ruch_oczu, ruch_glowy, komunikacja_arduino, Sektor, ruch_glowy_dwa
port='COM5' #tutaj nalezy wpisac port do ktorego podlaczone jest arduino
oczy_kat_lp=0
oczy_kat_gd=0
glowa_kat_lp=0
glowa_kat_gd=0

sektor = 0

czas_wyjscia_z_sektora = None
czy_glowa_ruszyla = False


prog_czasu = 1 #czas w s przez ktory glowa musi przebywac w jednym z bocznych sektorow aby glowa sie ruszyla
#wspolczynniki potrzebne do odpowiedniego sterowania serwami
o_wspolczynnik_x = 1
o_wspolczynnik_y = 1
g_wspolczynnik_x = 1
g_wspolczynnik_y = 1
odliczanie = 0
#wartosci domyslne w ktorych marian powinien sie ustawic po wlaczeniu programu
domyslne_x_glowy=103
domyslne_y_glowy=95
domyslne_x_oczu=90
domyslne_y_oczu=90
#zmienne w ktorych bedzie przechowywana pozycja serw
pozycja_x_glowy = domyslne_x_glowy
pozycja_y_glowy1 = domyslne_y_glowy
pozycja_y_glowy2 = domyslne_y_glowy
pozycja_x_oczu = domyslne_x_oczu
pozycja_y_oczu = domyslne_y_oczu
#zakresy serw dla glowy i oczu
minimum_x_glowy=48
maximum_x_glowy=158
minimum_y_glowy=80
maximum_y_glowy=110
minimum_x_oczu=45
maximum_x_oczu=135
minimum_y_oczu=45
maximum_y_oczu=135
wiadomosc_startowa="START"
wiadomosc_potwierdzajaca="OK"
arduino = serial.Serial(port, 9600) #tworzy obiekt z ktorym bedziemy sie komunikowac



def potwierdzenie(rduino, oczekiwana_wiadomosc):
    wiadomosc=""
    while True:
        if rduino.in_waiting > 0:
            wiadomosc = rduino.readline().decode().strip()
            print(wiadomosc)
        if wiadomosc == oczekiwana_wiadomosc:
            break


def komunikacja_arduino(arduino, glowa_x, glowa_y1, glowa_y2, oczy_x, oczy_y, wiad_start, wiad_potw):
    potwierdzenie(arduino, wiad_start)
    dane=[glowa_x, glowa_y1, glowa_y2, oczy_x, oczy_y]
    arduino.write(bytearray(dane))
    potwierdzenie(arduino, wiad_potw)





arduino = serial.Serial(port, 9600)





