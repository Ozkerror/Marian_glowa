#include <opencv2/opencv.hpp>
#include <iostream>
#include <chrono>
#include <thread>
#include "funkcje.h"
#include "serialib.h"

using namespace std;
using namespace cv;

// stałe portu i komunikacji
const string port = "COM7";
const string wiadomosc_startowa = "START";
const string wiadomosc_potwierdzajaca = "OK";

int main() {
    serialib arduino;
    if (arduino.openDevice(port.c_str(), 9600) != 1) {
        cout << "Nie udało się otworzyć portu!" << endl;
        return -1;
    }
    this_thread::sleep_for(chrono::seconds(2)); // stabilizacja połączenia

    CascadeClassifier face_cascade;
    if (!face_cascade.load("haarcascade_frontalface_default.xml")) {
        cout << "Nie udało się załadować klasyfikatora!" << endl;
        return -1;
    }

    VideoCapture nagranie(0);
    if (!nagranie.isOpened()) {
        cout << "Nie udało się otworzyć kamery!" << endl;
        return -1;
    }

    int sz_kamery = (int)nagranie.get(CAP_PROP_FRAME_WIDTH);
    int wys_kamery = (int)nagranie.get(CAP_PROP_FRAME_HEIGHT);

    // pozycje domyślne
    int domyslne_x_glowy = 103, domyslne_y_glowy = 95;
    int domyslne_x_oczu = 90, domyslne_y_oczu = 90;

    int pozycja_x_glowy = domyslne_x_glowy, pozycja_y_glowy1 = domyslne_y_glowy, pozycja_y_glowy2 = domyslne_y_glowy;
    int pozycja_x_oczu = domyslne_x_oczu, pozycja_y_oczu = domyslne_y_oczu;

    // zakresy
    int min_x_glowy=48, max_x_glowy=158, min_y_glowy=80, max_y_glowy=110;
    int min_x_oczu=45, max_x_oczu=135, min_y_oczu=45, max_y_oczu=135;

    float o_wsp_x=1, o_wsp_y=1, g_wsp_x=1, g_wsp_y=1;

    auto czas_poprzedni = chrono::high_resolution_clock::now();

    Mat klatka;
    while (true) {
        nagranie >> klatka;
        if (klatka.empty()) break;

        Mat szara_klatka;
        cvtColor(klatka, szara_klatka, COLOR_BGR2GRAY);

        vector<Rect> twarze;
        face_cascade.detectMultiScale(szara_klatka, twarze, 1.1, 5, 0, Size(30, 30));

        if (!twarze.empty()) {
            Rect twarz = twarze[0];
            int x = twarz.x, y = twarz.y, sz_twarzy = twarz.width, wys_twarzy = twarz.height;

            Sektor sektor = sprawdz_sektor(x, sz_kamery, sz_twarzy, y, wys_kamery, wys_twarzy);

            rectangle(klatka, twarz, Scalar(0, 255, 0), 2);

            auto czas_obecny = chrono::high_resolution_clock::now();
            double czas_diff = chrono::duration<double>(czas_obecny - czas_poprzedni).count();

            if (sektor == Sektor::SS) {
                pozycja_x_oczu = ruch_oczu(sz_twarzy, sz_kamery, x, o_wsp_x, min_x_oczu, max_x_oczu);
                pozycja_y_oczu = ruch_oczu(wys_twarzy, wys_kamery, y, o_wsp_y, min_y_oczu, max_y_oczu);
                czas_poprzedni = chrono::high_resolution_clock::now();
            } else {
                if (czas_diff > 3) {
                    pozycja_x_glowy = ruch_glowy(sz_twarzy, sz_kamery, x, o_wsp_x, pozycja_x_glowy, min_x_glowy, max_x_glowy, 8);
                    pozycja_y_glowy1 = ruch_glowy(wys_twarzy, wys_kamery, y, g_wsp_y, pozycja_y_glowy1, min_y_glowy, max_y_glowy, 8);
                    pozycja_y_glowy2 = ruch_glowy_dwa(wys_twarzy, wys_kamery, y, g_wsp_y, pozycja_y_glowy2, min_y_glowy, max_y_glowy, 8);

                    czas_poprzedni = chrono::high_resolution_clock::now();

                    pozycja_x_oczu = (pozycja_x_glowy <= min_x_glowy || pozycja_x_glowy >= max_x_glowy)
                                     ? ruch_oczu(sz_twarzy, sz_kamery, x, o_wsp_x, min_x_oczu, max_x_oczu)
                                     : domyslne_x_oczu;

                    pozycja_y_oczu = (pozycja_y_glowy1 <= min_y_glowy || pozycja_y_glowy1 >= max_y_glowy)
                                     ? ruch_oczu(wys_twarzy, wys_kamery, y, o_wsp_y, min_y_oczu, max_y_oczu)
                                     : domyslne_y_oczu;
                } else {
                    pozycja_x_oczu = ruch_oczu(sz_twarzy, sz_kamery, x, o_wsp_x, min_x_oczu, max_x_oczu);
                    pozycja_y_oczu = ruch_oczu(wys_twarzy, wys_kamery, y, o_wsp_y, min_y_oczu, max_y_oczu);
                }
            }

            // Wysyłanie do Arduino
            vector<uint8_t> dane = {
                (uint8_t)pozycja_x_glowy,
                (uint8_t)pozycja_y_glowy1,
                (uint8_t)pozycja_y_glowy2,
                (uint8_t)pozycja_x_oczu,
                (uint8_t)pozycja_y_oczu
            };
            komunikacja_arduino(arduino, dane, wiadomosc_startowa, wiadomosc_potwierdzajaca);
        }

        imshow("Obraz z kamery", klatka);
        if (waitKey(1) == 'q') break;
    }

    nagranie.release();
    arduino.closeDevice();
    destroyAllWindows();

    return 0;
}
