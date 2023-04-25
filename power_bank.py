import hashlib
import pandas as pd
from datetime import datetime

pd.options.mode.chained_assignment = None  # default='warn'

def hashHead():
    '''
    Add an empty line, a line of 80 hashes and another empty line.
    This is a function designed to separate two operations from each other.
    '''
    print('')
    print('#' * 80)
    print('')

def existsCheck(account):
    return account in df.CUSTOMER_ID.values

def pwCheck(account):
    '''
    Check password to enter account information.
    Input gets hashed and compared with database value.
    Input:  account number & password
    Output: boolean
    '''
    password = hashlib.sha3_256(input("Please enter password: ").encode()).hexdigest()
    if existsCheck(account): return password == df.loc[df["CUSTOMER_ID"] == account].PASSWORD.item()
    return False

def accCreate():
    hashHead()
    '''
    Create an account with automatic customer ID and manually entered name and password
    Initial balance and overdraft are set to 0 by default.
    '''
    customer_id = df.CUSTOMER_ID.max() + 1
    name = input("Enter your name: ")
    password = hashlib.sha3_256(input("Enter your password: ").encode()).hexdigest()
    new_line = [customer_id, name, 0, 0, password, 'y']
    df.loc[len(df)] = new_line
    df.index = [''] * len(df)
    dest = str(customer_id) + ".csv"
    with open(dest, 'a') as f:
        f.write("TIME;TYPE;INITIAL_BALANCE;DIFFERENCE;FINAL_BALANCE\n")
        f.write(str(datetime.now()) + ";CREATE;0;0;0\n")
        f.close()
        

def accDeposit():
    hashHead()
    '''
    Deposit money in account.
    Input:  account number, password & amount
    Output: New account balance & Update of database
    '''
    account = int(input("Enter Account ID: "))
    if pwCheck(account):
        print("Your balance is {}.".format(round(df[df.CUSTOMER_ID == account].BALANCE.item(), 2)))
        initial_balance = round(df[df.CUSTOMER_ID == account].BALANCE.item(), 2)
        print("You want to deposit money.")
        amount = round(float(input("Enter amount to deposit: ")), 2)
        if amount > 0:
            final_balance = initial_balance + amount
            df.loc[df["CUSTOMER_ID"] == account, "BALANCE"] += amount
            print("Deposited {}.".format(amount))
            print("New balance is {}.".format(round(df[df.CUSTOMER_ID == account].BALANCE.item(), 2)))
            dest = str(account) + ".csv"
            with open(dest, 'a') as f:
                f.write(str(datetime.now()) + 
                        ";DEPOSIT;" + 
                        str(initial_balance) + ";" + 
                        str(amount) + ";" + 
                        str(final_balance) + "\n")
                f.close()
        else: print("Amount has to be larger than 0!")
    else: print("Wrong password! Access denied!")
        
def accWithdraw():
    hashHead()
    '''
    Withdraw money from account.
    Input:  account number, password & amount
    Output: New account balance & Update of database
    '''
    account = int(input("Enter Account ID: "))
    if pwCheck(account):
        print("Your balance is {}.".format(round(df[df.CUSTOMER_ID == account].BALANCE.item(), 2)))
        initial_balance = round(df[df.CUSTOMER_ID == account].BALANCE.item(), 2)
        print("You want to withdraw money.")
        amount = round(float(input("Enter amount to withdraw: ")), 2)
        if amount > 0:
            if df[df.CUSTOMER_ID == account].BALANCE.item() - amount - df[df.CUSTOMER_ID == account].OVERDRAFT.item() >= 0:
                df.loc[df["CUSTOMER_ID"] == account, "BALANCE"] -= amount
                final_balance = initial_balance - amount
                print("Withdrawn {}.".format(amount))
                print("New balance is {}.".format(round(df[df.CUSTOMER_ID == account].BALANCE.item(), 2)))
                dest = str(account) + ".csv"
                with open(dest, 'a') as f:
                    f.write(str(datetime.now()) + 
                            ";WITHDRAW;" + 
                            str(initial_balance) + ";" + 
                            str(-amount) + ";" + 
                            str(final_balance) + "\n")
                    f.close()
            else: print("Your balance is too low!")
        else: print("Amount has to be larger than 0!")
    else: print("Account number and/or password are not correct!")

