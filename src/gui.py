from src.constants import Constants


class CreateGui:
    @classmethod
    def create_gui_params(cls, window):
        """
        Metoda ustawia główne parametry graficznego interfejsu programu wykorzystując bibliotekę tkinter.
        """

        cls.window = window
        cls.window.geometry("800x600")  # ustawienie wymiarów okna na 800 na 600 pikseli
        cls.window.resizable(False, False)  # zablokowanie możliwości zmiany rozmiaru okna
        cls.window['bg'] = Constants.COLOUR_BACKGROUND  # wybór koloru tła
        cls.window.title("Platforma transakcyjna")  # nadanie tytułu dla głównego okna
        # TODO: implement window.iconbitmap with .ico
