#1 zalaczenie kamerki
#2 centrowanie osoba w obiektywie start rozpoznawania
#3 zcheckowanie polozenia osoby w danym obszarze (prostokacie)
#4 marian jezdzi oczami do okreslonego czasu jesli obiekt jest nieruchomy to centruje oczy, dojezdza glowa
#5 jesli osoba wychodzi poza obszar widocznosci to marian jedzie glowa niezaleznie od czasu
#6 obliczenia w pythonie


import cv2
import serial
import time
import funkcje
from funkcje import ruch_oczu, ruch_glowy, komunikacja_arduino

port='COM3' #tutaj nalezy wpisac port do ktorego podlaczone jest arduino
oczy_kat_lp=0
oczy_kat_gd=0
glowa_kat_lp=0
glowa_kat_gd=0

sektor = 0
start = 0
poprzedni = 0

czas_glowa = 3 #czas w s przez ktory glowa musi przebywac w jednym z bocznych sektorow aby glowa sie ruszyla
#wspolczynniki potrzebne do odpowiedniego sterowania serwami
o_wspolczynnik_lp = 1
o_wspolczynnik_gd = 1
g_wspolczynnik_lp = 1
g_wspolczynnik_gd = 1
odliczanie = 0
#wartosci domyslne w ktorych marian powinien sie ustawic po wlaczeniu programu
domyslne_x_glowy=0
domyslne_y_glowy=0
domyslne_x_oczu=0
domyslne_y_oczu=0

wiadomosc_startowa="START"
wiadomosc_potwierdzajaca="OK"
arduino = serial.Serial(port, 9600) #tworzy obiekt z ktorym bedziemy sie komunikowac

time.sleep(2)  # zeby sie polaczenie ustabilizowalo
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') # Zaladowanie klasyfikatora, model do wykrywania twarzy
nagranie = cv2.VideoCapture(0)

if not nagranie.isOpened():
    print("nie udalo sie otworzyc kamery")
    exit()

sz_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_WIDTH)) # Pobranie szerokosci klatki wideo w pikselach
w_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Pobranie wysokosci klatki wideo w pikselach
komunikacja_arduino(arduino, domyslne_x_glowy, domyslne_y_glowy, domyslne_x_oczu, domyslne_y_oczu, wiadomosc_startowa, wiadomosc_potwierdzajaca) #ustawienie glowy i oczu w domyslnej pozycji


while True:
    sprawdzenie, klatka = nagranie.read() # Odczytywanie klatek nagrania, jesli sprawdzenie jest false to oznacza koniec nagrania
    if not sprawdzenie:
        break
    szara_klatka = cv2.cvtColor(klatka, cv2.COLOR_BGR2GRAY) # Konwersja obrazu na skale szarosci, klatka - obraz RGB, szara_klatka - nowy obraz w odcienach szarosci
    twarz = face_cascade.detectMultiScale(szara_klatka, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)) # Wykrywanie twarzy, skalowanie obrazu,


nagranie.release()
cv2.destroyAllWindows()
arduino.close()

#if odliczanie>=czas_glowa:
            #odliczanie=0
            #rusza glowa
            #srodkowanie oczu
            #time.sleep(2)

        #podazanie oczami
