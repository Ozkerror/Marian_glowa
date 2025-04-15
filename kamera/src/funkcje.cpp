#include "funkcje.h"
#include <thread>
#include <chrono>
#include <iostream>

using namespace std;
using namespace std::chrono;

void potwierdzenie(serialib &arduino, string oczekiwana_wiadomosc) {
    char buffer[256];
    string wiadomosc;
    while (true) {
        int n = arduino.readString(buffer, '\n', 1000, 256);
        if (n > 0) {
            wiadomosc = string(buffer);
            wiadomosc.erase(wiadomosc.find_last_not_of("\r\n") + 1); // usuń enter i newline
            cout << "Odebrano: " << wiadomosc << endl;
            if (wiadomosc == oczekiwana_wiadomosc) {
                break;
            }
        }
        this_thread::sleep_for(milliseconds(10));
    }
}

void komunikacja_arduino(serialib &arduino, vector<uint8_t> dane, string wiad_start, string wiad_potwierdzajaca) {
    potwierdzenie(arduino, wiad_start);
    arduino.writeBytes(dane.data(), dane.size());
    potwierdzenie(arduino, wiad_potwierdzajaca);
}
