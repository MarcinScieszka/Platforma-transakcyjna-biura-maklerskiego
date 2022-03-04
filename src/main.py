import tkinter as tk
from src.gui import Gui


def main():
    window = tk.Tk()
    Gui(window)
    window.mainloop()


if __name__ == '__main__':
    main()
