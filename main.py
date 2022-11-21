from bank import ConsoleDesign
from bank import Account

if __name__ == "__main__":
    account_list = []
    account_list.append(Account(len(account_list)))
    account_list.append(Account(len(account_list)))

    for i in account_list:
        i.show()

    ConsoleDesign.head()
    print("Ending program...")
