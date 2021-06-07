import unittest

from src.Utilities.constants import Constants
from src.platform import Account, Transfer, MinimalDepositException


class TestDeposit(unittest.TestCase):
    """Testy dotyczące wpłat środków pieniężnych na konto użytkownika"""

    @classmethod
    def setUpClass(cls):
        cls.transfer = Transfer()

    def test_depositing_amount_above_commission_threshold_should_increase_account_balance_by_amount(self):
        """Test sprawdza próbę wpłaty kwoty powyżej progu minimalnego depozytu.
        Oczekiwane zwiększenie wartości wolnych środków o kwotę depozytu"""

        # given
        account = Account()
        account.set_account_balance(0)
        deposit_amount = Constants.MINIMAL_DEPOSIT_AMOUNT + 400

        # when
        self.transfer.handle_deposit(deposit_amount)

        # then
        self.assertEqual(deposit_amount, account.get_account_balance())

    def test_depositing_amount_below_minimal_allowed_should_raise_exception(self):
        """Test sprawdza próbę wpłaty na konto kwoty poniżej minimalnego progu wpłaty.
        Oczekiwane rzucenie wyjątku"""

        # given
        deposit_amount = Constants.MINIMAL_DEPOSIT_AMOUNT - 1

        # then
        with self.assertRaises(MinimalDepositException):
            self.transfer.verify_deposit_amount(deposit_amount)


if __name__ == '__main__':
    unittest.main()
