import math
from tkinter import messagebox
from src.Utilities.constants import Constants
from src.Repository.data_provider import DataProvider


class Auxiliary:
    """Klasa zawiera zbiór metod pomocniczych, używanych przez poszczególne elementy platformy"""

    @staticmethod
    def show_error(error_message):
        """Wyświetlenie okna z komunikatem błędu."""

        messagebox.showerror(Constants.MESSAGE_ERROR, error_message)

    @staticmethod
    def exit_platform(window):
        """Metoda zamyka główne okno aplikacji."""

        confirmation = messagebox.askokcancel(Constants.MESSAGE_CONFIRM_EXIT, Constants.MESSAGE_CONFIRM_EXIT_TEXT)
        if confirmation:
            window.destroy()


class Error(Exception):
    """Klasa bazowa dla wyjątków w tym module"""
    pass


class DepositTooSmallException(Error):
    """Wyjątek zgłoszony, gdy użytkownik chce zdeponować kwotę poniżej progu minimalnego depozytu"""

    def __init__(self, amount):
        self.amount = amount
        Auxiliary.show_error(
            Constants.MESSAGE_INSUFFICIENT_DEPOSIT_AMOUNT + str(amount) + Constants.TEXT_CURRENCY + '\n'
            + Constants.MESSAGE_MINIMAL_DEPOSIT_AMOUNT)


class NegativeBalanceException(Error):
    """Wyjątek zgłoszony, gdy użytkownik chce wypłacić z konta kwotę większą niż stan wolnych środków"""

    def __init__(self):
        Auxiliary.show_error(Constants.MESSAGE_ERROR_NEGATIVE_BALANCE)


class VerifyUserInput(Auxiliary):
    """Klasa weryfikuję poprawność danych wprowadzonych przez użytkownika"""

    @classmethod
    def verify_user_input(cls, user_input):
        if len(user_input) == 0:
            # użytkownik nie podał żadnej wartości - żądanie zostaje zignorowane
            return False

        try:
            amount = float(user_input)
        except ValueError:
            # podana przez użytkownika wartość nie jest poprawną liczbą
            cls.show_error(Constants.MESSAGE_ERROR_VALUE)
            return False

        if amount < 0:
            # użytkownik podał ujemną kwotę
            cls.show_error(Constants.MESSAGE_ERROR_VALUE)
            return False

        if amount == 0:
            # żądanie wpłaty 0zł zostaje zignorowane
            return False

        return True


class Account:
    account_balance = 0  # aktualny stan wolnych środków na konice
    value_of_shares_held = 0  # aktualna wartość posiadanych akcji

    DataProvider.instantiate_companies()
    purchased_companies = DataProvider.make_companies_dict()
    purchased_companies_listbox_indexes = {}  # pozycje firm na liście zakupionych akcji

    def get_current_account_balance_text(self):
        return Constants.TEXT_CURRENT_BALANCE + str(self.get_account_balance()) + Constants.TEXT_CURRENCY

    def get_account_balance(self):
        return self.account_balance

    @staticmethod
    def set_account_balance(amount):
        Account.account_balance = amount

    def increase_account_balance(self, amount):
        self.set_account_balance(self.get_account_balance() + amount)

    def decrease_account_balance(self, amount):
        self.set_account_balance(self.get_account_balance() - amount)

    # ---------------------------------------------------------------------------- #

    def get_value_of_shares_held_text(self):
        return Constants.TEXT_VALUE_OF_SHARES_HELD + str(self.get_value_of_shares_held()) + Constants.TEXT_CURRENCY

    def get_value_of_shares_held(self):
        return self.value_of_shares_held

    @staticmethod
    def set_value_of_shares_held(amount):
        Account.value_of_shares_held = amount

    def increase_value_of_shares_held(self, amount):
        self.set_value_of_shares_held(self.get_value_of_shares_held() + amount)

    def decrease_value_of_shares_held(self, amount):
        self.set_value_of_shares_held(self.get_value_of_shares_held() - amount)

    # ---------------------------------------------------------------------------- #

    def get_total_account_value_text(self):
        return Constants.TEXT_TOTAL_ACCOUNT_VALUE + str(self.get_total_account_value()) + Constants.TEXT_CURRENCY

    def get_total_account_value(self):
        return self.get_account_balance() + self.get_value_of_shares_held()


class PlatformAccount:
    platform_balance = 0  # wartość pobranych prowizji przez platformę

    def get_platform_balance(self):
        return self.platform_balance

    @staticmethod
    def set_platform_balance(amount):
        PlatformAccount.platform_balance = amount

    def increase_platform_balance(self, amount):
        return self.set_platform_balance(self.get_platform_balance() + amount)


