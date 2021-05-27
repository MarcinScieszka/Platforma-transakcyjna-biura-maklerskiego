from tkinter import *
from tkinter import messagebox
from src.constants import Constants
from src.data_provider import DataProvider
from src.gui import CreateGui
import functools


class Auxiliary:
    """Klasa zawiera zbiór metod pomocniczych, używanych przez poszczególne elementy platformy"""

    @classmethod
    def show_error(cls, error_message):
        """Wyświetlenie okna z komunikatem błędu."""

        messagebox.showerror(Constants.MESSAGE_ERROR, error_message)

    @classmethod
    def update_label(cls, label_text_var, label_text):
        """Aktualizacja nazwy danej etykiety"""

        label_text_var.set(label_text)

    @classmethod
    def clear_entry_text(cls, entry):
        """Metoda czyści zawartość pola tekstowego"""

        entry.delete(0, END)


class Account:
    account_balance = 0  # aktualny stan wolnych środków na konice
    purchased_stock_list = []  # lista posiadanych firm przez użytkownika

    def get_current_account_balance_text(self):
        return Constants.TEXT_CURRENT_BALANCE + str(self.get_account_balance()) + Constants.TEXT_CURRENCY

    def get_account_balance(self):
        return Account.account_balance

    def set_account_balance(self, amount):
        Account.account_balance = amount

    def increase_account_balance(self, amount):
        Account.account_balance += amount
        self.set_account_balance(round(self.get_account_balance(), 2))

    def decrease_account_balance(self, amount):
        Account.account_balance -= amount
        self.set_account_balance(round(self.get_account_balance(), 2))


class Platform:
    """Główna klasa platformy transakcyjnej"""

    def __init__(self, window):
        self.window = window
        CreateGui.create_gui_params(window)  # wywołanie klasy ustawiającej parametry gui
        Widgets(window)
        Account()
        Market(window)
        # TODO: hovering over buttons changes their colour


class Market:
    """Klasa zarządza listą firm, których akcje można zakupić"""

    def __init__(self, window):
        self.available_companies = DataProvider.get_companies()
        self.window = window

        # TODO: add scrollbar to listbox
        # TODO: ability to deselect company from a list or show popup-like thing
        # TODO: handle error - clicking button when no item in listbox is selected

        # stworzenie i wyświetlenie listy dostępnych firm
        self.companies_listbox = Listbox(self.window,
                                         bg=Constants.COLOUR_BACKGROUND,
                                         selectbackground=Constants.COLOUR_BACKGROUND,
                                         fg='white',
                                         width=40,
                                         font=Constants.FONT_TYPEFACE,
                                         cursor='hand2',
                                         bd=0,
                                         highlightthickness=0)

        self.companies_listbox.place(x=150, y=250)

        self.insert_available_companies()

        # pole tekstowe umożliwiające wybór ilości akcji danej firmy
        self.stock_amount_spinbox = Spinbox(self.window, from_=1, to=5)
        self.stock_amount_spinbox.place(x=400, y=350)

        self.buy_shares_button = Button(self.window,
                                        background='#f1f1f1',
                                        fg='black',
                                        bd=0,
                                        # relief=RAISED, # relief can be flat, groove, raised, ridge, solid, or sunken
                                        cursor="hand2",
                                        text="Zakup akcje",
                                        command=lambda: self.select_company())

        self.buy_shares_button.place(x=20, y=200)

    def insert_available_companies(self):
        offset = 0
        for company in self.available_companies:
            combined_name = company.get_symbol() + company.get_price()
            self.companies_listbox.insert(END, combined_name)

            offset += 30

    def select_company(self):
        """Metoda obsługuje wybór firmy z listy dostępnych do zakupu akcji. Dzięki indeksowi na liście możemy powiązać daną pozycję z odpowiadającą jej klasą firmy."""

        selection_tuple = self.companies_listbox.curselection()  # odczytujemy indeks wybranego elementu z listy firm - wynik jest w postaci jednoelementowej krotki
        index = functools.reduce(lambda a: a, selection_tuple)  # zamiana typu tuple na int
        company = self.available_companies[index]

        stock_amount = self.stock_amount_spinbox.get()

        NewOrder(company, stock_amount, Constants.BUY_ORDER)


