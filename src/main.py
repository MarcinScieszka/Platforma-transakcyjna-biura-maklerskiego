from tkinter import *
from gui import CreateGui

"""Uruchomienie głównej pętli programu."""

window = Tk()
CreateGui(window)  # wywołanie klasy tworzącej gui
window.mainloop()
