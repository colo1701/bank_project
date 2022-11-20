class ConsoleDesign():
    def head():
        print("")
        print(80 * "#")
        print("")

class Account():
    def __init__(self):
        ConsoleDesign.head()
        print("Creating account")
        self.name = input("Please enter account name: ")
        self.amount = 0
        self.password = input("Please enter your new account password: ")
        self.active = True
        print("New Account initiated for {}. The initial balance is 0.".format(self.name))
        print("Please don't forget your password!")

    def deposit(self, cash):
        ConsoleDesign.head()
        print("Depositing {} in Account of {}".format(cash, self.name))
        if self.active == False: return print("Account does not exist!")
        if cash <= 0: return print("The amount has to be positive!")
        if input("Hello {}, please enter password: ".format(self.name)) != self.password:
            return print("Incorrect password!")
        self.amount += cash
        return print("The new balance is {}.".format(self.amount))

    def show(self):
        ConsoleDesign.head()
        print("Showing Account of {}".format(self.name))
        if self.active == False: return print("Account does not exist!")
        if input("Hello {}, please enter password: ".format(self.name)) != self.password:
            return print("Incorrect password!")
        return print("The actual balance is {}.".format(self.amount))

    def withdraw(self, cash):
        ConsoleDesign.head()
        print("Withdrawing {} from Account of {}".format(cash, self.name))
        if self.active == False: return print("Account does not exist!")
        if cash <= 0: return print("The amount has to be positive!")
        if input("Hello {}, please enter password: ".format(self.name)) != self.password:
            return print("Incorrect password!")
        if self.amount - cash < 0: return print("You can't withdraw more than you have in your account!")
        self.amount -= cash
        return print("The new balance is {}.".format(self.amount))

    def kill(self):
        ConsoleDesign.head()
        print("Deleting Account of {}".format(self.name))
        if input("Hello {}, please enter password: ".format(self.name)) != self.password:
            return print("Incorrect password!")
        self.active = False
        return print("Account deleted!")

    def transfer(self, receiver, cash):
        ConsoleDesign.head()
        print("Transfering {} to account of {}".format(cash, receiver.name))
        if self.active == False: return print("Account does not exist!")
        if cash <= 0: return print("The amount has to be positive!")
        if receiver.active != True: return print("Receiving account does not exist!")
        if input("Hello {}, please enter password: ".format(self.name)) != self.password:
            return print("Incorrect password!")
        if self.amount - cash < 0: return print("You can't transfer more than you have in your account!")
        self.amount -= cash
        receiver.amount += cash
        return print("Transfer completed!")