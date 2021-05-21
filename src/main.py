from tkinter import *
from src.platform import Platform

"""Uruchomienie głównej pętli programu."""

if __name__ == '__main__':
    window = Tk()
    Platform(window)  # wywołanie klasy obsługującej platformę
    window.mainloop()
