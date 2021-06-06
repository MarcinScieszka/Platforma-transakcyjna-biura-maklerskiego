import unittest

from src.platform import Account, Transfer


class TestDeposit(unittest.TestCase):
    def test_depositing_500_should_increase_account_balance_to_500(self):
        account = Account()
        transfer = Transfer()

        deposit_value = 500

        transfer.handle_deposit(deposit_value)

        self.assertEqual(500, account.account_balance)


if __name__ == '__main__':
    unittest.main()
