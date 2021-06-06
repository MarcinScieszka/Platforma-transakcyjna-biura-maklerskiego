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
        account = Account()
        account.set_account_balance(100)
        new_order = NewOrder()

        # then
        with self.assertRaises(Exception):
            new_order.validate_transaction_value(2000)

    def test_purchasing_shares_should_charge_commission_add_shares_reduce_balance(self):
        """Test sprawdza zakup akcji danej firmy.
        Oczekiwane:
        zwiększenie ilości posiadanych akcji danej firmy
        prawidłowe obliczenie oraz pobranie prowizji
        zmniejszenie wartości wolnych środków o wartość akcji powiększoną o kwotę prowizji"""


if __name__ == '__main__':
    unittest.main()
