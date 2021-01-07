import random
import sqlite3
import sys


def generate_check_sum(acc_number: int) -> int:
    """
    Generates check sum using the incomplete account number using Luhn's algorithm

    Args:
        acc_number (int): account number without check sum

    Returns:
        Check sum of the account number

    """
    num_sum = 0
    for index, value in enumerate(str(acc_number)):
        value = int(value)
        if index % 2 == 0:
            value = value * 2
        if value > 9:
            value = value - 9
        num_sum += value

    return 0 if num_sum % 10 == 0 else 10 - num_sum % 10


def generate_new_card():
    """
    Generates new card and adds new card's info to the database.

    Returns:
        None
    """
    print("Generating new card with pin for you...")

    _BANK_IDENTIFIER = "400000"

    while True:
        account_identifier = str(random.randint(1, 999999999))
        account_identifier = account_identifier.zfill(9)
        check_sum = str(generate_check_sum(int(_BANK_IDENTIFIER + account_identifier)))
        new_card_number = _BANK_IDENTIFIER + account_identifier + check_sum
        # check if the card number is already present
        needs_new_card = True if len(db_fetch(f'SELECT number FROM card WHERE number = {new_card_number}')) > 0 else False
        if not needs_new_card:
            break

    new_pin_number = str(random.randint(0, 9999)).zfill(4)
    # Add newly created account
    add_account(new_card_number, new_pin_number, 0)

    print("\nYour card has been created")
    print("Your card number:")
    print(new_card_number)
    print("Your card PIN:")
    print(new_pin_number)
    print("\n")


def log_in():
    """
    Asks for login info and logs user into the account

    Returns:
        None
    """

    account_number = input("Enter your card number:\n")
    account_pin = input("Enter your PIN:\n")
    can_login = True if len(db_fetch(f'SELECT id FROM card WHERE number = {account_number} AND pin = {account_pin}')) == 1 else False

    if not can_login:
        print("Wrong card number or PIN!")
        return

    def get_balance(do_print=True):
        balance = db_fetch(f'SELECT balance FROM card WHERE number = {account_number} AND pin = {account_pin}')
        if do_print:
            print(f"Balance: {balance[0][0]}\n")
        return balance[0][0]

    def add_income():
        print("Enter income:")
        income = int(input())
        new_income = income + get_balance(do_print=False)
        db_modify(f'UPDATE card SET balance = {new_income} WHERE number = {account_number}')
        print("Income was added!")

    def transfer():
        print("Enter card number: ")
        transfer_account = input()
        # Check if same as current card number
        if transfer_account == account_number:
            print("You can't transfer money to the same account!")
            return
        # Check for card number validity
        if generate_check_sum(int(str(transfer_account)[:-1])) != int(str(transfer_account)[-1]):
            print("Probably you made a mistake in the card number. Please try again!\n")
            return
        # Check if card exists
        transfer_account_info = db_fetch(f'SELECT id, balance FROM card WHERE number = {transfer_account}')
        if len(transfer_account_info) == 0:
            print("Such a card does not exist.")
            return

        print("Enter how much money you want to transfer: ")
        transfer_amount = int(input())
        # Check if you have enough balance
        my_balance = get_balance(do_print=False)
        if my_balance < transfer_amount:
            print("Not enough money!")
            return

        # Deduct transfer amount from your balance
        db_modify(f'UPDATE card SET balance = {my_balance - transfer_amount} WHERE number = {account_number}')
        # Add transfer amount to transfer account's balance
        transfer_account_balance = transfer_account_info[0][1]
        db_modify(f'UPDATE card SET balance = {transfer_account_balance + transfer_amount} WHERE number = {transfer_account}')
        print("Success!")

    def close_account():
        modify_status = db_modify(f'DELETE FROM card WHERE number = {account_number}')
        if modify_status == 0:
            print("The account has been closed!")
        else:
            print("The account cannot be closed!")

    account_func_dict = {
        1: get_balance,
        2: add_income,
        3: transfer,
        4: close_account,
        0: exit_program
    }

    print("You have successfully logged in\n")
    while True:
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        option = int(input())
        if option == 5:
            print("You have successfully logged out!")
            break
        try:
            account_func_dict[option]()
            if option == 4:
                break
        except KeyError:
            print("Wrong option selected. Please select correct option.")


def add_account(acc_number: str, acc_pin: str, acc_balance: int):
    """
    Adds account info to database.

    Args:
        acc_number (str): Account number
        acc_pin (str): Account pin
        acc_balance (int): Account balance

    Returns:
        int: 0 for success, 1 otherwise

    """
    add_status = db_modify(f'INSERT INTO card (number, pin, balance) VALUES ({acc_number}, {acc_pin}, {acc_balance})')
    return add_status


def read_table():
    table_name = input("Enter the table name: ")
    table_data = db_fetch(f'SELECT * FROM {table_name}')
    print(table_data)
    return table_data


def create_table():
    # create table
    db_modify('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT UNIQUE NOT NULL, pin TEXT NOT NULL, balance INTEGER DEFAULT 0)')


def db_fetch(query: str):
    try:
        conn = sqlite3.connect("card.s3db")
    except Exception as e:
        print(e)
        return

    cur = conn.cursor()
    try:
        cur.execute(query)
        return cur.fetchall()
    except sqlite3.OperationalError:
        return []


def db_modify(query: str):
    try:
        conn = sqlite3.connect("card.s3db")
    except Exception as e:
        print(e)
        return 1

    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    return 0


def exit_program():
    print("Bye!")
    sys.exit(0)


def main():
    random.seed(2021)
    create_table()
    main_func_dict = {
        0: exit_program,
        1: generate_new_card,
        2: log_in,
        666: read_table
    }
    while True:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        option = int(input())
        try:
            main_func_dict[option]()
        except KeyError:
            print("Wrong option selected. Please select correct option.")


if __name__ == '__main__':
    main()
