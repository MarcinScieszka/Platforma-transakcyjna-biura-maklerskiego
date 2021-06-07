import tkinter as tk

from src.gui import Gui


class Main:
    """Główna klasa programu.
    Wywołanie klasy Gui odpowiedzialnej za interfejs graficzny"""

    @staticmethod
    def main():
        window = tk.Tk()
        Gui(window)
        window.mainloop()


if __name__ == '__main__':
    Main.main()

