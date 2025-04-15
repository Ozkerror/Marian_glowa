cmake_minimum_required(VERSION 3.16)
project(Marian_glowa_PC)

set(CMAKE_CXX_STANDARD 20)

# Ścieżka do nagłówków serialib
include_directories(include)

# Ścieżka do OpenCV
set(OpenCV_DIR "C:/opencv/build")  # <-- podmień na swoją ścieżkę
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

# Dodanie plików źródłowych
add_executable(Marian_glowa_PC src/main.cpp src/serialib.cpp src/funkcje.cpp)

# Linkowanie z bibliotekami OpenCV
target_link_libraries(Marian_glowa_PC ${OpenCV_LIBS})