class NewOrder(PlatformAccount, Account, Auxiliary):
    """Klasa obsługuje zlecenia zakupu/sprzedaży akcji"""

    def select_company(self, order_type, company_index, stock_amount):
        """Metoda obsługuje wybór firmy z listy dostępnych do zakupu akcji. Dzięki indeksowi na liście możemy powiązać daną pozycję z odpowiadającą jej klasą firmy."""

        company = DataProvider.get_company(company_index)

        # weryfikacja danych wprowadzonych przez użytkownika
        verified = VerifyUserInput.verify_user_input(stock_amount)

        if not verified:
            return

        stock_amount = int(stock_amount)
        share_price = company.get_price()

        # obliczenie wartości potencjalnej transakcji
        transaction_value = stock_amount * share_price

        if order_type == Constants.BUY_ORDER:
            successful_transaction = self.handle_stock_buy_order(company, transaction_value, stock_amount)
        elif order_type == Constants.SELL_ORDER:
            successful_transaction = self.handle_stock_sell_order(company, transaction_value, stock_amount)
        else:
            successful_transaction = False

        return successful_transaction

    def handle_stock_buy_order(self, company, transaction_value, stock_amount):
        """Obsługa zlecenia zakupu akcji"""

        company_name = company.get_name()
        company_symbol = company.get_symbol()

        if transaction_value > self.get_account_balance():
            # użytkownik nie posiada wystarczającej ilości środków na koncie do dokonania zakupu akcji
            self.show_error(Constants.MESSAGE_ERROR_NOT_ENOUGH_FUNDS)
            successful_transaction = False
        else:
            # prośba o potwierdzenie chęci zakupu + podanie informacji o transakcji
            _response = messagebox.askokcancel(Constants.MESSAGE_CONFIRM_BUY_SHARES,
                                               'Czy na pewno chcesz zakupić {} akcji firmy {} za kwotę {} zł?'
                                               .format(stock_amount, company_name, transaction_value))

            if _response == 1:
                self.decrease_account_balance(transaction_value)
                self.increase_value_of_shares_held(transaction_value)

                # aktualizacja liczby posiadanych akcji danej firmy
                self.purchased_companies[company_symbol] += stock_amount

                messagebox.showinfo('Sukces', 'Pomyślnie dokonano zakupu {} akcji firmy {}'
                                    .format(stock_amount, company_name))

                successful_transaction = True
            else:
                successful_transaction = False

        return successful_transaction

    def handle_stock_sell_order(self, company, transaction_value, stock_amount):
        """Obsługa zlecenia sprzedaży akcji"""

        company_name = company.get_name()
        company_symbol = company.get_symbol()

        if self.purchased_companies[company_symbol] < stock_amount:
            # użytkownik nie posiada wystarczającej ilości akcji wybranej firmy
            self.show_error(Constants.MESSAGE_ERROR_NOT_ENOUGH_SHARES)
            return

        # prośba o potwierdzenie chęci sprzedaży + podanie informacji o transakcji
        _response = messagebox.askokcancel(Constants.MESSAGE_CONFIRM_SELL_SHARES,
                                           'Czy na pewno chcesz zakupić {} akcji firmy {} za kwotę {} zł?'
                                           .format(stock_amount, company_name, transaction_value))

        if _response == 1:
            self.increase_account_balance(transaction_value)
            self.decrease_value_of_shares_held(transaction_value)

            # aktualizacja liczby posiadanych akcji danej firmy
            self.purchased_companies[company_symbol] -= stock_amount

            messagebox.showinfo('Sukces', 'Pomyślnie dokonano sprzedaży {} akcji firmy {}'
                                .format(stock_amount, company_name))

            successful_transaction = True
        else:
            successful_transaction = False

        return successful_transaction


