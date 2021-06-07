import math
from tkinter import messagebox

from src.Repository.data_provider import DataProvider
from src.Utilities.constants import Constants


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


class MinimalDepositException(Error):
    """Wyjątek zgłoszony, gdy użytkownik chce zdeponować kwotę poniżej progu minimalnego depozytu"""

    def __init__(self, amount):
        self.amount = amount
        Auxiliary.show_error(
            Constants.MESSAGE_INSUFFICIENT_DEPOSIT_AMOUNT + str(amount) + Constants.TEXT_CURRENCY + '\n'
            + Constants.MESSAGE_MINIMAL_DEPOSIT_AMOUNT)


class MinimalWithdrawalException(Error):
    """Wyjątek zgłoszony, gdy użytkownik chce wypłacić kwotę poniżej progu minimalnej wypłaty"""

    def __init__(self, amount):
        self.amount = amount
        Auxiliary.show_error(Constants.MESSAGE_ERROR_MINIMAL_WITHDRAWAL_AMOUNT + Constants.TEXT_CURRENCY)


class NegativeBalanceException(Error):
    """Wyjątek zgłoszony, gdy użytkownik chce wypłacić z konta kwotę większą niż stan wolnych środków"""

    def __init__(self):
        Auxiliary.show_error(Constants.MESSAGE_ERROR_NEGATIVE_BALANCE)


class NotEnoughFundsException(Error):
    """Wyjątek zgłoszony, gdy użytkownik chce zakupić akcje za kwotę większą niż stan wolnych środków"""

    def __init__(self, total_transaction_value):
        self.total_transaction_value = total_transaction_value

        Auxiliary.show_error(Constants.MESSAGE_ERROR_NOT_ENOUGH_FUNDS + '\n' +
                             "Kwota potrzebna do realizacji zlecenia : " + str(self.total_transaction_value) +
                             Constants.TEXT_CURRENCY)


class NotEnoughSharesException(Error):
    """Wyjątek zgłoszony, gdy użytkownik chce sprzedać więcej akcji, niż aktualnie posiada"""

    def __init__(self):
        Auxiliary.show_error(Constants.MESSAGE_ERROR_NOT_ENOUGH_SHARES)


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
    DataProvider.instantiate_companies()  # stworzenie instancji obiektów firm
    __account_balance = 0  # aktualny stan wolnych środków na konice
    __value_of_shares_held = 0  # aktualna wartość posiadanych akcji
    _owned_shares_tracker = DataProvider.make_companies_dict()  # słownik z aktualną liczbą posiadanych akcji poszczególnych firm
    _bought_companies_listbox_indexes = {}  # pozycje firm na liście zakupionych akcji

    def check_if_company_is_already_bought(self, company_symbol) -> bool:
        if company_symbol in self._bought_companies_listbox_indexes:
            return True
        else:
            return False

    def get_bought_company_listbox_index(self, company_symbol):
        return self._bought_companies_listbox_indexes.get(company_symbol)

    def append_bought_company_to_listbox(self, company_symbol):
        self._bought_companies_listbox_indexes[company_symbol] = len(
            self._bought_companies_listbox_indexes)

    def get_nr_of_shares_owned(self, company_symbol):
        return self._owned_shares_tracker.get(company_symbol)

    def set_nr_of_owned_shares(self, company_symbol, amount):
        self._owned_shares_tracker[company_symbol] = amount

    def get_current_account_balance_text(self):
        return Constants.TEXT_CURRENT_BALANCE + str(self.get_account_balance()) + Constants.TEXT_CURRENCY

    def get_account_balance(self):
        return self.__account_balance

    @staticmethod
    def set_account_balance(amount):
        Account.__account_balance = amount

    def increase_account_balance(self, amount):
        self.set_account_balance(self.get_account_balance() + amount)

    def decrease_account_balance(self, amount):
        self.set_account_balance(self.get_account_balance() - amount)

    # ---------------------------------------------------------------------------- #

    def get_value_of_shares_held_text(self):
        return Constants.TEXT_VALUE_OF_SHARES_HELD + str(self.get_value_of_shares_held()) + Constants.TEXT_CURRENCY

    def get_value_of_shares_held(self):
        return self.__value_of_shares_held

    @staticmethod
    def set_value_of_shares_held(amount):
        Account.__value_of_shares_held = amount

    def increase_value_of_shares_held(self, amount):
        self.set_value_of_shares_held(self.get_value_of_shares_held() + amount)

    def decrease_value_of_shares_held(self, amount):
        self.set_value_of_shares_held(self.get_value_of_shares_held() - amount)

    # ---------------------------------------------------------------------------- #

    def get_total_account_value_text(self):
        return Constants.TEXT_TOTAL_ACCOUNT_VALUE + str(self.get_total_account_value()) + Constants.TEXT_CURRENCY

    def get_total_account_value(self):
        return self.get_account_balance() + self.get_value_of_shares_held()

    @property
    def bought_companies_listbox_indexes(self):
        return self._bought_companies_listbox_indexes


