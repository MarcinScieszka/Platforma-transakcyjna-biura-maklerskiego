import unittest

from src.Repository.data_provider import DataProvider
from src.trading_platform import Account, NewOrder, NotEnoughSharesException


class TestSellShares(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.account = Account()
        cls.new_order = NewOrder()
        cls.company = DataProvider.get_company(5)
        cls.company_symbol = cls.company.get_symbol()
        cls.company_price = cls.company.get_price()

    def test_sell_more_shares_than_owned_should_raise_exception(self):
        """Test sprawdza próbę sprzedaży większej liczby akcji, niż aktualnie posiadana przez użytkownika.
        Oczekiwane rzucenie wyjątku."""

        # given
        account_balance_before_transaction = 5000
        self.account.set_account_balance(account_balance_before_transaction)
        nr_of_shares_to_buy = 10

        # then
        with self.assertRaises(NotEnoughSharesException):
            self.new_order.check_if_user_has_enough_shares(self.company_symbol, nr_of_shares_to_buy)

    def test_sell_more_shares_than_owned_should_not_change_account_properties(self):
        """Test sprawdza próbę sprzedaży większej liczby akcji, niż aktualnie posiadana przez użytkownika.
        Oczekiwania: stan konta oraz liczba posiadanych akcji powinna pozostać bez zmian"""

        # given
        nr_of_owned_shares_before_transaction = 8
        self.account.set_nr_of_owned_shares(self.company_symbol, nr_of_owned_shares_before_transaction)  # użytkownik posiada 8 akcji danej firmy
        account_balance_before_transaction = 5000
        self.account.set_account_balance(account_balance_before_transaction)
        nr_of_shares_to_sell = 10
        transaction_value = nr_of_shares_to_sell * self.company_price

        # when
        self.new_order.handle_stock_sell_order(self.company, transaction_value, nr_of_shares_to_sell)

        # then
        self.assertEqual(account_balance_before_transaction, self.account.get_account_balance())
        self.assertEqual(nr_of_owned_shares_before_transaction, self.account.get_nr_of_shares_owned(self.company_symbol))

    def test_sell_shares_should_decrease_nr_of_shares_owned_and_increase_account_balance(self):
        """Test sprawdza poprawność sprzedaży uprzednio zakupionych akcji.
        Oczekiwania: odpowiednie zmniejszenie liczby posiadanych akcji, zwiększenie wartości wolnych środków,
        zmniejszenie wartości posiadanych akcji,
        wartość konta nie powinna się zmienić"""

        # given
        account_balance_before_transaction = 0
        self.account.set_account_balance(account_balance_before_transaction)
        value_of_owned_shares_before_transaction = 5000.0
        self.account.set_value_of_shares_held(value_of_owned_shares_before_transaction)
        nr_of_company_shares_owned_before_transaction = 8
        self.account.set_nr_of_owned_shares(self.company_symbol, nr_of_company_shares_owned_before_transaction)
        nr_of_shares_to_sell = 5
        transaction_value = nr_of_shares_to_sell * self.company_price
        expected_nr_of_shares_owned_after_transaction = nr_of_company_shares_owned_before_transaction - nr_of_shares_to_sell
        expected_account_balance = account_balance_before_transaction + transaction_value
        expected_value_of_owned_shares = value_of_owned_shares_before_transaction - transaction_value
        expected_total_account_value = self.account.get_total_account_value_text()

        # when
        self.new_order.handle_stock_sell_order(self.company, transaction_value, nr_of_shares_to_sell)

        # then
        self.assertEqual(expected_nr_of_shares_owned_after_transaction, self.account._owned_shares_tracker[self.company_symbol])
        self.assertEqual(expected_account_balance, self.account.get_account_balance())
        self.assertEqual(expected_value_of_owned_shares, self.account.get_value_of_shares_held())
        self.assertEqual(expected_total_account_value, self.account.get_total_account_value_text())


if __name__ == '__main__':
    unittest.main()
