from tkinter import *
from tkinter import messagebox
from src.constants import Constants
from src.data_provider import DataProvider
from src.gui import CreateGui


def show_error(error_message):
    """Wyświetlenie okna z komunikatem błędu."""

    messagebox.showerror(Constants.MESSAGE_ERROR, error_message)


def update_label(label_text_var, label_text):
    """Aktualizacja nazwy danej etykiety"""

    label_text_var.set(label_text)


class Platform:
    """Główna klasa platformy transakcyjnej"""

    account_balance = 0

    def __init__(self, window):
        self.window = window
        CreateGui.create_gui_params(window)  # wywołanie klasy ustawiającej parametry gui
        Widgets(window)
        Market(window)


class Market:
    def __init__(self, window):
        self.window = window
        self.create_available_companies()

    def create_available_companies(self):
        available_companies = DataProvider.get_companies()
        offset = 0
        for company in available_companies:
            Label(self.window,
                  text=company.get_name() + company.get_symbol() + company.get_price(),
                  bg='grey',
                  fg=Constants.COLOUR_TEXT,
                  font=('bold', 10)).place(x=20, y=200 + offset)
            Button(self.window,
                   text="Kup",
                   command=lambda: self.buy_stock(company)).place(x=280, y=200 + offset)

            offset += 30

    def buy_stock(self, company):
        # TODO:implement
        pass


class Widgets:
    """Klasa obsługująca widżety"""

    count = 0  # zmienna zlicza ilość wywołań klasy, dzięki czemu możemy tworzyć widżety tylko podczas pierwszego wywołania klasy

    def __init__(self, window):
        self.window = window

        if Widgets.count == 0:
            self.create_widgets()  # tworzenie widżetów
            self.show_widgets()  # wyświetlenie startowych widżetów

        Widgets.count += 1

    def create_widgets(self):
        """Metoda tworzy widżety takie jak przyciski, pola tekstowe, napisy"""

        # tworzenie etykiet
        self.main_title_label = Label(self.window,
                                      text=Constants.TEXT_MAIN_TITLE,
                                      bg=Constants.COLOUR_BACKGROUND,
                                      fg=Constants.COLOUR_TEXT,
                                      font=(
                                          Constants.FONT_TYPEFACE,
                                          Constants.FONT_SIZE_TITLE,
                                          Constants.FONT_WEIGHT_TITLE),
                                      pady=20)
        self.main_description_label = Label(self.window,
                                            text=Constants.TEXT_MAIN_DESCRIPTION,
                                            bg=Constants.COLOUR_BACKGROUND,
                                            fg=Constants.COLOUR_TEXT,
                                            font=(Constants.FONT_TYPEFACE,
                                                  Constants.FONT_SIZE_DESCRIPTION),
                                            pady=20)
        self.amount_label = Label(self.window,
                                  text=Constants.TEXT_AMOUNT,
                                  bg=Constants.COLOUR_BACKGROUND,
                                  fg=Constants.COLOUR_TEXT,
                                  padx=20,
                                  font=(Constants.FONT_TYPEFACE,
                                        Constants.FONT_SIZE_REGULAR))
        self.account_balance_label_text = StringVar()
        self.account_balance_label_text.set(self.get_current_account_balance_text())
        self.account_balance_label = Label(self.window,
                                           textvariable=self.account_balance_label_text,
                                           padx=20,
                                           bg=Constants.COLOUR_BACKGROUND,
                                           fg=Constants.COLOUR_TEXT,
                                           font=(Constants.FONT_TYPEFACE,
                                                 Constants.FONT_SIZE_REGULAR))

        # tworzenie pól tekstowych
        self.amount_text = StringVar()
        self.amount_entry = Entry(self.window, textvariable=Constants.TEXT_AMOUNT)

        # tworzenie przycisków
        self.close_button = Button(self.window,
                                   text=Constants.TEXT_CLOSE_BUTTON,
                                   command=lambda: self.exit_platform(),
                                   padx=10)
        self.deposit_amount_button = Button(self.window,
                                            text=Constants.TEXT_DEPOSIT_BUTTON,
                                            command=lambda: self.execute_transfer(Constants.STATE_DEPOSIT))
        self.withdraw_amount_button = Button(self.window,
                                             text=Constants.TEXT_WITHDRAW_BUTTON,
                                             command=lambda: self.execute_transfer(Constants.STATE_WITHDRAWAL))
        self.withdraw_all_funds_button = Button(self.window,
                                                text=Constants.TEXT_WITHDRAW_ALL_BUTTON,
                                                command=lambda: self.execute_transfer(Constants.STATE_WITHDRAWAL_ALL))

    def show_widgets(self):
        """Metoda wyświetla na ekranie zdefiniowane widżety"""

        # wyświetlanie etykiet
        self.main_title_label.grid(row=0, column=0, sticky='nsew')
        self.main_description_label.grid(row=1, column=0, sticky='new')
        self.window.columnconfigure(0, weight=1)  # umieszczenie etykiet tytułowych na środku
        self.window.rowconfigure(1, weight=1)  # umieszczenie etykiet tytułowych u góry okna

        self.amount_label.place(x=0, y=500)
        self.account_balance_label.place(x=0, y=540)

        # wyświetlanie pól tekstowych
        self.amount_entry.place(x=70, y=500)

        # wyświetlanie przycisków
        self.close_button.place(x=700, y=500)
        self.deposit_amount_button.place(x=200, y=495)
        self.withdraw_amount_button.place(x=300, y=495)
        self.withdraw_all_funds_button.place(x=200, y=530)

    def execute_transfer(self, state):
        """Metoda wywołuje klasę obsługującą transfer pieniężny"""

        Transfer(self, self.window, state)

    def get_current_account_balance_text(self):
        return Constants.TEXT_CURRENT_BALANCE + str(Platform.account_balance) + Constants.TEXT_CURRENCY

    def clear_entry_text(self, entry):
        """Metoda czyści zawartość pola tekstowego"""

        entry.delete(0, END)

    def exit_platform(self):
        """Metoda zamyka główne okno aplikacji."""

        confirmation = messagebox.askokcancel(Constants.MESSAGE_CONFIRM_EXIT, Constants.MESSAGE_CONFIRM_EXIT_TEXT)
        if confirmation:
            self.window.destroy()


