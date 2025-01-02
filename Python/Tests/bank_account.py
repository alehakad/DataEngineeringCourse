import unittest


class BankAccount:
    def __init__(self, id):
        self.id = id
        self.balance = 0

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def deposit(self, amount):
        self.balance += amount
        return True


if __name__ == "__main__":
    # unittests for BankAccount
    class TestBankAccount(unittest.TestCase):
        def test_bank_account_balance(self):
            account = BankAccount(1)
            self.assertEqual(account.balance, 0)
            self.assertTrue(account.deposit(100))
            self.assertEqual(account.balance, 100)

        def test_bank_account_withdraw(self):
            account = BankAccount(2)
            self.assertTrue(account.deposit(100))
            self.assertTrue(account.withdraw(50))
            self.assertEqual(account.balance, 50)
            self.assertFalse(account.withdraw(51))

    unittest.main(argv=[""], exit=False)