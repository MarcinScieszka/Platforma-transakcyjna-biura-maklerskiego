from src.constants import COLOUR_BACKGROUND


class CreateGui:
    @classmethod
    def create_gui_params(cls, window):
        """
        Metoda ustawia główne parametry graficznego interfejsu programu wykorzystując bibliotekę tkinter.
        """

        cls.window = window
        cls.window.geometry("800x700")  # ustawienie wymiarów okna na 800 na 700 pixeli
        cls.window.maxsize(800, 700)  # ustawienie minimalnego rozmiaru okna
        cls.window.minsize(800, 700)  # ustawienie maksymalnego rozmiaru okna
        cls.window['bg'] = COLOUR_BACKGROUND  # wybór koloru tła
        cls.window.title("Platforma transakcyjna")  # nadanie tytułu dla głównego okna
        # TODO: implement window.iconbitmap with .ico
