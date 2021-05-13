from tkinter import *


# TODO: implement main program loop
class MainLoop:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("800x700")
        self.window.maxsize(800, 700)  # ustawienie minimalnego rozmiaru okna
        self.window.minsize(800, 700)  # ustawienie maksymalnego rozmiaru okna
        self.window['bg'] = '#2A2A2E'  # wybór koloru tła
        self.window.title("Platforma transakcyjna") # nadanie tytułu dla głównego okna
        # TODO: implement window.iconbitmap with .ico

        self.window.mainloop()


platforma = MainLoop()
