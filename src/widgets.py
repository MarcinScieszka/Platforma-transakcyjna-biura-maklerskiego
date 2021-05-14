from tkinter import *
import constants


class Widgets:
    def __init__(self, window):
        self.window = window

    def setUpButtons(self):
        """Metoda tworzy oraz wyświetla przyciski"""
        close_button = Button(self.window, text="Wyjdź", command=self.quit)
        close_button.pack()


    def setUpLabels(self):
        """Metoda tworzy oraz wyświetla etykiety"""

        myLabel = Label(self.window, text="Platforma transakcyjna", bg=constants.BACKGROUND_COLOUR,
                        fg=constants.TEXT_COLOUR, font=(constants.FONT_SPACE, constants.FONT_SIZE, "bold"), pady=10,
                        padx=3)
        myLabel2 = Label(self.window, text="Biuro maklerskie MorganLeeCash", background='white', font=120)

        myLabel.pack()  # wyświetl etykiety
        myLabel2.pack()

    def quit(self):
        """Metoda zamyka główne okno aplikacji."""
        self.window.destroy()