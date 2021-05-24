from tkinter import *

from src.data_provider import DataProvider
from src.gui import CreateGui
from src.platform import Platform


def main():
    """Główna funkcja programu"""
    window = Tk()
    CreateGui.create_gui_params(window)  # wywołanie klasy ustawiającej parametry gui
    Platform(window)  # wywołanie głównej klasy obsługującej platformę

    DataProvider.get_companies()


    window.mainloop()


if __name__ == '__main__':
    main()
