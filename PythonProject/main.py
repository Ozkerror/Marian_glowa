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
from funkcje import ruch_oczu, ruch_glowy, komunikacja_arduino, Sektor

port='COM3' #tutaj nalezy wpisac port do ktorego podlaczone jest arduino
oczy_kat_lp=0
oczy_kat_gd=0
glowa_kat_lp=0
glowa_kat_gd=0

sektor = 0

poprzedni_czas=0
aktualny_czas=0
prog_czasu = 3 #czas w s przez ktory glowa musi przebywac w jednym z bocznych sektorow aby glowa sie ruszyla
#wspolczynniki potrzebne do odpowiedniego sterowania serwami
o_wspolczynnik_x = 1
o_wspolczynnik_y = 1
g_wspolczynnik_x = 1
g_wspolczynnik_y = 1
odliczanie = 0
#wartosci domyslne w ktorych marian powinien sie ustawic po wlaczeniu programu
domyslne_x_glowy=0
domyslne_y_glowy=0
domyslne_x_oczu=0
domyslne_y_oczu=0
#zmienne w ktorych bedzie przechowywana pozycja serw
pozycja_x_glowy = domyslne_x_glowy
pozycja_y_glowy = domyslne_y_glowy
pozycja_x_oczu = domyslne_x_oczu
pozycja_y_oczu = domyslne_y_oczu
#zakresy serw dla glowy i oczu
minimum_x_glowy=0
maximum_x_glowy=0
minimum_y_glowy=0
maximum_y_glowy=0
minimum_x_oczu=0
maximum_x_oczu=0
minimum_y_oczu=0
maximum_y_oczu=0
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
wys_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Pobranie wysokosci klatki wideo w pikselach
komunikacja_arduino(arduino, domyslne_x_glowy, domyslne_y_glowy, domyslne_x_oczu, domyslne_y_oczu, wiadomosc_startowa, wiadomosc_potwierdzajaca) #ustawienie glowy i oczu w domyslnej pozycji


while True:
    sprawdzenie, klatka = nagranie.read() # Odczytywanie klatek nagrania, jesli sprawdzenie jest false to oznacza koniec nagrania
    if not sprawdzenie:
        break
    szara_klatka = cv2.cvtColor(klatka, cv2.COLOR_BGR2GRAY) # Konwersja obrazu na skale szarosci, klatka - obraz RGB, szara_klatka - nowy obraz w odcienach szarosci
    twarz = face_cascade.detectMultiScale(szara_klatka, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)) # Wykrywanie twarzy, skalowanie obrazu,
    if len(twarz)>0: #obliczenie wykonywane są tylko i wylacznie gdy jakakolwiek twarz jest wykryta
        x, y, sz_twarzy, wys_twarzy = twarz[0]
        sektor=funkcje.sprawdz_sektor(x,sz_kamery,sz_twarzy,y, wys_kamery, wys_twarzy)
        if sektor!=Sektor.SS:
            aktualny_czas=time.perf_counter()
        else:
            poprzedni_czas=aktualny_czas
        if (aktualny_czas-poprzedni_czas)>5:
            #oś x
            pozycja_x_glowy= ruch_glowy(sz_twarzy, sz_kamery, x, o_wspolczynnik_x, pozycja_x_glowy, minimum_x_glowy, maximum_x_glowy)
            #oś y
            pozycja_y_glowy= ruch_glowy(wys_twarzy,wys_kamery,y,g_wspolczynnik_y, pozycja_y_glowy, minimum_y_glowy, maximum_y_glowy)
            #centrowanie oczu
            pozycja_x_oczu=domyslne_x_oczu
            pozycja_y_oczu=domyslne_y_oczu
            #zresetowanie odliczania
            poprzedni_czas=aktualny_czas
        else:
            pozycja_x_oczu=ruch_oczu(sz_twarzy, sz_kamery, x, o_wspolczynnik_x,minimum_x_oczu, maximum_x_oczu)
            pozycja_y_oczu=ruch_oczu(wys_twarzy, wys_kamery, y, o_wspolczynnik_y, minimum_y_oczu, maximum_y_oczu)
        komunikacja_arduino(arduino,pozycja_x_glowy, pozycja_y_glowy, pozycja_x_oczu, pozycja_y_oczu, wiadomosc_startowa, wiadomosc_potwierdzajaca)
    cv2.imshow("nagrywanie", klatka)  # wyswietla klatke w okienku nagrywanie
    if cv2.waitKey(1) & 0xFF == ord('q'):  # pozwolenie uzytkownikowi na zakonczenie dzialania programu poprzez nacisniecie klawisza 'q'
        break
nagranie.release()
cv2.destroyAllWindows()
arduino.close()
