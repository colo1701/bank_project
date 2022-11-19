import bcrypt
from bank import ConsoleDesign
from bank import Account

account1 = Account()
account2 = Account()

account1.show()
account2.show()

account1.deposit(1000)

account2.kill()

account1.transfer(account2, 300)

account1.show()
account2.show()