class Transfer(Widgets):
    """Obsługa transakcji wpłaty i wypłaty środków oraz aktualizacja stanu środków na kocie."""

    # TODO: clear textbox after successful transfer

    def __init__(self, widget_object, window, state):
        super().__init__(window)
        self.widget_object = widget_object
        self.state = state
        self.handle_transfer(self.state)

    def handle_transfer(self, state):
        """Metoda obsługuje proces transakcji"""

        if self.state == Constants.STATE_WITHDRAWAL_ALL:
            self.withdraw_all()
        else:
            amount = self.get_amount()
            is_correct = self.verify(amount, state)

            if is_correct:
                amount = round(float(amount), 2)  # kwota jest poprawna, zaokrąglamy ją do dwóch miejsc po przecinku
                if self.state == Constants.STATE_DEPOSIT:
                    self.deposit(amount)
                if self.state == Constants.STATE_WITHDRAWAL:
                    self.withdraw(amount)
            else:
                self.clear_entry_text(self.widget_object.amount_entry)

    def deposit(self, amount):
        """Metoda odpowiedzialna za wpłatę środków na konto"""

        response = messagebox.askokcancel("Potwierdź wpłatę", 'Czy na pewno chcesz wpłacić {} zł?'.format(amount))
        if response == 1:  # użytkownik potwierdził chęć wpłaty na konto
            Platform.account_balance += amount
            Platform.account_balance = round(Platform.account_balance, 2)
            messagebox.showinfo('', 'Pomyślnie dokonano wpłaty {} zł'.format(amount))
            update_label(self.widget_object.account_balance_label_text,
                         self.get_current_account_balance_text())
            self.clear_entry_text(self.widget_object.amount_entry)

    def withdraw(self, amount):
        """Metoda odpowiedzialna za wypłatę środków z konta"""

        response = messagebox.askokcancel("Potwierdź wypłatę", 'Czy na pewno chcesz wypłacić {} zł?'.format(amount))
        if response == 1:  # użytkownik potwierdził chęć wypłaty na konto
            Platform.account_balance -= amount
            Platform.account_balance = round(Platform.account_balance, 2)
            messagebox.showinfo('', 'Pomyślnie dokonano wypłaty {} zł'.format(amount))
            update_label(self.widget_object.account_balance_label_text,
                         self.get_current_account_balance_text())
            self.clear_entry_text(self.widget_object.amount_entry)

    def withdraw_all(self):
        """Metoda odpowiedzialna za wypłatę wszystkich środków z konta"""

        if Platform.account_balance == 0:
            return
        else:
            response = messagebox.askokcancel("Potwierdź wypłatę wszystkich środków",
                                              'Czy na pewno chcesz wypłacić {} zł?'.format(Platform.account_balance))
            if response == 1:  # użytkownik potwierdził chęć wypłaty wszystkich środków
                withdrawal_amount = Platform.account_balance
                Platform.account_balance = 0
                messagebox.showinfo('', 'Pomyślnie dokonano wypłaty {} zł'.format(withdrawal_amount))
                update_label(self.widget_object.account_balance_label_text,
                             self.get_current_account_balance_text())

    def get_amount(self):
        """Metoda odczytuje kwotę podaną przez użytkownika"""

        return self.widget_object.amount_entry.get()

    def verify(self, amount, state):
        """Metoda weryfikuję poprawność danych wprowadzonych przez użytkownika podczas podawania kwoty"""

        if len(amount) == 0:  # użytkownik nie podał żadnej kwoty
            return False  # ignorujemy żądanie

        try:
            amount = float(amount)
        except ValueError:
            show_error(Constants.MESSAGE_ERROR_VALUE)
            return False

        if amount < 0:
            show_error(Constants.MESSAGE_ERROR_VALUE)
            return False

        if amount == 0:
            return False

        if state == Constants.STATE_WITHDRAWAL:
            if Platform.account_balance - amount < 0:
                show_error(Constants.MESSAGE_ERROR_NEGATIVE_BALANCE)
                return False

        return True
