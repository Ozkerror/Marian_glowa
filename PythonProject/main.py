import cv2
import serial
import time
import funkcje
from funkcje import ruch_oczu, ruch_glowy, komunikacja_arduino, Sektor, ruch_glowy_dwa

port = 'COM5'
oczy_kat_lp = 0
oczy_kat_gd = 0
glowa_kat_lp = 0
glowa_kat_gd = 0

sektor = 0

czas_wyjscia_z_sektora = None
czy_glowa_ruszyla = False

prog_czasu = 1
o_wspolczynnik_x = 1
o_wspolczynnik_y = 1
g_wspolczynnik_x = 1
g_wspolczynnik_y = 1
odliczanie = 0

domyslne_x_glowy = 103
domyslne_y_glowy = 95
domyslne_x_oczu = 90
domyslne_y_oczu = 90

pozycja_x_glowy = domyslne_x_glowy
pozycja_y_glowy1 = domyslne_y_glowy
pozycja_y_glowy2 = domyslne_y_glowy
pozycja_x_oczu = domyslne_x_oczu
pozycja_y_oczu = domyslne_y_oczu

minimum_x_glowy = 48
maximum_x_glowy = 158
minimum_y_glowy = 80
maximum_y_glowy = 110
minimum_x_oczu = 45
maximum_x_oczu = 135
minimum_y_oczu = 45
maximum_y_oczu = 135

wiadomosc_startowa = "START"
wiadomosc_potwierdzajaca = "OK"

arduino = serial.Serial(port, 9600)
time.sleep(2)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
nagranie = cv2.VideoCapture(1)
if not nagranie.isOpened():
    print("nie udalo sie otworzyc kamery")
    exit()

sz_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_WIDTH))
wys_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_HEIGHT))

czas_obecny = time.perf_counter()
czas_poprzedni = time.perf_counter()

while True:
    sprawdzenie, klatka = nagranie.read()
    if not sprawdzenie:
        break

    szara_klatka = cv2.cvtColor(klatka, cv2.COLOR_BGR2GRAY)
    twarz = face_cascade.detectMultiScale(szara_klatka, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(twarz) > 0:
        x, y, sz_twarzy, wys_twarzy = twarz[0]
        sektor = funkcje.sprawdz_sektor(x, sz_kamery, sz_twarzy, y, wys_kamery, wys_twarzy)
        cv2.rectangle(klatka, (x, y), (x + sz_twarzy, y + wys_twarzy), (0, 255, 0), 2)

        if sektor == Sektor.SS:
            pozycja_x_oczu = ruch_oczu(sz_twarzy, sz_kamery, x, o_wspolczynnik_x, minimum_x_oczu, maximum_x_oczu)
            pozycja_y_oczu = ruch_oczu(wys_twarzy, wys_kamery, y, o_wspolczynnik_y, minimum_y_oczu, maximum_y_oczu)
            czas_obecny = time.perf_counter()
            czas_poprzedni = time.perf_counter()
        else:
            czas_obecny = time.perf_counter()
            if (czas_obecny - czas_poprzedni) > 0.5:
                pozycja_x_glowy = ruch_glowy_dwa(sz_twarzy, sz_kamery, x, o_wspolczynnik_x, pozycja_x_glowy, minimum_x_glowy, maximum_x_glowy, 20)
                pozycja_y_glowy1 = ruch_glowy(wys_twarzy, wys_kamery, y, g_wspolczynnik_y, pozycja_y_glowy1, minimum_y_glowy, maximum_y_glowy, 8)
                pozycja_y_glowy2 = ruch_glowy_dwa(wys_twarzy, wys_kamery, y, g_wspolczynnik_y, pozycja_y_glowy2, minimum_y_glowy, maximum_y_glowy, 8)
                czas_poprzedni = time.perf_counter()

                if pozycja_x_glowy <= minimum_x_glowy or pozycja_x_glowy >= maximum_x_glowy:
                    pozycja_x_oczu = ruch_oczu(sz_twarzy, sz_kamery, x, o_wspolczynnik_x, minimum_x_oczu, maximum_x_oczu)
                else:
                    pozycja_x_oczu = domyslne_x_oczu

                if pozycja_y_glowy1 <= minimum_y_glowy or pozycja_y_glowy1 >= maximum_y_glowy:
                    pozycja_y_oczu = ruch_oczu(wys_twarzy, wys_kamery, y, o_wspolczynnik_y, minimum_y_oczu, maximum_y_oczu)
                else:
                    pozycja_y_oczu = domyslne_y_oczu
            else:
                pozycja_x_oczu = ruch_oczu(sz_twarzy, sz_kamery, x, o_wspolczynnik_x, minimum_x_oczu, maximum_x_oczu)
                pozycja_y_oczu = ruch_oczu(wys_twarzy, wys_kamery, y, o_wspolczynnik_y, minimum_y_oczu, maximum_y_oczu)

        komunikacja_arduino(arduino, pozycja_x_glowy, pozycja_y_glowy1, pozycja_y_glowy2, pozycja_x_oczu, pozycja_y_oczu, wiadomosc_startowa, wiadomosc_potwierdzajaca)

    cv2.imshow("nagrywanie", klatka)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

nagranie.release()
cv2.destroyAllWindows()
arduino.close()