class PlatformAccount:
    _platform_balance = 0  # wartość pobranych prowizji przez platformę

    def get_platform_balance(self):
        return self._platform_balance

    @staticmethod
    def set_platform_balance(amount):
        PlatformAccount._platform_balance = amount

    def increase_platform_balance(self, amount):
        return self.set_platform_balance(self.get_platform_balance() + amount)


class NewOrder(PlatformAccount, Account, Auxiliary):
    """Klasa obsługuje zlecenia zakupu/sprzedaży akcji"""

    def select_company(self, order_type, company_index, nr_of_shares):
        """Metoda obsługuje wybór firmy z listy dostępnych do zakupu akcji. Dzięki indeksowi na liście możemy powiązać daną pozycję z odpowiadającą jej klasą firmy."""

        company = DataProvider.get_company(company_index)

        # weryfikacja danych wprowadzonych przez użytkownika
        verified = VerifyUserInput.verify_user_input(nr_of_shares)

        if not verified:
            return

        nr_of_shares = int(nr_of_shares)
        share_price = company.get_price()

        # obliczenie wartości potencjalnej transakcji
        transaction_value = round(nr_of_shares * share_price, 2)

        if order_type == Constants.BUY_ORDER:
            successful_transaction = self.handle_stock_buy_order(company, transaction_value, nr_of_shares)
        elif order_type == Constants.SELL_ORDER:
            successful_transaction = self.handle_stock_sell_order(company, transaction_value, nr_of_shares)
        else:
            successful_transaction = False

        return successful_transaction

    def handle_stock_buy_order(self, company, transaction_value, nr_of_shares_to_buy):
        """Obsługa zlecenia zakupu akcji"""

        company_name = company.get_name()
        company_symbol = company.get_symbol()

        try:
            commission = self.validate_transaction_value(transaction_value)
        except NotEnoughFundsException:
            successful_transaction = False
            return successful_transaction

        # prośba o potwierdzenie chęci zakupu + podanie informacji o transakcji
        confirmation = messagebox.askokcancel(Constants.MESSAGE_CONFIRM_BUY_SHARES,
                                           'Czy na pewno chcesz zakupić {} akcji firmy {} za kwotę {} zł?'
                                              .format(nr_of_shares_to_buy, company_name, transaction_value + commission))

        if confirmation:
            self.decrease_account_balance(transaction_value + commission)
            self.increase_platform_balance(commission)
            self.increase_value_of_shares_held(transaction_value)

            # aktualizacja liczby posiadanych akcji danej firmy
            self._owned_shares_tracker[company_symbol] += nr_of_shares_to_buy

            messagebox.showinfo('Sukces', 'Pomyślnie dokonano zakupu {} akcji firmy {}'
                                .format(nr_of_shares_to_buy, company_name))

            successful_transaction = True
        else:
            successful_transaction = False

        return successful_transaction

    def validate_transaction_value(self, transaction_value):
        commission = round(Constants.BUYING_SHARES_COMMISSION * transaction_value, 2)
        if commission < 5.0:
            commission = 5.0

        total_transaction_value = round(transaction_value + commission, 2)
        if total_transaction_value > self.get_account_balance():
            # użytkownik nie posiada wystarczającej ilości środków na koncie do dokonania zakupu akcji
            raise NotEnoughFundsException(total_transaction_value)

        return commission

    def handle_stock_sell_order(self, company, transaction_value, nr_of_shares_to_sell):
        """Obsługa zlecenia sprzedaży akcji"""

        company_name = company.get_name()
        company_symbol = company.get_symbol()

        try:
            self.check_if_user_has_enough_shares(company_symbol, nr_of_shares_to_sell)
        except NotEnoughSharesException:
            return

        # prośba o potwierdzenie chęci sprzedaży + podanie informacji o transakcji
        confirmation = messagebox.askokcancel(Constants.MESSAGE_CONFIRM_SELL_SHARES,
                                           'Czy na pewno chcesz zakupić {} akcji firmy {} za kwotę {} zł?'
                                              .format(nr_of_shares_to_sell, company_name, transaction_value))

        if confirmation:
            self.increase_account_balance(transaction_value)
            self.decrease_value_of_shares_held(transaction_value)

            # aktualizacja liczby posiadanych akcji danej firmy
            self._owned_shares_tracker[company_symbol] -= nr_of_shares_to_sell

            messagebox.showinfo('Sukces', 'Pomyślnie dokonano sprzedaży {} akcji firmy {}'
                                .format(nr_of_shares_to_sell, company_name))

            successful_transaction = True
        else:
            successful_transaction = False

        return successful_transaction

    def check_if_user_has_enough_shares(self, company_symbol, stock_amount):
        if self._owned_shares_tracker[company_symbol] < stock_amount:
            # użytkownik nie posiada wystarczającej ilości akcji wybranej firmy
            raise NotEnoughSharesException


