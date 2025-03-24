import serial
import time

port="COM3"
tablica1=[20, 50, 80, 100, 150]
tablica2=[120, 100, 80, 50, 30]
wiadomosc_potwierdzajaca="OK"
def potwierdzenie(rduino, oczekiwana_wiadomosc):
    wiadomosc=""
    while True:
        if rduino.in_waiting() > 0:
            wiadomosc = rduino.readline().decode().strip()
        if wiadomosc == oczekiwana_wiadomosc:
            break
arduino=serial.Serial(port, 9600)
string_tablica1 = ",".join(map(str,tablica1)) + "\n"
string_tablica2 = ",".join(map(str,tablica2)) + "\n"
while True:
    arduino.write(string_tablica1.encode())
    potwierdzenie(arduino, wiadomosc_potwierdzajaca)
    time.sleep(0.2)
    arduino.write(string_tablica2.encode())
    potwierdzenie(arduino, wiadomosc_potwierdzajaca)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
arduino.close()

