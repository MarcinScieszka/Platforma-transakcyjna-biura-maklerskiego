import unittest

from src.Repository.data_provider import DataProvider
from src.platform import NotEnoughFundsException, NewOrder, Account, PlatformAccount


class TestBuyShares(unittest.TestCase):
    """Testy dotyczą kupna akcji spośród dostępnych firm"""

    @classmethod
    def setUpClass(cls):
        cls.account = Account()
        cls.new_order = NewOrder()

    def test_buying_shares_costing_more_than_account_balance_should_raise_exception(self):
        """Test sprawdza próbę zakupu akcji za kwotę przekraczającą stan wolnych środków na koncie użytkownika.
        Oczekiwane rzucenie wyjątku"""

        # given
        account_balance_before_transaction = 100
        self.account.set_account_balance(account_balance_before_transaction)
        transaction_value = 2000

        # then
        with self.assertRaises(NotEnoughFundsException):
            self.new_order.validate_transaction_value(transaction_value)

    def test_buying_shares_should_charge_commission_and_add_shares_and_reduce_balance(self):
        """Test sprawdza efekt zakupu akcji danej firmy.
        Oczekiwane:
        zwiększenie ilości posiadanych akcji danej firmy
        prawidłowe obliczenie oraz pobranie prowizji
        zmniejszenie wartości wolnych środków o wartość akcji powiększoną o kwotę prowizji"""

        # given
        DataProvider.instantiate_companies()
        company = DataProvider.get_company(5)
        platform_account = PlatformAccount()
        self.account_balance_before_transaction = 5000
        self.account.set_account_balance(self.account_balance_before_transaction)
        nr_of_shares_willing_to_buy = 10
        transaction_value = company.get_price() * nr_of_shares_willing_to_buy
        expected_commission = 5.0

        # when
        self.new_order.handle_stock_buy_order(company, transaction_value, nr_of_shares_willing_to_buy)

        # then
        self.assertEqual(nr_of_shares_willing_to_buy, self.account.bought_companies[company.get_symbol()])
        self.assertEqual(expected_commission, platform_account.platform_balance)
        self.assertEqual(self.account_balance_before_transaction - (transaction_value + expected_commission), self.account.get_account_balance())


if __name__ == '__main__':
    unittest.main()
