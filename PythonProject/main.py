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

serwo_lp = "glowa_lp"
serwo_gd = "glowa_gd"

serwo_oko_lp = "oko_lp"
serwo_oko_gd = "oko_gd"

serwo_kat_lp = 0
serwo_kat_gd = 0
serwo_kat_oko_lp = 0
serwo_kat_oko_gd = 0

sektor = 0
start = 0
poprzedni = 0

czas_glowa = 3

o_wspolczynnik_lp = 1
o_wspolczynnik_gd = 1
g_wspolczynnik_lp = 1
g_wspolczynnik_gd = 1
odliczanie = 0

arduino = serial.Serial('COM3', 9600)
time.sleep(2)  # zeby sie polaczenie ustabilizowalo
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
nagranie = cv2.VideoCapture(0)

if not nagranie.isOpened():
    print("nie udalo sie otworzyc kamery")
    exit()

sz_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_WIDTH))
w_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_HEIGHT))

funkcje.centrowanie(arduino, serwo_lp, serwo_kat_lp, serwo_gd, serwo_kat_gd, serwo_oko_lp, serwo_oko_gd,
                    serwo_kat_oko_lp, serwo_kat_oko_gd)

while True:
    sprawdzenie, klatka = nagranie.read()
    if not sprawdzenie:
        break

    szara_klatka = cv2.cvtColor(klatka, cv2.COLOR_BGR2GRAY)
    twarz = face_cascade.detectMultiScale(szara_klatka, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, sz_twarzy, wys_twarzy) in twarz:
        cv2.rectangle(klatka, (x, y), (x + sz_twarzy, y + wys_twarzy), (100, 100, 100), 3)

        srodek_x = funkcje.srodek(x, sz_twarzy)
        srodek_y = funkcje.srodek(y, wys_twarzy)
        prop_x = funkcje.pozycja_x(x, sz_kamery, sz_twarzy)
        prop_y = funkcje.pozycja_y(y, w_kamery, wys_twarzy)
        funkcje.ruch_oczu(o_wspolczynnik_lp, o_wspolczynnik_gd, prop_x, prop_y, arduino, serwo_oko_gd, serwo_oko_lp)

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

        if not cokolwiek:
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

        if skrajne_l or skrajne_g or skrajne_d or skrajne_p or (odliczanie >= czas_glowa):
            funkcje.ruch_glowy(arduino, g_wspolczynnik_lp, g_wspolczynnik_gd, sz_kamery, w_kamery, srodek_x, srodek_y,
                               serwo_lp, serwo_gd)
            odliczanie = 0

        if sektor != 0 and sektor != poprzedni:
            odliczanie = time.time()

        if sektor == 1:
            odliczanie = 0

        poprzedni = sektor

    cv2.imshow("nagrywanie", klatka)
    if cv2.waitKey(1) & 0xFF == ord('q'):
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