import functools
import math
from tkinter import *
from tkinter import messagebox
from src.constants import Constants
from src.data_provider import DataProvider

# TODO: hovering over buttons changes their colour
# TODO: add scrollbar to listbox
# TODO: sell button


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
            cls.show_error(Constants.MESSAGE_ERROR_VALUE)  # użytkownik podał ujemną kwotę
            return False

        if amount == 0:  # ignorujemy żądanie wpłaty 0zł
            return False

        return True


class Account:
    account_balance = 10000  # aktualny stan wolnych środków na konice
    value_of_shares_held = 0  # aktualna wartość posiadanych akcji
    total_account_value = account_balance + value_of_shares_held  # całkowita wartość konta

    purchased_stock_list = []  # lista posiadanych firm przez użytkownika

    # ---------------------------------------------------------------------------- #

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

    # ---------------------------------------------------------------------------- #

    def get_current_value_of_shares_held_text(self):
        return Constants.TEXT_VALUE_OF_SHARES_HELD + str(self.get_value_of_shares_held()) + Constants.TEXT_CURRENCY

    def get_value_of_shares_held(self):
        return self.value_of_shares_held

    def set_value_of_shares_held(self, amount):
        Account.value_of_shares_held = amount

    def increase_value_of_shares_held(self, amount):
        self.set_value_of_shares_held(self.get_value_of_shares_held() + amount)

    def decrease_value_of_shares_held(self, amount):
        self.set_value_of_shares_held(self.get_value_of_shares_held() - amount)

    # ---------------------------------------------------------------------------- #

    def get_total_account_value_text(self):
        return Constants.TEXT_TOTAL_ACCOUNT_VALUE + str(self.get_total_account_value()) + Constants.TEXT_CURRENCY

    def get_total_account_value(self):
        return self.total_account_value


class Market:
    """Klasa zarządza listą firm, których akcje można zakupić"""

    def __init__(self, stock_amount_spinbox, companies_listbox, account_balance_label_text, value_of_shares_held_label_text):
        self.available_companies = DataProvider.get_companies()
        self.stock_amount_spinbox = stock_amount_spinbox
        self.companies_listbox = companies_listbox

        self.account_balance_label_text = account_balance_label_text
        self.value_of_shares_held_label_text = value_of_shares_held_label_text

    def insert_available_companies(self):
        offset = 0
        for company in self.available_companies:
            combined_name = company.get_symbol() + str(company.get_price())
            self.companies_listbox.insert(END, combined_name)

            offset += 30

    def select_company(self, order_type):
        """Metoda obsługuje wybór firmy z listy dostępnych do zakupu akcji. Dzięki indeksowi na liście możemy powiązać daną pozycję z odpowiadającą jej klasą firmy."""

        # odczytujemy indeks wybranego elementu z listy firm - wynik jest w postaci jednoelementowej krotki
        selection_tuple = self.companies_listbox.curselection()

        if len(selection_tuple) == 0:
            # żaden element z listy nie został zaznaczony
            return

        # zamiana typu tuple na int
        index = functools.reduce(lambda a: a, selection_tuple)

        company = self.available_companies[index]

        stock_amount_str = self.stock_amount_spinbox.get()

        NewOrder(company, stock_amount_str, order_type, self.account_balance_label_text, self.value_of_shares_held_label_text)

        # po dokonaniu transakcji, odznaczamy element z listy
        self.companies_listbox.selection_clear(0, 'end')


class NewOrder(Account, VerifyUserInput):
    """Klasa obsługuje zlecenia zakupu/sprzedaży akcji"""

    def __init__(self, company, stock_amount, order_type, account_balance_label_text, value_of_shares_held_label_text):
        self.company = company
        self.stock_amount = stock_amount
        self.order_type = order_type
        self.share_price = self.company.get_price()
        self.company_name = self.company.get_name()

        self.account_balance_label_text = account_balance_label_text
        self.value_of_shares_held_label_text = value_of_shares_held_label_text

        verified = self.verify_user_input(str(self.stock_amount))

        if verified:
            self.stock_amount = int(stock_amount)
            if order_type == Constants.BUY_ORDER:
                self.handle_stock_buy_order()
            if order_type == Constants.SELL_ORDER:
                self.handle_stock_sell_order()

    def handle_stock_buy_order(self):
        """Obsługa zlecenia zakupu akcji"""

        # obliczenie wartości potencjalnej transakcji
        transaction_value = self.stock_amount * self.share_price

        if transaction_value > self.get_account_balance():
            # użytkownik nie posiada wystarczającej ilości środków na koncie do dokonania zakupu akcji
            self.show_error(Constants.MESSAGE_ERROR_NOT_ENOUGH_FUNDS)
        else:
            # prośba o potwierdzenie chęci zakupu + podanie informacji
            _response = messagebox.askokcancel(Constants.MESSAGE_CONFIRM_BUY_SHARES,
                                               'Czy na pewno chcesz zakupić {} akcji firmy {} za kwotę {} zł?'
                                               .format(self.stock_amount, self.company_name, transaction_value))

            if _response == 1:
                self.decrease_account_balance(transaction_value)
                self.increase_value_of_shares_held(transaction_value)

                messagebox.showinfo('Sukces', 'Pomyślnie dokonano zakupu {} akcji firmy {}'
                                    .format(self.stock_amount, self.company_name))

                self.update_label(self.value_of_shares_held_label_text,
                                  self.get_current_value_of_shares_held_text())
                self.update_label(self.account_balance_label_text,
                                  self.get_current_account_balance_text())

    def handle_stock_sell_order(self):
        """Obsługa zlecenia sprzedaży akcji"""
        pass


