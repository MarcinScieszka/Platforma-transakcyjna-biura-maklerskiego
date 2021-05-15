from widgets import Widgets
import constants

class CreateGui:
    def __init__(self, window):
        """
        Klasa wyświetla graficzny interfejs programu wykorzystując bibliotekę tkinter.
        """

        self.window = window
        self.window.geometry("800x700")
        self.window.maxsize(800, 700)  # ustawienie minimalnego rozmiaru okna
        self.window.minsize(800, 700)  # ustawienie maksymalnego rozmiaru okna
        self.window['bg'] = constants.COLOUR_BACKGROUND # wybór koloru tła
        self.window.title("Platforma transakcyjna")  # nadanie tytułu dla głównego okna
        # TODO: implement window.iconbitmap with .ico

        widgets = Widgets(window)
        widgets.setUpLabels()  # stworzenie etykiet
        widgets.setUpTextboxes()  # stworzenie pól tekstowych
        widgets.setUpButtons()  # stworzenie przycisków
