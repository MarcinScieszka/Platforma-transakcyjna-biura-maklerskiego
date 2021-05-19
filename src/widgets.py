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
        self.main_title_label.grid(row=0, column=2, columnspan=6, sticky='ew')
        self.main_description_label.grid(row=1, column=2, columnspan=6, sticky='ew')
        self.amount_label.grid(row=3, column=0, sticky=W)

        # tworzenie pól tekstowych
        self.amount_text = StringVar()
        self.amount_entry = Entry(self.window, textvariable=TEXT_AMOUNT)

        # wyświetlanie pól tekstowych
        self.amount_entry.grid(row=3, column=1)

        # tworzenie przycisków
        self.close_button = Button(self.window, text=TEXT_CLOSE_BUTTON, command=self.quit, padx=10)
        self.deposit_amount_button = Button(self.window, text=TEXT_DEPOSIT_BUTTON,
                                            command=lambda: self.read_amount(STATE_DEPOSIT))
        self.withdraw_amount_button = Button(self.window, text=TEXT_WITHDRAW_BUTTON,
                                             command=lambda: self.read_amount(STATE_WITHDRAWAL))

        # wyświetlanie przycisków
        self.close_button.grid(row=10, column=1)
        self.deposit_amount_button.grid(row=3, column=2)
        self.withdraw_amount_button.grid(row=3, column=3)

    def show_error(self, error_message):
        """Metoda wyświetla okno z komunikatem błędu."""

        messagebox.showerror('Błąd', error_message)

    def quit(self):
        """Metoda zamyka główne okno aplikacji."""

        self.window.destroy()

    def read_amount(self, state):
        """Metoda odczytuje wartość kwoty wprowadzonej przez użytkownika"""

        try:
            amount = int(self.amount_entry.get())
        except ValueError:
            self.show_error(ERROR_MESSAGE_VALUE)
            return

        if amount <= 0:
            self.show_error(ERROR_MESSAGE_VALUE)

        if state == STATE_DEPOSIT:
            print('You chose to deposit %lf zł' % amount)
            # TODO: implement deposit method
        if state == STATE_WITHDRAWAL:
            print('You chose to withdraw %lf zł' % amount)
            # TODO: implement withdrawal method
