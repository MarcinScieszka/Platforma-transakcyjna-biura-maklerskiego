import unittest

from src.Repository.data_provider import DataProvider
from src.platform import NotEnoughFundsException, NewOrder, Account, PlatformAccount


class TestPurchaseShares(unittest.TestCase):
    """Testy dotyczą kupna akcji spośród dostępnych firm"""

    def test_purchasing_shares_costing_more_than_account_balance_should_raise_exception(self):
        """Test sprawdza próbę zakupu akcji za kwotę przekraczającą stan wolnych środków na koncie użytkownika.
        Oczekiwana informacja o błędzie"""

        # given
        account = Account()
        account.set_account_balance(100)
        new_order = NewOrder()

        # then
        with self.assertRaises(NotEnoughFundsException):
            new_order.validate_transaction_value(2000)

    def test_purchasing_shares_should_charge_commission_and_add_shares_and_reduce_balance(self):
        """Test sprawdza efekt zakupu akcji danej firmy.
        Oczekiwane:
        zwiększenie ilości posiadanych akcji danej firmy
        prawidłowe obliczenie oraz pobranie prowizji
        zmniejszenie wartości wolnych środków o wartość akcji powiększoną o kwotę prowizji"""

        # given
        DataProvider.instantiate_companies()
        company = DataProvider.get_company(5)
        account = Account()
        platform_account = PlatformAccount()
        account_balance_before_transaction = 5000
        account.set_account_balance(account_balance_before_transaction)
        new_order = NewOrder()
        stock_amount = 10
        transaction_value = company.get_price() * stock_amount
        expected_commission = 5.0

        # when
        new_order.handle_stock_buy_order(company, transaction_value, stock_amount)

        # then
        self.assertEqual(stock_amount, account.purchased_companies[company.get_symbol()])
        self.assertEqual(expected_commission, platform_account.platform_balance)
        self.assertEqual(account_balance_before_transaction - (transaction_value + expected_commission), account.get_account_balance())


if __name__ == '__main__':
    unittest.main()
