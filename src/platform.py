import functools
import math
from tkinter import *
from tkinter import messagebox
from src.constants import Constants
from src.data_provider import DataProvider


# class Platform:
#     """Główna klasa platformy transakcyjnej"""
#     # TODO: subclasses inside Platform ?
#
#     def __init__(self, window):
#         self.window = window
#         # Account()
#         # Market(window)
#         # TODO: hovering over buttons changes their colour


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

    @classmethod
    def exit_platform(cls, window):
        """Metoda zamyka główne okno aplikacji."""

        confirmation = messagebox.askokcancel(Constants.MESSAGE_CONFIRM_EXIT, Constants.MESSAGE_CONFIRM_EXIT_TEXT)
        if confirmation:
            window.destroy()


class VerifyUserInput(Auxiliary):
    """Klasa weryfikuję poprawność danych wprowadzonych przez użytkownika"""

    @classmethod
    def verify_user_input(cls, user_input):
        if len(user_input) == 0:  # użytkownik nie podał żadnej wartości
            return False  # ignorujemy żądanie

        try:
            amount = float(user_input)
        except ValueError:
            cls.show_error(Constants.MESSAGE_ERROR_VALUE)  # podana przez użytkownika wartość nie jest poprawną liczbą
            return False

        if amount < 0:
            cls.show_error(Constants.MESSAGE_ERROR_VALUE)
            return False

        if amount == 0:
            return False

        return True


class Account:
    account_balance = 0  # aktualny stan wolnych środków na konice
    purchased_stock_list = []  # lista posiadanych firm przez użytkownika

    def get_current_account_balance_text(self):
        return Constants.TEXT_CURRENT_BALANCE + str(self.get_account_balance()) + Constants.TEXT_CURRENCY

    def get_account_balance(self):
        return self.account_balance

    def set_account_balance(self, amount):
        Account.account_balance = amount

    def increase_account_balance(self, amount):
        self.set_account_balance(self.get_account_balance() + amount)

    def decrease_account_balance(self, amount):
        self.set_account_balance(self.get_account_balance() - amount)


class Market:
    """Klasa zarządza listą firm, których akcje można zakupić"""

    def __init__(self, stock_amount_spinbox, companies_listbox):
        self.available_companies = DataProvider.get_companies()
        self.stock_amount_spinbox = stock_amount_spinbox
        self.companies_listbox = companies_listbox

        # TODO: add scrollbar to listbox
        # TODO: ability to deselect company from a list or show popup-like thing
        # TODO: handle error - clicking button when no item in listbox is selected
        # TODO: sell button
        # TODO: remove ability to buy when not selected

        # self.insert_available_companies()

    def insert_available_companies(self):
        offset = 0
        for company in self.available_companies:
            combined_name = company.get_symbol() + company.get_price()
            self.companies_listbox.insert(END, combined_name)

            offset += 30

    def select_company(self, order_type):
        """Metoda obsługuje wybór firmy z listy dostępnych do zakupu akcji. Dzięki indeksowi na liście możemy powiązać daną pozycję z odpowiadającą jej klasą firmy."""

        selection_tuple = self.companies_listbox.curselection()  # odczytujemy indeks wybranego elementu z listy firm - wynik jest w postaci jednoelementowej krotki
        if len(selection_tuple) == 0:  # żaden element z listy nie został zaznaczony
            return

        index = functools.reduce(lambda a: a, selection_tuple)  # zamiana typu tuple na int
        company = self.available_companies[index]

        stock_amount = self.stock_amount_spinbox.get()

        NewOrder(company, stock_amount, order_type)
        self.companies_listbox.selection_clear(0, 'end')  # po dokonaniu transakcji, odznaczamy element z listy


class NewOrder(Account, VerifyUserInput):
    """Klasa obsługuje zlecenia zakupu/sprzedaży akcji"""

    def __init__(self, company, stock_amount, order_type):  # stock_amount
        self.company = company
        self.stock_amount = stock_amount
        self.order_type = order_type

        verified = self.verify_user_input(stock_amount)

        if verified:
            if order_type == Constants.BUY_ORDER:
                self.handle_stock_buy_order()
            if order_type == Constants.SELL_ORDER:
                self.handle_stock_sell_order()

    def handle_stock_buy_order(self):
        """Obsługa zlecenia zakupu akcji"""

        print("company: ", self.company.get_name())
        print("stock amount: ", self.stock_amount)

    def handle_stock_sell_order(self):
        """Obsługa zlecenia sprzedaży akcji"""
        pass


class Transfer(VerifyUserInput, Auxiliary, Account):
    """Obsługa transakcji wpłaty i wypłaty środków oraz aktualizacja stanu środków na kocie."""

    # TODO: clear textbox after successful transfer

    def __init__(self, amount_entry, account_balance_label_text):
        self.amount_entry = amount_entry
        self.account_balance_label_text = account_balance_label_text

    def handle_transfer(self, transfer_type):
        """Metoda obsługuje proces transakcji"""

        if transfer_type == Constants.WITHDRAWAL_ALL:
            self.withdraw_all()
        else:
            amount = self.get_amount()
            is_correct, amount = self.verify_amount(amount, transfer_type)
            if is_correct:

                if transfer_type == Constants.DEPOSIT:
                    self.deposit(amount)
                if transfer_type == Constants.WITHDRAWAL:
                    self.withdraw(amount)
            else:
                self.clear_entry_text(self.amount_entry)

    def deposit(self, amount):
        """Metoda odpowiedzialna za wpłatę środków na konto"""

        if amount < 100.0:
            messagebox.showinfo('Niewłaściwa kwota depozytu', 'Minimalny depozyt wynosi 100zł.')
            return
        else:
            response = messagebox.askokcancel("Potwierdź wpłatę", 'Czy na pewno chcesz wpłacić {} zł?'.format(amount))
            if response == 1:  # użytkownik potwierdził chęć wpłaty na konto
                self.increase_account_balance(amount)

                messagebox.showinfo('', 'Pomyślnie dokonano wpłaty {} zł'.format(amount))
                self.update_label(self.account_balance_label_text,
                                  self.get_current_account_balance_text())
        self.clear_entry_text(self.amount_entry)

    def withdraw(self, amount):
        """Metoda odpowiedzialna za wypłatę środków z konta"""

        response = messagebox.askokcancel("Potwierdź wypłatę", 'Czy na pewno chcesz wypłacić {} zł?'.format(amount))
        if response == 1:  # użytkownik potwierdził chęć wypłaty na konto
            self.decrease_account_balance(amount)
            messagebox.showinfo('', 'Pomyślnie dokonano wypłaty {} zł'.format(amount))
            self.update_label(self.account_balance_label_text,
                              self.get_current_account_balance_text())
            self.clear_entry_text(self.amount_entry)

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
                self.update_label(self.account_balance_label_text,
                                  self.get_current_account_balance_text())

    def get_amount(self):
        """Metoda odczytuje kwotę podaną przez użytkownika"""

        return self.amount_entry.get()

    def verify_amount(self, amount, transfer_type):
        """Metoda weryfikuję poprawność danych wprowadzonych przez użytkownika podczas podawania kwoty"""

        verified = self.verify_user_input(amount)

        if verified:
            verified_amount = math.floor(float(amount) * 100.0) / 100.0  # kwota jest poprawna, ucinamy nadmiarową kwotę do dwóch miejsc po przecinku

        else:
            return False, 0

        if transfer_type == Constants.WITHDRAWAL:
            if self.get_account_balance() - verified_amount < 0:
                self.show_error(Constants.MESSAGE_ERROR_NEGATIVE_BALANCE)
                return False, 0

        return True, verified_amount
