#1 zalaczenie kamerki
#2 centrowanie osoba w obiektywie start rozpoznawania
#3 zcheckowanie polozenia osoby w danym obszarze (prostokacie)ruch_glowy(wys_twarzy,wys_kamery,y,g_wspolczynnik_y, pozycja_y_glowy, minimum_y_glowy, maximum_y_glowy, 45)
#4 marian jezdzi oczami do okreslonego czasu jesli obiekt jest nieruchomy to centruje oczy, dojezdza glowa
#5 jesli osoba wychodzi poza obszar widocznosci to marian jedzie glowa niezaleznie od czasu
#6 obliczenia w pythonie


import cv2
import serial
import time
import funkcje
from funkcje import ruch_oczu, ruch_glowy, komunikacja_arduino, Sektor, ruch_glowy_dwa

port='COM7' #tutaj nalezy wpisac port do ktorego podlaczone jest arduino
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

time.sleep(2)  # zeby sie polaczenie ustabilizowalo
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') # Zaladowanie klasyfikatora, model do wykrywania twarzy
nagranie = cv2.VideoCapture(0)

if not nagranie.isOpened():
    print("nie udalo sie otworzyc kamery")
    exit()

sz_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_WIDTH)) # Pobranie szerokosci klatki wideo w pikselach
wys_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Pobranie wysokosci klatki wideo w pikselach
#komunikacja_arduino(arduino, domyslne_x_glowy, domyslne_y_glowy, domyslne_x_oczu, domyslne_y_oczu, wiadomosc_startowa, wiadomosc_potwierdzajaca) #ustawienie glowy i oczu w domyslnej pozycji


while True:
    sprawdzenie, klatka = nagranie.read() # Odczytywanie klatek nagrania, jesli sprawdzenie jest false to oznacza koniec nagrania
    if not sprawdzenie:
        break
    szara_klatka = cv2.cvtColor(klatka, cv2.COLOR_BGR2GRAY) # Konwersja obrazu na skale szarosci, klatka - obraz RGB, szara_klatka - nowy obraz w odcienach szarosci
    twarz = face_cascade.detectMultiScale(szara_klatka, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)) # Wykrywanie twarzy, skalowanie obrazu,
    if len(twarz)>0: #obliczenie wykonywane są tylko i wylacznie gdy jakakolwiek twarz jest wykryta
        x, y, sz_twarzy, wys_twarzy = twarz[0]
        # Logika czasowa i sektory
        sektor = funkcje.sprawdz_sektor(x, sz_kamery, sz_twarzy, y, wys_kamery, wys_twarzy)
        czas_obecny = time.perf_counter()

        if sektor == Sektor.SS:
            # Twarz jest w środku – resetujemy licznik i przywracamy domyślne ustawienie
            czas_wyjscia_z_sektora = None
            czy_glowa_ruszyla = False

            # Resetuj oczy do centrum, jeśli głowa nie jest na krańcu
            if pozycja_x_glowy <= minimum_x_glowy or pozycja_x_glowy >= maximum_x_glowy:
                pozycja_x_oczu = ruch_oczu(sz_twarzy, sz_kamery, x, o_wspolczynnik_x, minimum_x_oczu, maximum_x_oczu)
            else:
                pozycja_x_oczu = domyslne_x_oczu

            if pozycja_y_glowy1 <= minimum_y_glowy or pozycja_y_glowy1 >= maximum_y_glowy:
                pozycja_y_oczu = ruch_oczu(wys_twarzy, wys_kamery, y, o_wspolczynnik_y, minimum_y_oczu, maximum_y_oczu)
            else:
                pozycja_y_oczu = domyslne_y_oczu

        else:
            # Twarz nie jest w sektorze SS
            if czas_wyjscia_z_sektora is None:
                czas_wyjscia_z_sektora = czas_obecny

            # Jeżeli przekroczył czas 2s – ruszamy głową i oczy się centrować nie muszą
            if (czas_obecny - czas_wyjscia_z_sektora > 2.0) and not czy_glowa_ruszyla:
                pozycja_x_glowy = ruch_glowy(sz_twarzy, sz_kamery, x, o_wspolczynnik_x, pozycja_x_glowy,
                                             minimum_x_glowy, maximum_x_glowy, 8)
                pozycja_y_glowy1 = ruch_glowy(wys_twarzy, wys_kamery, y, g_wspolczynnik_y, pozycja_y_glowy1,
                                              minimum_y_glowy, maximum_y_glowy, 8)
                pozycja_y_glowy2 = ruch_glowy_dwa(wys_twarzy, wys_kamery, y, g_wspolczynnik_y, pozycja_y_glowy2,
                                                  minimum_y_glowy, maximum_y_glowy, 8)
                czy_glowa_ruszyla = True

            # Dopóki głowa się nie ruszy – ruszamy oczami
            if not czy_glowa_ruszyla:
                pozycja_x_oczu = ruch_oczu(sz_twarzy, sz_kamery, x, o_wspolczynnik_x, minimum_x_oczu, maximum_x_oczu)
                pozycja_y_oczu = ruch_oczu(wys_twarzy, wys_kamery, y, o_wspolczynnik_y, minimum_y_oczu, maximum_y_oczu)

        # Wysyłamy pozycje do Arduino

        komunikacja_arduino(arduino, pozycja_x_glowy, pozycja_y_glowy1, pozycja_y_glowy2, pozycja_x_oczu,
                            pozycja_y_oczu, wiadomosc_startowa, wiadomosc_potwierdzajaca)

    #resetuje czas jesli zadna twarz nie znalazla sie w kamerze
    aktualny_czas=time.perf_counter()
    cv2.imshow("nagrywanie", klatka)  # wyswietla klatke w okienku nagrywanie
    if cv2.waitKey(1) & 0xFF == ord('q'):  # pozwolenie uzytkownikowi na zakonczenie dzialania programu poprzez nacisniecie klawisza 'q'
        break
nagranie.release()
cv2.destroyAllWindows()
arduino.close()
