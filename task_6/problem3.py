class BankAccount:
    def __init__ (self):
        self.balance=0

    def deposit(self,amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance = {self.balance}")

    def withdraw(self, amount): 
         if amount <= self.balance:
            self.balance -= amount
            print(f"Withdrawn {amount}. New balance = {self.balance}")
           
         else:
             print("Not enough balance!") 
               

account = BankAccount()
account.deposit(100)
account.withdraw(30)
account.withdraw(100)                
