import pytest 

from app.calculations import add, multiply, BankAccount


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)  # starting balance of 100


def test_add():
    print("Testing add function")
    assert add(2, 4) == 6

def test_multiply():
    print("testing multiply fun")
    assert multiply(4, 3) == 12

def test_bank_amount(zero_bank_account):
    # bank_account = BankAccount(50)
    assert zero_bank_account.balance == 0

def test_interest(bank_account): 
    # bank_account = BankAccount(50)
    bank_account.collect_interest()
    test = 50*1.1
    # compare the account balance (float) to the expected value
    assert bank_account.balance == test

def test_bank_transaction(zero_bank_account):
    zero_bank_account.deposit(200)
    zero_bank_account.withdraw(200)
    assert zero_bank_account.balance == 00
