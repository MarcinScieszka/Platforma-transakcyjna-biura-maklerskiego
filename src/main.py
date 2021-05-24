from tkinter import *
from src.platform import Platform


class Main:
    @classmethod
    def main(cls):
        """Główna funkcja programu"""
        window = Tk()
        Platform(window)  # wywołanie głównej klasy obsługującej platformę
        window.mainloop()


if __name__ == '__main__':
    Main.main()