def accShow():
    hashHead()
    '''
    Show account details
    Input:  account number & password
    Output: account data
    '''
    account = int(input("Enter Account ID: "))
    if pwCheck(account): print(df[df.CUSTOMER_ID == account][["CUSTOMER_ID", "NAME", "BALANCE", "OVERDRAFT"]])
    else: print("Account number and/or password are not correct!")

        
def accTransfer():
    pass
    '''
    Transfer money from own account to another
    Input:  account number, password, receivers account number & amount
    Output: New own balance & updates of account database, sender account log & receiver account log
    '''
    hashHead()
    s_account = int(input("Enter your Account ID: "))
    if pwCheck(s_account):
        print("Your balance is {}.".format(round(df[df.CUSTOMER_ID == s_account].BALANCE.item(), 2)))
        s_initial_balance = round(df[df.CUSTOMER_ID == s_account].BALANCE.item(), 2)
        print("You want to transfer money.")
        r_account = int(input("Enter receivers Account ID: "))
        if existsCheck(r_account):
            amount = round(float(input("Enter amount to transfer: ")), 2)
            if amount > 0:
                if df[df.CUSTOMER_ID == s_account].BALANCE.item() - amount - df[df.CUSTOMER_ID == s_account].OVERDRAFT.item() >= 0:
                    print("You want to transfer {} to Account {}.".format(amount, r_account))
                    confirmation = input("Is this correct (y/n)? ")
                    if confirmation.lower() != 'y':
                        print("Transfer was not confirmed!")
                    else:
                        s_final_balance = s_initial_balance - amount
                        r_initial_balance = round(df[df.CUSTOMER_ID == r_account].BALANCE.item(), 2)
                        r_final_balance = r_initial_balance + amount
                        df.loc[df["CUSTOMER_ID"] == s_account, "BALANCE"] -= amount
                        s_dest = str(s_account) + ".csv"
                        with open(s_dest, 'a') as sf:
                            sf.write(str(datetime.now()) + 
                                     ";TRANSFER TO {};".format(str(r_account)) + 
                                     str(s_initial_balance) + ";" + 
                                     str(-amount) + ";" + 
                                     str(s_final_balance) + "\n")
                            sf.close()
                        df.loc[df["CUSTOMER_ID"] == r_account, "BALANCE"] += amount
                        r_dest = str(r_account) + ".csv"
                        with open(r_dest, 'a') as rf:
                            rf.write(str(datetime.now()) + 
                                     ";TRANSFER FROM {};".format(str(s_account)) + 
                                     str(r_initial_balance) + ";" + 
                                     str(amount) + ";" + 
                                     str(r_final_balance) + "\n")
                            rf.close()
                        print("Transaction done!")
                        print("Your new balance is {}.".format(round(df[df.CUSTOMER_ID == s_account].BALANCE.item(), 2)))
                else: print("Your balance is too low!")
            else: print("Amount has to be larger than 0!")
        else: print("Receivers Account number is not correct!")
    else: print("Your Account number and/or password is not correct!")

if __name__ == '__main__':
    '''
    Load account database, set column types and remove indizes.
    '''
    df = pd.read_csv('account_data.csv', delimiter = ';')
    df.CUSTOMER_ID = df.CUSTOMER_ID.astype('object')
    df.BALANCE = df.BALANCE.astype('string')
    df.BALANCE = df.BALANCE.str.replace(',', '.')
    df.BALANCE = df.BALANCE.astype('float')
    df.index = [''] * len(df)
    
    while True:
        hashHead()
        print("Welcome to Power Bank!\nChoose one of the following options:")
        print("Enter 'C': Create new Account")
        print("Enter 'S': Show Account Details")
        print("Enter 'D': Deposit Money")
        print("Enter 'W': Withdraw Money")
        print("Enter 'T': Transfer Money to another Account")
        print("Enter 'Q': Quit Application")
        action = input("How may I help you?: ")
        
        if action == "Q": 
            df.to_csv('account_data.csv', sep = ';', index = False)
            break
        
        if action == "W": accWithdraw()
        if action == "D": accDeposit()
        if action == "S": accShow()
        if action == "C": accCreate()
        if action == "T": accTransfer()