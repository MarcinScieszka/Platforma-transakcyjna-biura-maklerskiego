import unittest

from src.Utilities.constants import Constants
from src.platform import Account, Transfer, DepositTooSmallException, NegativeBalanceException


class TestDeposit(unittest.TestCase):
    def test_depositing_500_should_increase_account_balance_to_500(self):
        """Test sprawdza próbę wpłaty 500zł na konto
        oczekiwane zwiększenie wartości wolnych środków o 500zł"""

        # given
        account = Account()
        transfer = Transfer()
        deposit_amount = 500

        # when
        transfer.handle_deposit(deposit_amount)

        # then
        self.assertEqual(500, account.account_balance)

    def test_depositing_100_should_raise_exception(self):
        """Test sprawdza próbę wpłaty na konto kwoty poniżej minimalnego progu wpłaty (100zł)
        oczekiwana informacja o błędzie"""

        # given
        transfer = Transfer()
        deposit_amount = 50

        # when
        transfer.handle_deposit(deposit_amount)

        # then
        self.assertRaises(DepositTooSmallException)

    def test_withdrawing_more_than_account_balance_should_raise_exception(self):
        """Test sprawdza próbę wypłaty z konta kwoty większej niż stan wolnych środków
        oczekiwana informacja o błędzie"""

        # given
        account = Account()
        transfer = Transfer()
        account.set_account_balance(100)
        withdrawal_amount = 500

        # when
        transfer.handle_withdrawal(withdrawal_amount, Constants.WITHDRAWAL)

        # then
        self.assertRaises(NegativeBalanceException)


if __name__ == '__main__':
    unittest.main()
