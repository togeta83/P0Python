import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="############",
  database="BankDatabase"
)

myCursor = mydb.cursor()


def get_id(firstname, lastname, account):
    myCursor.execute(f"SELECT id from accounts WHERE firstName = '{firstname}' AND lastName = '{lastname}' "
                     f"AND type = '{account}'")
    return myCursor.fetchall()


def deuces(acct_id):
    del_sql = f"DELETE FROM accounts WHERE id = {acct_id}"
    myCursor.execute(del_sql)
    mydb.commit()
    print("Your account has been removed.")


def my_balance(acct_id):
    bal = f"SELECT balance FROM accounts WHERE id = {acct_id}"
    myCursor.execute(bal)
    check_balance = myCursor.fetchone()
    return check_balance[0]


def withdraw(acct_id):
    get_money = int(input("How much would you like to withdraw?: "))
    minus_sql = f"UPDATE accounts SET balance = {my_balance(acct_id)} - {get_money} WHERE id ={acct_id}"
    myCursor.execute(minus_sql)
    mydb.commit()
    print(f"You withdrew {get_money} dollars from your account.")
    print(f"And so you now have a balance of ${my_balance(acct_id)}.")


def deposit(acct_id):
    stack_money = int(input("How much would you like to deposit?: "))
    plus_sql = f"UPDATE accounts SET balance = {my_balance(acct_id)} + {stack_money} WHERE id ={acct_id}"
    myCursor.execute(plus_sql)
    mydb.commit()
    print(f"You deposited {stack_money} dollars into your account.")


def access_account():
    account_name = []
    access_id = []
    acct_type = 'z'
    # accounts = []
    account_type = ""
    transaction = 'z'
    while len(account_name) == 0:
        first_name = input("Please enter your first name: ")
        last_name = input("Please enter your last name: ")
        myCursor.execute(f"SELECT id from accounts WHERE firstName = '{first_name}' AND lastName = '{last_name}' ")
        account_name = myCursor.fetchall()
        if len(account_name) == 0:
            print(f"Sorry but there are no accounts with name: '{first_name} {last_name}'.")
            print("Please try again.")
    print(f"Welcome {first_name}!")
    while acct_type != 'c' or acct_type != 's':
        print("What type of account would you like to access, Checking or Savings?: ")
        acct_type = input("Please enter [C]- Checking or [S]- Savings: ")
        if acct_type == "c":
            account_type = "Checking"
            access_id = get_id(first_name, last_name, account_type)
            if len(access_id) == 0:
                acct_type = 'z'
                print(f"Sorry but there are no {account_type} accounts under the name: '{first_name} {last_name}'.")
                print("Please try again.")
                access_account()
            break
        elif acct_type == "s":
            account_type = "Savings"
            access_id = get_id(first_name, last_name, account_type)
            if len(access_id) == 0:
                acct_type = 'z'
                print(f"Sorry but there are no {account_type} accounts under the name: '{first_name} {last_name}'.")
                print("Please try again.")
                access_account()
            break
        else:
            acct_type = 'z'
            print(f"Invalid option. Please try again.")

    print(f"Okay, {account_type}. Got it.")

    access_id = get_id(first_name, last_name, account_type)[0]
    while transaction not in ['d', 'w', 'b', 'x']:
        transaction = input("What would like to do? [D]- Deposit [W]- Withdraw or "
                            "[B]- Check your balance [x]- Close your account: ").lower()

        if transaction.lower() == 'd':
            print(f"Okay, make a deposit.")
            deposit(access_id[0])
            break
        elif transaction.lower() == 'w':
            print(f"Okay, make a withdrawal.")
            withdraw(access_id[0])
            break
        elif transaction.lower() == 'b':
            print(f"Okay, checking your balance...")
            balance = my_balance(access_id[0])
            print(f"Your balance is ${balance}.")
            break
        elif transaction.lower() == 'x':
            print(f"You chose to close your account.")
            deuces(access_id[0])
            break
        else:
            transaction = 'z'
            print(f"Invalid option. Please try again.")


def open_account():
    account_type = ""
    acct_type = 'z'
    first_name = input("Please enter your first name: ")
    last_name = input("Please enter your last name: ")
    print(f"Thank you for that information, {first_name} {last_name}!")

    while acct_type != 'c' or acct_type != 's':
        print("What type of account would you like to open, Checking or Savings?: ")
        acct_type = input("Please enter [C] for Checking or [S] for Savings: ").lower()
        if acct_type == "c":
            account_type = "Checking"
            break
        elif acct_type == "s":
            account_type = "Savings"
            break
        else:
            acct_type = 'z'
            print(f"Invalid option. Please try again.")

    if account_type == "Checking" or account_type == "Savings":
        print(f"Okay, {account_type} account. Got it.")
        initial_deposit = input("How much would you like to open your account with?: ")

        new_account = {"First Name": first_name, "Last Name": last_name,
                       "Account Type": account_type, "Initial Deposit": initial_deposit}

        new_sql = "INSERT INTO accounts (firstName, lastName, type, balance) VALUES (%s, %s, %s, %s)"
        new_val = (first_name, last_name, account_type, initial_deposit)
        myCursor.execute(new_sql, new_val)
        mydb.commit()

        print(f"Okay {new_account['First Name']}, we're all set!")
        print(f"Your new {new_account['Account Type']} account has a starting balance of "
              f"${new_account['Initial Deposit']}.\n")
        print()


# ########## Main ##########
# myCursor.execute("CREATE DATABASE BankDatabase")
# acctSQL = "CREATE TABLE accounts (id INT AUTO_INCREMENT PRIMARY KEY, firstName VARCHAR(255),\
#                   lastName VARCHAR(255), type VARCHAR(255), Balance int)"
# myCursor.execute(acctSQL)
accounts_sql = "SELECT * FROM accounts"
myCursor.execute(accounts_sql)
all_accounts = myCursor.fetchall()
for acct in all_accounts:
    print(acct)
main_choices = {0: "exit", 1: "open and account", 2: "access an existing account"}
main_option = -1
while main_option != 0:
    print("Hello and Welcome to Eden Mutual!")
    print("How may we help you?")
    print("[1]-[Open an account] [2]-[Access an account] [0]-[Exit]")

    main_option = int(input())

    if main_option == 1:
        print(f"Alright let's {main_choices[1]}.")
        open_account()
    elif main_option == 2:
        print(f"You chose to {main_choices[2]}.")
        access_account()
    elif main_option == 0:
        print(f"You chose to {main_choices[0]}. Please enjoy your day!")
    else:
        print(f"Invalid option. Please try again.")
