import cv2
import serial
import time
import funkcje
from funkcje import ruch_oczu, ruch_glowy, komunikacja_arduino, Sektor, ruch_glowy_dwa, rozrusznik

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
A=0
time.sleep(2)  # zeby sie polaczenie ustabilizowalo
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') # Zaladowanie klasyfikatora, model do wykrywania twarzy
nagranie = cv2.VideoCapture(0)
rozrusznik(arduino, wiadomosc_startowa, "READY")
if not nagranie.isOpened():
    print("nie udalo sie otworzyc kamery")
    exit()

sz_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_WIDTH)) # Pobranie szerokosci klatki wideo w pikselach
wys_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Pobranie wysokosci klatki wideo w pikselach
#komunikacja_arduino(arduino, domyslne_x_glowy, domyslne_y_glowy, domyslne_x_oczu, domyslne_y_oczu, wiadomosc_startowa, wiadomosc_potwierdzajaca) #ustawienie glowy i oczu w domyslnej pozycji
czas_obecny = time.perf_counter()
czas_poprzedni = time.perf_counter()

while True:
    sprawdzenie, klatka = nagranie.read() # Odczytywanie klatek nagrania, jesli sprawdzenie jest false to oznacza koniec nagrania
    if not sprawdzenie:
        break
    szara_klatka = cv2.cvtColor(klatka, cv2.COLOR_BGR2GRAY) # Konwersja obrazu na skale szarosci, klatka - obraz RGB, szara_klatka - nowy obraz w odcienach szarosci
    twarz = face_cascade.detectMultiScale(szara_klatka, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)) # Wykrywanie twarzy, skalowanie obrazu,
    if len(twarz)>0: #obliczenie wykonywane są tylko i wylacznie gdy jakakolwiek twarz jest wykryta
        #wyciagnij dane z krotki twarz
        x, y, sz_twarzy, wys_twarzy = twarz[0]
        #sprawdz w jakim sektorze znajduje sie twarz i przypisz wartosc odpowiadajaca danemu sektorowi do zmiennej sektor
        sektor = funkcje.sprawdz_sektor(x, sz_kamery, sz_twarzy, y, wys_kamery, wys_twarzy)
        cv2.rectangle(klatka, (x, y), (x + sz_twarzy, y + wys_twarzy), (0, 255, 0), 2)
        #LOGIKA CZASOWA
        #perf_counter zwraca czas dzialania programu w sekundach. Aby odmierzac czas to korzystam z dwoch zmiennych pomocniczyc , czas_poprzedni i czas_aktualny
        #jesli chce zresetowac czas to przypisuje perf_counter do zmiennej czas_poprzedni, jesli chce zaczac odliczanie to przypisuje perf_counter do zmiennej czas_aktualny upewniajac
        #sie z w miedzy czasie nie przypisze nic do zmiennej poprzedni_czas aby nie zresetowac odliczanie

        #jesli twarz w srodkowym sektorze to wyznacz pozycje oczu i zrownaj ze soba czas_obecny i czas_poprzedni
        if sektor == Sektor.SS:
            pozycja_x_oczu = ruch_oczu(sz_twarzy, sz_kamery, x, o_wspolczynnik_x, minimum_x_oczu, maximum_x_oczu)
            pozycja_y_oczu = ruch_oczu(wys_twarzy, wys_kamery, y, o_wspolczynnik_y, minimum_y_oczu, maximum_y_oczu)
            czas_obecny=time.perf_counter()
            czas_poprzedni=time.perf_counter()
        #jesli twarz nie znajduje sie w srodkowym sektorze
        else:
            czas_obecny=time.perf_counter()
            #jesli odliczonny czas wiekszy od 3 sekund to ustaw glowe w odpowiedniej pozycji
            if(czas_obecny-czas_poprzedni)>0.2:
                pozycja_x_glowy = ruch_glowy_dwa(sz_twarzy, sz_kamery, x, o_wspolczynnik_x, pozycja_x_glowy, minimum_x_glowy, maximum_x_glowy, 15)
                pozycja_y_glowy1 = ruch_glowy_dwa(wys_twarzy, wys_kamery, y, g_wspolczynnik_y, pozycja_y_glowy1, minimum_y_glowy, maximum_y_glowy, 8)
                pozycja_y_glowy2 = ruch_glowy(wys_twarzy, wys_kamery, y, g_wspolczynnik_y, pozycja_y_glowy2, minimum_y_glowy, maximum_y_glowy, 8)
                #zresetuj odliczanie
                czas_poprzedni=time.perf_counter()
                #jesli glowa w skrajnych pozycjach to wtedy ruszamy normalnie oczami
                if pozycja_x_glowy <= minimum_x_glowy or pozycja_x_glowy >= maximum_x_glowy:
                    pozycja_x_oczu = ruch_oczu(sz_twarzy, sz_kamery, x, o_wspolczynnik_x, minimum_x_oczu, maximum_x_oczu)
                #jesli glowa nie w skrajnej pozycji to zakladamy ze glowa dojedzie mniej wiecej na wprost czyjejs twarzy, wiec oczy wracaja do pozycji bazowej
                else:
                    pozycja_x_oczu = domyslne_x_oczu
                if pozycja_y_glowy1 <= minimum_y_glowy or pozycja_y_glowy1 >= maximum_y_glowy:
                    pozycja_y_oczu = ruch_oczu(wys_twarzy, wys_kamery, y, o_wspolczynnik_y, minimum_y_oczu, maximum_y_oczu)
                else:
                    pozycja_y_oczu = domyslne_y_oczu
            #jesli twarz jest niewystarczajaco dlugo poza srodkowym polem to normalnie rusza tylko oczami
            else:
                pozycja_x_oczu = ruch_oczu(sz_twarzy, sz_kamery, x, o_wspolczynnik_x, minimum_x_oczu, maximum_x_oczu)
                pozycja_y_oczu = ruch_oczu(wys_twarzy, wys_kamery, y, o_wspolczynnik_y, minimum_y_oczu, maximum_y_oczu)
        #wyslij dane do arduino
            komunikacja_arduino(arduino, pozycja_x_glowy, pozycja_y_glowy1, pozycja_y_glowy2, pozycja_x_oczu, pozycja_y_oczu, wiadomosc_potwierdzajaca)
    cv2.imshow("nagrywanie", klatka)  # wyswietla klatke w okienku nagrywanie
    if cv2.waitKey(1) & 0xFF == ord('q'):  # pozwolenie uzytkownikowi na zakonczenie dzialania programu poprzez nacisniecie klawisza 'q'
        break
nagranie.release()
cv2.destroyAllWindows()
arduino.close()
