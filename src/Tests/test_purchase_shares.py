import unittest

from src.Repository.data_provider import DataProvider
from src.platform import NotEnoughFundsException, NewOrder, Account


class TestPurchaseShares(unittest.TestCase):
    """Testy dotyczą kupna akcji spośród dostępnych firm"""

    def test_purchasing_shares_costing_more_than_account_balance_should_raise_exception(self):
        """Test sprawdza próbę zakupu akcji za kwotę przekraczającą stan wolnych środków na koncie użytkownika.
        Oczekiwana informacja o błędzie"""

        # given
        DataProvider.instantiate_companies()
        company = DataProvider.get_company(1)
        account = Account()
        account.set_account_balance(100)
        new_order = NewOrder()

        # when
        new_order.handle_stock_buy_order(company, 500, 5)

        # then
        self.assertRaises(NotEnoughFundsException)


if __name__ == '__main__':
    unittest.main()
