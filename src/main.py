from tkinter import *
from src.platform import Platform


def main():
    """Główna funkcja programu"""
    window = Tk()
    Platform(window)  # wywołanie głównej klasy obsługującej platformę
    window.mainloop()


if __name__ == '__main__':
    main()
