import serial
import time

port="COM9"
tablica1=[20, 50, 80, 100, 150] #tablice zawierajace kolejne wartosci pozycji serwomechanizmu
tablica2=[120, 100, 80, 50, 30]
wiadomosc_potwierdzajaca="OK" #wiadomosc ktora potwierdza odbior danych
wiadomosc_startowa="START" #wiadomosc ktora potwierdza gotowosc danych do odbioru

def potwierdzenie(rduino, oczekiwana_wiadomosc): #funkcja ktora zatrzymuje program i wykonuje sie w kolko poki nie przeslemy przez serial oczekiwanej wiadomosci
    wiadomosc=""
    while True:
        if rduino.in_waiting > 0: #jesli w buforze odbiorczym znajduja sie jakiekolwiek dane to warunek spelniony
            wiadomosc = rduino.readline().decode().strip() #odczytujemy te dane, dekodujemy ciag bajtow na stringa, usuwamy biale znaki czyli spacje, /r, /n
        if wiadomosc == oczekiwana_wiadomosc:
            break
        time.sleep(0.01) #podobno pomoze uniknac niepotrzebnego obciazenia CPU
arduino=serial.Serial(port, 9600) #inicjalizacja komunikacji przez port szeregowy
time.sleep(2) #dajemy czas arduino na ustabilizowanie polaczenia
while True:
    potwierdzenie(arduino, wiadomosc_startowa)
    arduino.write(bytearray(tablica1)) #przeslij tablice w postaci ciagu bajtow, dziala to dlatego bo przesylamy dane nie wieksze niz 255 czyli max przy jednym bajcie
    time.sleep(0.05) #opcjonalny, trzeba sprawdzic czy zadziala bez tego
    potwierdzenie(arduino, wiadomosc_potwierdzajaca)
    potwierdzenie(arduino, wiadomosc_startowa)
    arduino.write(bytearray(tablica2))
    time.sleep(0.05) #opcjonalny
    potwierdzenie(arduino, wiadomosc_potwierdzajaca)
    if cv2.waitKey(1) & 0xFF == ord('q'): #jesli wcisniemy q na klawiaturze to wyjdziemy z programu
        break
arduino.close()

