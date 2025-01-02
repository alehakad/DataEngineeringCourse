import pytest
from bank_account import BankAccount

#tests with pytest
import pytest

def test_bank_account_balance():
    account = BankAccount(1)
    assert account.balance == 0
    assert account.deposit(100)
    assert account.balance == 100

def test_bank_account_withdraw():
    account = BankAccount(2)
    assert account.deposit(100)
    assert account.withdraw(50)
    assert account.balance == 50
    assert not account.withdraw(51)
