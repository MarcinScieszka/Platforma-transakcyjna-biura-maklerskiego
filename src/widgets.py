from tkinter import *
from tkinter import messagebox

from constants import *


class Widgets:

    def __init__(self, window):
        self.window = window

        # tworzenie etykiet
        self.main_title_label = Label(self.window, text=TEXT_MAIN_TITLE, bg=COLOUR_BACKGROUND, fg=COLOUR_TEXT,
                                      font=(FONT_TYPEFACE, FONT_SIZE_TITLE, FONT_WEIGHT_TITLE), pady=20)
        self.main_description_label = Label(self.window, text=TEXT_MAIN_DESCRIPTION, bg=COLOUR_BACKGROUND,
                                            fg=COLOUR_TEXT, font=(FONT_TYPEFACE, FONT_SIZE_DESCRIPTION), pady=20)
        self.amount_label = Label(self.window, text=TEXT_AMOUNT, bg=COLOUR_BACKGROUND, fg=COLOUR_TEXT,
                                  font=(FONT_TYPEFACE, FONT_SIZE_REGULAR))

        # wyświetlanie etykiet
        self.main_title_label.grid(row=0, column=3, sticky=N)
        self.main_description_label.grid(row=1, column=3, sticky=N)
        self.amount_label.grid(row=3, column=0, sticky=W)

        # tworzenie pól tekstowych
        self.amount_text = StringVar()
        self.amount_entry = Entry(self.window, textvariable=TEXT_AMOUNT)

        # wyświetlanie pól tekstowych
        self.amount_entry.grid(row=3, column=1)

        # tworzenie przycisków
        self.close_button = Button(self.window, text=TEXT_CLOSE_BUTTON, command=self.quit, padx=10)
        self.confirm_amount_button = Button(self.window, text=TEXT_CONFIRM_BUTTON, command=self.read_amount)

        # wyświetlanie przycisków
        self.close_button.grid(row=10, column=1)
        self.confirm_amount_button.grid(row=3, column=2)


    def show_error(self):
        """Metoda wyświetla okno z komunikatem błędu."""
        messagebox.showerror('Błąd', 'Podano nieprawidłową wartość')

    def quit(self):
        """Metoda zamyka główne okno aplikacji."""

        self.window.destroy()

    def read_amount(self):
        print(self.amount_entry.get())
