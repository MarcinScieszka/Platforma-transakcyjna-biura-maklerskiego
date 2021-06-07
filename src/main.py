import tkinter as tk

from src.gui import CreateGui


class Main:
    """Główna klasa programu.
    Wywołanie klasy CreateGui odpowiedzialnej za interfejs graficzny"""

    @staticmethod
    def main():
        window = tk.Tk()
        CreateGui(window)
        window.mainloop()


if __name__ == '__main__':
    Main.main()
