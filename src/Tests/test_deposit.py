import unittest

from src.platform import Account, Transfer, DepositTooSmallException


class TestDeposit(unittest.TestCase):
    def test_depositing_500_should_increase_account_balance_to_500(self):
        # given
        account = Account()
        transfer = Transfer()
        deposit_value = 500

        # when
        transfer.handle_deposit(deposit_value)

        # then
        self.assertEqual(500, account.account_balance)

    def test_depositing_100_should_raise_exception(self):
        # given
        transfer = Transfer()
        deposit_value = 50

        # when
        transfer.handle_deposit(deposit_value)

        # then
        self.assertRaises(DepositTooSmallException)


if __name__ == '__main__':
    unittest.main()