class Transfer(PlatformAccount, Account, Auxiliary):
    """Obsługa transakcji wpłaty i wypłaty środków oraz aktualizacja stanu środków na kocie."""

    def __init__(self):
        self.paid_commission_amount = 0
        self.withdrawal_amount = 0

    def handle_deposit(self, amount):
        """Metoda obsługuje wpłatę środków na konto"""

        verified_input = VerifyUserInput.verify_user_input(str(amount))
        if not verified_input:
            # użytkownik nie podał poprawnej kwoty
            return
        else:
            # kwota jest poprawna, ucinamy nadmiarową kwotę do dwóch miejsc po przecinku
            deposit_amount = math.floor(float(amount) * 100.0) / 100.0

        correct_value = self.verify_deposit_amount(deposit_amount)
        if not correct_value:
            # podana kwota nie spełnia warunków depozytu
            return

        response = messagebox.askokcancel("Potwierdź wpłatę",
                                          'Czy na pewno chcesz wpłacić {} zł?'.format(deposit_amount))
        if response == 1:
            # użytkownik potwierdził chęć wpłaty na konto
            self.increase_account_balance(deposit_amount)

            messagebox.showinfo('Sukces', 'Pomyślnie dokonano wpłaty {} zł'.format(deposit_amount))

    @staticmethod
    def verify_deposit_amount(deposit_amount):
        """Metoda weryfikuję poprawność kwoty wprowadzonej przez użytkownika"""

        if deposit_amount < Constants.MINIMAL_DEPOSIT_AMOUNT:
            try:
                raise DepositTooSmallException(deposit_amount)
            except DepositTooSmallException as err:
                pass
            return False
        else:
            return True

    def handle_withdrawal(self, amount, withdrawal_option):
        """Metoda obsługuje wypłatę środków z konta"""

        if withdrawal_option == Constants.WITHDRAWAL:
            # użytkownik wybrał wypłatę danej kwoty z konta

            correct_input = VerifyUserInput.verify_user_input(str(amount))
            if not correct_input:
                return
            else:
                # kwota jest poprawna, ucinamy nadmiarową kwotę do dwóch miejsc po przecinku
                self.withdrawal_amount = math.floor(float(amount) * 100.0) / 100.0

        elif withdrawal_option == Constants.WITHDRAWAL_ALL:
            # użytkownik wybrał wypłatę wszystkich wolnych środków z konta
            withdrawal_amount = self.get_account_balance()
            if withdrawal_amount == 0:
                # stan środków na koncie wynosi już 0zł
                return
        else:
            return

        correct, will_pay_commission = self.verify_withdrawal_amount(self.withdrawal_amount,
                                                                     Constants.WITHDRAWAL_COMMISSION_THRESHOLD,
                                                                     Constants.WITHDRAWAL_COMMISSION_AMOUNT)
        if not correct:
            return

        if will_pay_commission:
            # użytkownik płaci prowizję
            self.paid_commission_amount = Constants.WITHDRAWAL_COMMISSION_AMOUNT

            # pomniejszenie kwoty, którą otrzyma użytkownik o wysokość prowizji
            self.withdrawal_amount -= self.paid_commission_amount

        else:
            # użytkownik nie płaci prowizji
            self.paid_commission_amount = 0

        response = messagebox.askokcancel("Potwierdź wypłatę",
                                          'Czy na pewno chcesz wypłacić {} zł?\n'
                                          'Prowizja wyniesie: {} zł.'.format(self.withdrawal_amount + self.paid_commission_amount,
                                                                             self.paid_commission_amount))
        if response == 1:  # użytkownik potwierdził chęć wypłaty z konta

            # przekazanie prowizji na konto platformy
            self.decrease_account_balance(self.paid_commission_amount)
            self.increase_platform_balance(self.paid_commission_amount)

            # wypłata użytkownikowi kwoty pomniejszonej o wysokość prowizji
            self.decrease_account_balance(self.withdrawal_amount)

            messagebox.showinfo('Sukces', 'Pomyślnie dokonano wypłaty {} zł.\n'
                                          'Prowizja wyniosła {} zł.'.format(self.withdrawal_amount,
                                                                            self.paid_commission_amount))

    def verify_withdrawal_amount(self, withdrawal_amount, withdrawal_commission_threshold,
                                 withdrawal_commission_amount):
        """Metoda weryfikuję poprawność danych wprowadzonych przez użytkownika podczas podawania kwoty oraz wyznacza wysokość prowizji"""

        current_account_balance = self.get_account_balance()

        if withdrawal_amount < (withdrawal_commission_amount + 0.5):
            messagebox.showinfo('Informacja', 'Minimalna wypłata wynosi {} zł.'
                                .format(Constants.WITHDRAWAL_COMMISSION_AMOUNT + 0.5))
            return False, False

        if current_account_balance - withdrawal_amount < 0.0:
            # użytkownik nie ma wystarczającego stanu konta, żeby wypłacić podaną ilość środków
            try:
                raise NegativeBalanceException
            except NegativeBalanceException:
                pass

            correct = False
            will_pay_commission = False
            return correct, will_pay_commission

        correct = True

        if withdrawal_amount > withdrawal_commission_threshold:
            # użytkownik nie płaci prowizji za wypłatę

            will_pay_commission = False

        else:
            # użytkownik powinien zapłacić prowizję
            will_pay_commission = True

        return correct, will_pay_commission