class Transfer(PlatformAccount, Account, Auxiliary):
    """Obsługa transakcji wpłaty i wypłaty środków oraz aktualizacja stanu środków na kocie."""

    def __init__(self):
        super().__init__()
        self.paid_commission_amount = 0
        self.withdrawal_amount_given_to_user = 0

    def handle_deposit(self, amount):
        """Metoda obsługuje wpłatę środków na konto"""

        verified_input = VerifyUserInput.verify_user_input(str(amount))
        if not verified_input:
            # użytkownik nie podał poprawnej kwoty
            return
        else:
            # kwota jest poprawna, ucinamy nadmiarową kwotę do dwóch miejsc po przecinku
            deposit_amount = math.floor(float(amount) * 100.0) / 100.0

        try:
            correct_value = self.verify_deposit_amount(deposit_amount)
        except MinimalDepositException:
            correct_value = False

        if not correct_value:
            # podana kwota nie spełnia warunków depozytu
            return

        confirmation = messagebox.askokcancel("Potwierdź wpłatę",
                                          'Czy na pewno chcesz wpłacić {} zł?'.format(deposit_amount))
        if confirmation:
            # użytkownik potwierdził chęć wpłaty na konto
            self.increase_account_balance(deposit_amount)

            messagebox.showinfo('Sukces', 'Pomyślnie dokonano wpłaty {} zł'.format(deposit_amount))

    @staticmethod
    def verify_deposit_amount(deposit_amount):
        """Metoda weryfikuję poprawność kwoty wprowadzonej przez użytkownika"""

        if deposit_amount < Constants.MINIMAL_DEPOSIT_AMOUNT:
            raise MinimalDepositException(deposit_amount)
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
                withdrawal_amount = math.floor(float(amount) * 100.0) / 100.0

        elif withdrawal_option == Constants.WITHDRAWAL_ALL:
            # użytkownik wybrał wypłatę wszystkich wolnych środków z konta
            withdrawal_amount = self.get_account_balance()
            if withdrawal_amount == 0:
                # stan środków na koncie wynosi już 0zł
                return
        else:
            return

        try:
            will_pay_commission = self.verify_withdrawal_amount(withdrawal_amount)
        except (MinimalWithdrawalException, NegativeBalanceException):
            return

        if will_pay_commission:
            # użytkownik płaci prowizję
            self.paid_commission_amount = Constants.WITHDRAWAL_COMMISSION_AMOUNT

            # pomniejszenie kwoty, którą otrzyma użytkownik o wysokość prowizji
            self.withdrawal_amount_given_to_user = withdrawal_amount - self.paid_commission_amount

        else:
            # użytkownik nie płaci prowizji
            self.withdrawal_amount_given_to_user = withdrawal_amount
            self.paid_commission_amount = 0

        confirmation = messagebox.askokcancel("Potwierdź wypłatę",
                                          'Czy na pewno chcesz wypłacić {} zł?\n'
                                          'Prowizja wyniesie: {} zł.'.format(
                                              self.withdrawal_amount_given_to_user + self.paid_commission_amount,
                                              self.paid_commission_amount))
        if confirmation:  # użytkownik potwierdził chęć wypłaty z konta

            # przekazanie prowizji na konto platformy
            self.decrease_account_balance(self.paid_commission_amount)
            self.increase_platform_balance(self.paid_commission_amount)

            # wypłata użytkownikowi kwoty pomniejszonej o wysokość prowizji
            self.decrease_account_balance(self.withdrawal_amount_given_to_user)

            messagebox.showinfo('Sukces', 'Pomyślnie dokonano wypłaty {} zł.\n'
                                          'Prowizja wyniosła {} zł.'.format(self.withdrawal_amount_given_to_user,
                                                                            self.paid_commission_amount))

    def verify_withdrawal_amount(self, withdrawal_amount):
        """Weryfikacja poprawności danych wprowadzonych przez użytkownika podczas podawania kwoty
        oraz sprawdzenie czy użytkownik zapłaci prowizję"""

        current_account_balance = self.get_account_balance()

        if withdrawal_amount < Constants.MINIMAL_WITHDRAWAL_AMOUNT:
            raise MinimalWithdrawalException(withdrawal_amount)

        elif current_account_balance - withdrawal_amount < 0.0:
            # użytkownik nie ma wystarczającego stanu konta, żeby wypłacić podaną ilość środków
            raise NegativeBalanceException

        elif withdrawal_amount > Constants.WITHDRAWAL_COMMISSION_THRESHOLD:
            # użytkownik nie płaci prowizji za wypłatę
            will_pay_commission = False

        else:
            # użytkownik powinien zapłacić prowizję
            will_pay_commission = True

        return will_pay_commission
