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

czas_glowa = 3

o_wspolczynnik_lp = 1
o_wspolczynnik_gd = 1
g_wspolczynnik_lp = 1
g_wspolczynnik_gd = 1
odliczanie = 0


wiadomosc_potwierdzajaca="potwierdzenie"
arduino = serial.Serial(port, 9600) #tworzy obiekt z ktorym bedziemy sie komunikowac

time.sleep(2)  # zeby sie polaczenie ustabilizowalo
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') # Zaladowanie klasyfikatora, model do wykrywania twarzy
nagranie = cv2.VideoCapture(0)

if not nagranie.isOpened():
    print("nie udalo sie otworzyc kamery")
    exit()

sz_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_WIDTH)) # Pobranie szerokosci klatki wideo w pikselach
w_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Pobranie wysokosci klatki wideo w pikselach


funkcje.centrowanie(arduino, glowa_kat_lp,glowa_kat_gd,oczy_kat_lp,oczy_kat_gd,wiadomosc_potwierdzajaca)


while True:                                     # Odczytywanie klatek nagrania, jesli sprawdzenie jest false to oznacza koniec nagrania
    sprawdzenie, klatka = nagranie.read()
    if not sprawdzenie:
        break


    szara_klatka = cv2.cvtColor(klatka, cv2.COLOR_BGR2GRAY) # Konwersja obrazu na skale szarosci, klatka - obraz RGB, szara_klatka - nowy obraz w odcienach szarosci
    twarz = face_cascade.detectMultiScale(szara_klatka, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)) # Wykrywanie twarzy, skalowanie obrazu,
                                                                                                           # minNeighbors - Liczba sąsiadujących prostokątów (kandydatów na twarz), które muszą zostać wykryte, aby uznać, że jest tam faktyczna twarz,
                                                                                                           # minSize=(30, 30) - Minimalny rozmiar wykrywanej twarzy w pikselach.
    krotka_x=twarz[0]#wyciagam z obiektu twarz krotke ktora przechowuje wspolrzedne x twarzy w kamerze
    krotka_y=twarz[1]
    krotka_sz_twarzy=twarz[2]
    krotka_wys_twarzy=twarz[3]
    x=krotka_x[0]#wycaigam z krotki wspolrzedna x pierwszej wykrytej twarzy
    y=krotka_y[0]
    sz_twarzy=krotka_sz_twarzy[0]
    wys_twarzy=krotka_wys_twarzy[0]
    cv2.rectangle(klatka, (x, y), (x + sz_twarzy, y + wys_twarzy), (100, 100, 100), 3) # Kod przechodzi przez wszystkie wykryte twarze i rysuje wokol nich prostokat

    srodek_x = funkcje.srodek(x, sz_twarzy)
    srodek_y = funkcje.srodek(y, wys_twarzy)
    prop_x = funkcje.pozycja_x(x, sz_kamery, sz_twarzy)
    prop_y = funkcje.pozycja_y(y, w_kamery, wys_twarzy)

    #wywolanie funkcji sprawdzania

    ss = funkcje.sprawdz_ss(prop_x, prop_y)
    sg = funkcje.sprawdz_sg(prop_x, prop_y)
    sd = funkcje.sprawdz_sd(prop_x, prop_y)
    ls = funkcje.sprawdz_ls(prop_x, prop_y)
    lg = funkcje.sprawdz_lg(prop_x, prop_y)
    ld = funkcje.sprawdz_ld(prop_x, prop_y)
    ps = funkcje.sprawdz_ps(prop_x, prop_y)
    pg = funkcje.sprawdz_pg(prop_x, prop_y)
    pd = funkcje.sprawdz_pd(prop_x, prop_y)
    cokolwiek = funkcje.sprawdz_cokolwiek(ss, sg, sd, ls, lg, ld, ps, pg, pd)


    skrajne_l = funkcje.skrajne_l(x, sz_kamery, 0.05)
    skrajne_p = funkcje.skrajne_p(x, sz_twarzy, sz_kamery, 0.95)
    skrajne_g = funkcje.skrajne_g(y, w_kamery, 0.05)
    skrajne_d = funkcje.skrajne_d(y, wys_twarzy, w_kamery, 0.95)

    if not twarz: #ten zostanie spelniony jesli twarz bedzie pustą listą, czyli jesli zadna twarz nie zostanie wykryta
        sektor = 0
    elif ss:
        sektor = 1
    elif sg:
        sektor = 2
    elif sd:
        sektor = 3
    elif ls:
        sektor = 4
    elif lg:
        sektor = 5
    elif ld:
        sektor = 6
    elif ps:
        sektor = 7
    elif pg:
        sektor = 8
    elif pd:
        sektor = 9
    # sprawdzanie czy sektor sie zmienil
    if sektor != 0 and sektor != poprzedni:
        odliczanie = time.time()

    if skrajne_l or skrajne_g or skrajne_d or skrajne_p or (odliczanie >= czas_glowa):
        glowa_kat_lp, glowa_kat_gd =ruch_glowy(g_wspolczynnik_lp,g_wspolczynnik_gd, sz_kamery,w_kamery,x,y)
        odliczanie = 0

    oczy_kat_lp, oczy_kat_gd=ruch_oczu(o_wspolczynnik_lp, o_wspolczynnik_gd, prop_x,prop_y)
    komunikacja_arduino(arduino, glowa_kat_lp, glowa_kat_gd, oczy_kat_lp, oczy_kat_gd, wiadomosc_potwierdzajaca)

    poprzedni=sektor
    cv2.imshow("nagrywanie", klatka) # wyswietla klatke w okienku nagrywanie
    if cv2.waitKey(1) & 0xFF == ord('q'): # pozwolenie uzytkownikowi na zakonczenie dzialania programu poprzez nacisniecie klawisza 'q'
        break

nagranie.release()
cv2.destroyAllWindows()
arduino.close()

#if odliczanie>=czas_glowa:
            #odliczanie=0
            #rusza glowa
            #srodkowanie oczu
            #time.sleep(2)

        #podazanie oczami
