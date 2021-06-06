import unittest

from src.Utilities.constants import Constants
from src.platform import Account, NegativeBalanceException, PlatformAccount, Transfer


class TestWithdrawal(unittest.TestCase):
    """Testy dotyczące wypłat środków pieniężnych z konta użytkownika"""

    def test_withdrawing_more_than_account_balance_should_raise_exception(self):
        """Test sprawdza próbę wypłaty z konta kwoty większej niż stan wolnych środków.
        Oczekiwana informacja o błędzie"""

        # given
        account = Account()
        transfer = Transfer()
        account.set_account_balance(100)
        withdrawal_amount = 500

        # then
        with self.assertRaises(NegativeBalanceException):
            transfer.verify_withdrawal_amount(withdrawal_amount)

    def test_withdrawing_amount_within_commission_threshold_should_charge_commission(self):
        """Test sprawdza próbę wypłaty z konta kwoty zawierającej się w zakresie pobierania prowizji.
        Oczekiwane zmniejszenie wartości wolnych środków na koncie o wartość podaną przez użytkownika, pobranie prowizji i wypłacenie pozostałych środków użytkownikowi"""

        # given
        account = Account()
        transfer = Transfer()
        platform_account = PlatformAccount()

        account_balance_before_withdrawal = 500
        account.set_account_balance(account_balance_before_withdrawal)
        withdrawal_amount = Constants.WITHDRAWAL_COMMISSION_THRESHOLD - 100

        # when
        transfer.handle_withdrawal(withdrawal_amount, Constants.WITHDRAWAL)

        # then
        expected_account_balance_after_withdrawal = account_balance_before_withdrawal - withdrawal_amount
        self.assertEqual(expected_account_balance_after_withdrawal, account.account_balance)
        self.assertEqual(Constants.WITHDRAWAL_COMMISSION_AMOUNT, platform_account.get_platform_balance())
        self.assertEqual(withdrawal_amount - Constants.WITHDRAWAL_COMMISSION_AMOUNT, transfer.withdrawal_amount)


if __name__ == '__main__':
    unittest.main()
