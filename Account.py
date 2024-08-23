class Bank_Account:
    def __init__(self, holder, balance, id, password,expenses,groceries,utilities,entertainment,transportation):
        self.holder = holder
        self.balance = balance
        self.id = id
        self.password = password
        self.expenses = expenses
        self.groceries = groceries
        self.utilities = utilities
        self.entertainment = entertainment
        self.transportation = transportation

     #ΓΙΑ ΚΑΤΑΘΕΣΗ ΧΡΗΜΑΤΩΝ
    def deposit(self):

        while True:
            try:
                amount = float(input("Give me the amount that you want to deposit:"))
                if amount > 0:
                    self.balance += amount
                    print(f"{amount} $ have successfully been deposited to your account!")
                    return amount
                else:
                    print("You did not give me a valid number.Please give a number bigger than 0!")
            except ValueError:
                print("You did not give me a number.Please give me a number bigger than 0!")

    #ΓΙΑ ΑΝΑΛΗΨΗ ΧΡΗΜΑΤΩΝ
    def withdraw(self):
        while True:
            try:
                amount = float(input("give me the amount you want to withdrawn from your account: "))
                if amount > 0:

                    if self.balance - amount >=0:
                        self.balance -= amount
                        print("The money have been successfully withdrawn from the account")
                        return amount
                    else:
                        print('There is not enough in your bank account!Please give a smaller amount')
                else:
                    print('Invalid input.Please give a number bigger than 0.')

            except ValueError:
                print("Please give me a number!")

    #ΕΜΦΑΝΙΣΗ ΤΟΥ ΥΠΟΛΟΙΠΟΥ ΤΟΥ ΛΟΓΑΡΙΑΣΜΟΥ
    def show_details(self):

        print('ACCOUNT HOLDER :',self.holder)
        print('BALANCE : ',self.balance)
        print('EXPENSES : ',self.expenses)

