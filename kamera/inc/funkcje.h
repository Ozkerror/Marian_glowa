#ifndef FUNKCJE_H
#define FUNKCJE_H

#include <vector>
#include <string>
#include "serialib.h"

// Enum do oznaczenia sektorów
enum class Sektor {
    SS, LS, PS, LG, PG
};

// Prototypy funkcji

// Potwierdzenie odebrania wiadomości od Arduino
void potwierdzenie(serialib &arduino, std::string oczekiwana_wiadomosc);

// Wysyłanie danych do Arduino
void komunikacja_arduino(serialib &arduino, std::vector<uint8_t> dane, std::string wiad_start, std::string wiad_potwierdzajaca);

// Wyznaczanie sektora, w którym znajduje się wykryta twarz
Sektor sprawdz_sektor(int x, int szer_kamery, int szer_twarzy, int y, int wys_kamery, int wys_twarzy);

// Obliczanie pozycji dla serwomechanizmów oczu
int ruch_oczu(int rozmiar_twarzy, int rozmiar_kamery, int pozycja, float wsp, int min_poz, int max_poz);

// Obliczanie pozycji dla serwomechanizmów głowy (wariant 1)
int ruch_glowy(int rozmiar_twarzy, int rozmiar_kamery, int pozycja, float wsp, int pozycja_aktualna, int min_poz, int max_poz, int predkosc);

// Obliczanie pozycji dla serwomechanizmów głowy (wariant 2)
int ruch_glowy_dwa(int rozmiar_twarzy, int rozmiar_kamery, int pozycja, float wsp, int pozycja_aktualna, int min_poz, int max_poz, int predkosc);

#endif