class NewOrder(Account):
    """Klasa obsługuje zlecenia zakupu/sprzedaży akcji"""

    def __init__(self, company, stock_amount, type):  # stock_amount
        self.company = company
        self.stock_amount = stock_amount
        self.type = type

        if type == Constants.BUY_ORDER:
            self.handle_stock_buy_order()
        if type == Constants.SELL_ORDER:
            self.handle_stock_sell_order()

    def handle_stock_buy_order(self):
        """Obsługa zlecenia zakupu akcji"""

        print("company: ", self.company.get_name())
        print("stock amount: ", self.stock_amount)

    def handle_stock_sell_order(self):
        """Obsługa zlecenia sprzedaży akcji"""

        pass


class Widgets(Account):
    """Klasa obsługująca widżety"""

    count = 0  # zmienna zlicza ilość wywołań klasy, dzięki czemu możemy tworzyć widżety tylko podczas pierwszego wywołania klasy

    def __init__(self, window):
        self.window = window

        if Widgets.count == 0:  # zapewniamy jednokrotne tworzenie widżetów

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
                                       cursor="hand2",
                                       command=lambda: self.exit_platform(),
                                       padx=10)
            self.deposit_amount_button = Button(self.window,
                                                text=Constants.TEXT_DEPOSIT_BUTTON,
                                                cursor="hand2",
                                                command=lambda: self.execute_transfer(Constants.STATE_DEPOSIT))
            self.withdraw_amount_button = Button(self.window,
                                                 text=Constants.TEXT_WITHDRAW_BUTTON,
                                                 cursor="hand2",
                                                 command=lambda: self.execute_transfer(Constants.STATE_WITHDRAWAL))
            self.withdraw_all_funds_button = Button(self.window,
                                                    text=Constants.TEXT_WITHDRAW_ALL_BUTTON,
                                                    cursor="hand2",
                                                    command=lambda: self.execute_transfer(
                                                        Constants.STATE_WITHDRAWAL_ALL))

            self.show_widgets()  # wyświetlenie startowych widżetów

        Widgets.count += 1

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

    def exit_platform(self):
        """Metoda zamyka główne okno aplikacji."""

        confirmation = messagebox.askokcancel(Constants.MESSAGE_CONFIRM_EXIT, Constants.MESSAGE_CONFIRM_EXIT_TEXT)
        if confirmation:
            self.window.destroy()


class Transfer(Widgets, Auxiliary, Account):
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
            self.increase_account_balance(amount)

            messagebox.showinfo('', 'Pomyślnie dokonano wpłaty {} zł'.format(amount))
            self.update_label(self.widget_object.account_balance_label_text,
                              self.get_current_account_balance_text())
            self.clear_entry_text(self.widget_object.amount_entry)

    def withdraw(self, amount):
        """Metoda odpowiedzialna za wypłatę środków z konta"""

        response = messagebox.askokcancel("Potwierdź wypłatę", 'Czy na pewno chcesz wypłacić {} zł?'.format(amount))
        if response == 1:  # użytkownik potwierdził chęć wypłaty na konto
            self.decrease_account_balance(amount)
            messagebox.showinfo('', 'Pomyślnie dokonano wypłaty {} zł'.format(amount))
            self.update_label(self.widget_object.account_balance_label_text,
                              self.get_current_account_balance_text())
            self.clear_entry_text(self.widget_object.amount_entry)

    def withdraw_all(self):
        """Metoda odpowiedzialna za wypłatę wszystkich środków z konta"""

        current_account_balance = self.get_account_balance()
        if current_account_balance == 0:
            return
        else:
            response = messagebox.askokcancel("Potwierdź wypłatę wszystkich środków",
                                              'Czy na pewno chcesz wypłacić {} zł?'.format(current_account_balance))
            if response == 1:  # użytkownik potwierdził chęć wypłaty wszystkich środków
                withdrawal_amount = current_account_balance
                self.set_account_balance(0)

                messagebox.showinfo('', 'Pomyślnie dokonano wypłaty {} zł'.format(withdrawal_amount))
                self.update_label(self.widget_object.account_balance_label_text,
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
            self.show_error(Constants.MESSAGE_ERROR_VALUE)
            return False

        if amount < 0:
            self.show_error(Constants.MESSAGE_ERROR_VALUE)
            return False

        if amount == 0:
            return False

        if state == Constants.STATE_WITHDRAWAL:
            if self.get_account_balance() - amount < 0:
                self.show_error(Constants.MESSAGE_ERROR_NEGATIVE_BALANCE)
                return False

        return True
