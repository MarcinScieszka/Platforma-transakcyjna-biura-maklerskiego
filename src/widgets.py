from tkinter import *
from constants import *


class Widgets:
    def __init__(self, window):
        self.window = window

    def setUpLabels(self):
        """Metoda tworzy oraz wyświetla etykiety"""

        # tworzenie etykiet
        main_title_label = Label(self.window, text=TEXT_MAIN_TITLE, bg=COLOUR_BACKGROUND, fg=COLOUR_TEXT,
                           font=(FONT_TYPEFACE, FONT_SIZE_TITLE, TITLE_FONT_WEIGHT), pady=20)
        main_description_label = Label(self.window, text=TEXT_MAIN_DESCRIPTION, bg=COLOUR_BACKGROUND, fg=COLOUR_TEXT,
                                 font=(FONT_TYPEFACE, FONT_SIZE_DESCRIPTION), pady=20)

        amount_label = Label(self.window, text=TEXT_AMOUNT, bg=COLOUR_BACKGROUND, fg=COLOUR_TEXT,
                             font=(FONT_TYPEFACE, FONT_SIZE_REGULAR))

        # wyświetlanie etykiet
        main_title_label.grid(row=0, column=3, sticky=N)
        main_description_label.grid(row=1, column=3, sticky=N)
        amount_label.grid(row=3, column=0, sticky=W)

    def setUpTextboxes(self):
        """Metoda tworzy oraz wyświetla pola tekstowe"""

        amount_text = StringVar()
        amount_entry = Entry(self.window, textvariable=amount_text)
        amount_entry.grid(row=3, column=1)

    def setUpButtons(self):
        """Metoda tworzy oraz wyświetla przyciski"""

        close_button = Button(self.window, text=TEXT_CLOSE_BUTTON, command=self.quit, padx=10)
        close_button.grid(row=10, column=5)

    def quit(self):
        """Metoda zamyka główne okno aplikacji."""

        self.window.destroy()
