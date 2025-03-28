#DZIAŁA

import serial
import time
import cv2

port="COM7"
wiadomosc_potwierdzajaca="OK" #wiadomosc ktora potwierdza odbior danych
wiadomosc_startowa="START" #wiadomosc ktora potwierdza gotowosc danych do odbioru

def potwierdzenie(rduino, oczekiwana_wiadomosc): #funkcja ktora zatrzymuje program i wykonuje sie w kolko poki nie przeslemy przez serial oczekiwanej wiadomosci
    wiadomosc=""
    while True:
        if rduino.in_waiting > 0: #jesli w buforze odbiorczym znajduja sie jakiekolwiek dane to warunek spelniony
            wiadomosc = rduino.readline().decode().strip() #odczytujemy te dane, dekodujemy ciag bajtow na stringa, usuwamy biale znaki czyli spacje, /r, /n
            print(wiadomosc) #linijka ktora w polaczeniu z programem w C pozwala na sprawdzenie czy dane zostaly przeslane poprawnie.
        if wiadomosc == oczekiwana_wiadomosc:
            break
        time.sleep(0.01) #podobno pomoze uniknac niepotrzebnego obciazenia CPU

def pozycja_serwo(wspolrzedna_twarzy, wymiar_twarzy, wymiar_kamery):
    proporcja=(wspolrzedna_twarzy+(wymiar_twarzy/2))/wymiar_kamery
    pozycja=180*proporcja
    return int(pozycja)


arduino=serial.Serial(port, 9600) #inicjalizacja komunikacji przez port szeregowy
time.sleep(2) #dajemy czas arduino na ustabilizowanie polaczenia

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
nagranie = cv2.VideoCapture(0)
if not nagranie.isOpened():
    print("nie udalo sie otworzyc kamery")
    exit()
sz_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_WIDTH)) # Pobranie szerokosci klatki wideo w pikselach
wys_kamery = int(nagranie.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Pobranie wysokosci klatki wideo w pikselach

while True:

    sprawdzenie, klatka = nagranie.read()
    if not sprawdzenie:
        break
    szara_klatka = cv2.cvtColor(klatka, cv2.COLOR_BGR2GRAY) # Konwersja obrazu na skale szarosci, klatka - obraz RGB, szara_klatka - nowy obraz w odcienach szarosci
    twarz = face_cascade.detectMultiScale(szara_klatka, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(twarz) > 0:
        x, y, sz_twarzy, wys_twarzy = twarz[0]
        cv2.rectangle(klatka, (x, y), (x + sz_twarzy, y + wys_twarzy), (100, 100, 100), 3)
        serwo_x=pozycja_serwo(x, sz_twarzy,sz_kamery)
        serwo_y=pozycja_serwo(y, wys_twarzy, wys_kamery)
        pozycje=[serwo_x,serwo_y]


        potwierdzenie(arduino, wiadomosc_startowa)
        arduino.write(bytearray(pozycje)) #przeslij tablice w postaci ciagu bajtow, dziala to dlatego bo przesylamy dane nie wieksze niz 255 czyli max przy jednym bajcie
        time.sleep(0.05) #opcjonalny, trzeba sprawdzic czy zadziala bez tego
        potwierdzenie(arduino, wiadomosc_potwierdzajaca)
    cv2.imshow("nagrywanie", klatka)  # wyswietla klatke w okienku nagrywanie
    if cv2.waitKey(1) & 0xFF == ord('q'):  # pozwolenie uzytkownikowi na zakonczenie dzialania programu poprzez nacisniecie klawisza 'q'
        break

nagranie.release()
cv2.destroyAllWindows()
arduino.close()