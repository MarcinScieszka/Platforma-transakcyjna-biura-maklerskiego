import tkinter as tk
from src.gui import CreateGui


class Main:
    """Główna klasa programu.
    Wywołanie CreateGui odpowiedzialnej za interfejs graficzny"""
    @classmethod
    def main(cls):
        window = tk.Tk()
        CreateGui.create_gui(window)
        window.mainloop()


if __name__ == '__main__':
    Main.main()