class Transfer(VerifyUserInput, Auxiliary, Account):
    """Obsługa transakcji wpłaty i wypłaty środków oraz aktualizacja stanu środków na kocie."""

    def __init__(self, amount_entry, account_balance_label_text):
        self.amount_entry = amount_entry
        self.account_balance_label_text = account_balance_label_text

    def handle_deposit(self):
        """Metoda obsługuje wpłatę środków na konto"""

        amount = self.get_amount()
        is_correct, deposit_amount = self.verify_deposit_amount(amount)
        if is_correct:
            response = messagebox.askokcancel("Potwierdź wpłatę",
                                              'Czy na pewno chcesz wpłacić {} zł?'.format(deposit_amount))
            if response == 1:
                # użytkownik potwierdził chęć wpłaty na konto
                self.increase_account_balance(deposit_amount)

                messagebox.showinfo('Sukces', 'Pomyślnie dokonano wpłaty {} zł'.format(deposit_amount))

                self.update_label(self.account_balance_label_text,
                                  self.get_current_account_balance_text())

        self.clear_entry_text(self.amount_entry)

    def verify_deposit_amount(self, deposit_amount):
        """Metoda weryfikuję poprawność kwoty wprowadzonej przez użytkownika"""

        verified = self.verify_user_input(deposit_amount)
        if verified:
            # kwota jest poprawna, ucinamy nadmiarową kwotę do dwóch miejsc po przecinku
            verified_amount = math.floor(float(deposit_amount) * 100.0) / 100.0

            if verified_amount < 100.0:
                messagebox.showinfo('Niewłaściwa kwota depozytu', 'Minimalny depozyt wynosi 100zł.')
                return False, 0
        else:
            return False, 0

        return True, verified_amount

    def handle_withdrawal(self, withdrawal_option):
        """Metoda obsługuje wypłatę środków z konta"""

        if withdrawal_option == Constants.WITHDRAWAL:
            # użytkownik wybrał wypłatę danej kwoty z konta
            amount = self.get_amount()

            correct_input = self.verify_user_input(amount)
            if not correct_input:
                self.clear_entry_text(self.amount_entry)
                return
            else:
                # kwota jest poprawna, ucinamy nadmiarową kwotę do dwóch miejsc po przecinku
                withdrawal_amount = math.floor(float(amount) * 100.0) / 100.0

        elif withdrawal_option == Constants.WITHDRAWAL_ALL:
            # użytkownik wybrał wypłatę wszystkich wolnych środków z konta
            withdrawal_amount = self.get_account_balance()
            if withdrawal_amount == 0:
                # stan środków na koncie wynosi już 0zł
                return
        else:
            return

        correct, will_pay_commission = self.verify_withdrawal_amount(withdrawal_amount,
                                                                     Constants.WITHDRAWAL_COMMISSION_THRESHOLD,
                                                                     Constants.WITHDRAWAL_COMMISSION_AMOUNT)
        if not correct:
            self.clear_entry_text(self.amount_entry)
            return

        if will_pay_commission:
            commission_amount = Constants.WITHDRAWAL_COMMISSION_AMOUNT
        else:
            commission_amount = 0

        response = messagebox.askokcancel("Potwierdź wypłatę",
                                          'Czy na pewno chcesz wypłacić {} zł?\n'
                                          'Prowizja wyniesie: {} zł.'.format(withdrawal_amount, commission_amount))
        if response == 1:  # użytkownik potwierdził chęć wypłaty z konta
            # dokonujemy wypłaty środków wraz z ewentualnym poborem prowizji
            if will_pay_commission:
                withdrawal_amount -= Constants.WITHDRAWAL_COMMISSION_AMOUNT
                self.decrease_account_balance(Constants.WITHDRAWAL_COMMISSION_AMOUNT)

            self.decrease_account_balance(withdrawal_amount)

            messagebox.showinfo('Sukces', 'Pomyślnie dokonano wypłaty {} zł'.format(withdrawal_amount))
            self.update_label(self.account_balance_label_text,
                              self.get_current_account_balance_text())

            self.clear_entry_text(self.amount_entry)

    def verify_withdrawal_amount(self, withdrawal_amount, withdrawal_commission_threshold,
                                 withdrawal_commission_amount):
        """Metoda weryfikuję poprawność danych wprowadzonych przez użytkownika podczas podawania kwoty oraz wyznacza wysokość prowizji"""

        current_account_balance = self.get_account_balance()

        if current_account_balance - withdrawal_amount < 0.0:
            # użytkownik nie ma wystarczającego stanu konta, żeby wypłacić podaną ilość środków
            self.show_error(Constants.MESSAGE_ERROR_NEGATIVE_BALANCE)
            correct = False
            will_pay_commission = False

        elif withdrawal_amount > withdrawal_commission_threshold:
            # użytkownik nie płaci prowizji za wypłatę
            correct = True
            will_pay_commission = False

        else:
            # użytkownik powinien zapłacić prowizję
            will_pay_commission = True

            if current_account_balance == withdrawal_amount and current_account_balance > withdrawal_commission_amount:
                # użytkownik wypłaca wszystkie środki z konta oraz posiada wystarczającą ilość środków na pokrycie prowizji
                correct = True
                will_pay_commission = True

            elif current_account_balance < (withdrawal_amount + withdrawal_commission_amount):
                # użytkownik nie ma wystarczającego stanu konta, żeby zapłacić prowizję
                self.show_error(Constants.MESSAGE_ERROR_NEGATIVE_BALANCE)
                correct = False
            else:
                # użytkownik ma wystarczający stan konta, żeby zapłacić prowizję
                correct = True

        return correct, will_pay_commission

    def get_amount(self):
        """Metoda odczytuje kwotę podaną przez użytkownika"""

        return self.amount_entry.get()
