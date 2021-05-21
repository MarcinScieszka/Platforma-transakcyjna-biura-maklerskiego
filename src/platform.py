from tkinter import *
from tkinter import messagebox
from src.constants import *
from src.gui import CreateGui


def show_error(error_message):
    """Wyświetlenie okna z komunikatem błędu."""

    messagebox.showerror(ERROR, error_message)


def update_label(label_text_var, label_text):
    """Aktualizacja nazwy danej etykiety"""

    label_text_var.set(label_text)


class Platform:
    """Główna klasa platformy transakcyjnej"""

    def __init__(self, window):
        self.window = window
        CreateGui.create_gui_params(window)  # wywołanie klasy ustawiającej parametry gui
        # tworzenie etykiet
        self.main_title_label = Label(self.window, text=TEXT_MAIN_TITLE, bg=COLOUR_BACKGROUND, fg=COLOUR_TEXT,
                                      font=(FONT_TYPEFACE, FONT_SIZE_TITLE, FONT_WEIGHT_TITLE), pady=20)
        self.main_description_label = Label(self.window, text=TEXT_MAIN_DESCRIPTION, bg=COLOUR_BACKGROUND,
                                            fg=COLOUR_TEXT, font=(FONT_TYPEFACE, FONT_SIZE_DESCRIPTION), pady=20)
        self.amount_label = Label(self.window, text=TEXT_AMOUNT, bg=COLOUR_BACKGROUND, fg=COLOUR_TEXT,
                                  font=(FONT_TYPEFACE, FONT_SIZE_REGULAR))

        self.account_value_label_text = StringVar()
        self.account_value_label_text.set(TEXT_CURRENT_BALANCE + str(Transfer.account_value) + TEXT_CURRENCY)
        self.account_value_label = Label(self.window, textvariable=self.account_value_label_text,
                                         bg=COLOUR_BACKGROUND, fg=COLOUR_TEXT, font=(FONT_TYPEFACE, FONT_SIZE_REGULAR))

        # tworzenie pól tekstowych
        self.amount_text = StringVar()
        self.amount_entry = Entry(self.window, textvariable=TEXT_AMOUNT)

        # tworzenie przycisków
        self.close_button = Button(self.window, text=TEXT_CLOSE_BUTTON, command=lambda: self.quit_platform(), padx=10)
        self.deposit_amount_button = Button(self.window, text=TEXT_DEPOSIT_BUTTON,
                                            command=lambda: Transfer(self.window, STATE_DEPOSIT))
        self.withdraw_amount_button = Button(self.window, text=TEXT_WITHDRAW_BUTTON,
                                             command=lambda: Transfer(self.window, STATE_WITHDRAWAL))

        self.show_widgets()  # wyświetlenie startowych widżetów

    def show_widgets(self):
        """Metoda wyświetla na ekranie zdefiniowane widżety"""

        # wyświetlanie etykiet
        self.main_title_label.grid(row=0, column=2, columnspan=6, sticky='ew')
        self.main_description_label.grid(row=1, column=2, columnspan=6, sticky='ew')
        self.amount_label.grid(row=3, column=0, sticky=W)
        self.account_value_label.grid(row=4, column=2)

        # wyświetlanie pól tekstowych
        self.amount_entry.grid(row=3, column=1)

        # wyświetlanie przycisków
        self.close_button.grid(row=10, column=1)
        self.deposit_amount_button.grid(row=3, column=2)
        self.withdraw_amount_button.grid(row=3, column=3)

    def quit_platform(self):
        """Metoda zamyka główne okno aplikacji."""

        self.window.destroy()


class Transfer(Platform):
    """Obsługa transakcji wpłaty i wypłaty środków oraz aktualizacja stanu środków na kocie."""
    account_value = 0

    # TODO: withdraw all available funds

    def __init__(self, window, state):
        super().__init__(window)
        self.state = state
        self.handle_transfer(self.state)

    def handle_transfer(self, state):
        """Metoda obsługuje proces transakcji"""
        amount = self.get_amount()
        is_correct = self.verify(amount, state)

        if is_correct:
            amount = round(float(amount), 2)  # wiemy, że kwota jest poprawna, możemy ją zaokrąglić do dwóch miejsc po przecinku
            if self.state == STATE_DEPOSIT:
                self.deposit(amount)
            if self.state == STATE_WITHDRAWAL:
                self.withdraw(amount)

    def deposit(self, amount):
        response = messagebox.askokcancel("Potwierdź wpłatę", 'Czy na pewno chcesz wpłacić {} zł?'.format(amount))
        if response == 1:  # użytkownik potwierdził chęć wpłaty na konto
            Transfer.account_value += amount
            Transfer.account_value = round(Transfer.account_value, 2)
            messagebox.showinfo('', 'Pomyślnie dokonano wpłaty {} zł'.format(amount))
            messagebox.showinfo('', 'Stan środków na kocie: {} zł'.format(Transfer.account_value))
            update_label(self.account_value_label_text,
                         TEXT_CURRENT_BALANCE + str(Transfer.account_value) + TEXT_CURRENCY)

    def withdraw(self, amount):
        response = messagebox.askokcancel("Potwierdź wypłatę", 'Czy na pewno chcesz wypłacić {} zł?'.format(amount))
        if response == 1:  # użytkownik potwierdził chęć wypłaty na konto
            Transfer.account_value -= amount
            Transfer.account_value = round(Transfer.account_value, 2)
            messagebox.showinfo('', 'Pomyślnie dokonano wypłaty {} zł'.format(amount))
            messagebox.showinfo('', 'Stan środków na kocie: {} zł'.format(Transfer.account_value))
            update_label(self.account_value_label_text,
                         TEXT_CURRENT_BALANCE + str(Transfer.account_value) + TEXT_CURRENCY)

    def get_amount(self):
        """Metoda odczytuje kwotę podaną przez użytkownika"""

        return self.amount_entry.get()

    def verify(self, amount, state):
        """Metoda weryfikuję poprawność danych wprowadzonych przez użytkownika podczas podawania kwoty"""

        try:
            amount = float(amount)
        except ValueError:
            show_error(ERROR_MESSAGE_VALUE)
            return False

        if amount <= 0:
            show_error(ERROR_MESSAGE_VALUE)
            return False

        if state == STATE_WITHDRAWAL:
            if self.account_value - amount < 0:
                show_error(ERROR_MESSAGE_NEGATIVE_BALANCE)
                return False

        return True
