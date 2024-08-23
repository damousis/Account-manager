import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from Account import Bank_Account
from file import CSV_FILE
import random
import string
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.styles import Style


menu_completer = WordCompleter(['Add New Account', 'Deposit', 'Withdraw', 'Show Bank Details', 'Delete Account', 'Exit'], ignore_case=True)
expenses = ['GROCERIES','UTILITIES','ENTERTAINMENT','TRANSPORTATION']
#ΑΡΧΙΚΟΠΟΙΗΣΗ ΔΕΔΟΜΕΝΩΝ

CSV_FILE.initialize()
all_account = CSV_FILE.load()
all_id = [acc.id for acc in all_account]  # Update the all_id list with loaded data
index = None
a = None


#ΔΗΜΙΟΥΓΡΙΑ ΤΗΣ ΠΙΤΑΣ
def create_pie_chart(pos):
    # Extract the expenses for the specified account (pos)
    account = all_account[pos]

    # Prepare the data for the pie chart
    labels = ['GROCERIES', 'UTILITIES', 'ENTERTAINMENT', 'TRANSPORTATION']
    sizes = [account.groceries, account.utilities, account.entertainment, account.transportation]

    # Filter out zero-value categories
    filtered_labels = [label for label, size in zip(labels, sizes) if size > 0]
    filtered_sizes = [size for size in sizes if size > 0]

    # Check if there's any data to display
    if sum(filtered_sizes) > 0:  # Ensure there are non-zero expenses
        fig, ax = plt.subplots()
        ax.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(f"Expense Distribution for {account.holder}")
        plt.show()
    else:
        print("No expenses to display.")


#ΕΛΕΓΧΟΣ ΓΙΑ ΤΟ ΑΜΑ ΕΙΝΑΙ ΣΩΣΤΑ ΤΑ ΔΕΔΟΜΕΝΑ ΓΙΑ ΝΑ ΣΥΝΕΧΙΣΤΟΥΝ ΟΙ ΥΠΟΛΟΙΠΕΣ ΠΡΑΞΕΙΣ
def check():
    global index
    j = 3
    id = int(input("Give me your ID: "))

    while j > 0:
        index = None
        for i in range(len(all_id)):
            if id == all_id[i]:
                index = i
                j = -1
                break
        if index is None:
            j -= 1
            id = int(input(f"Wrong ID. Please try again ({j} more tries left): "))

    if j == 0:
        print("No more tries left, please try again in 2 minutes.")
        time.sleep(120)
        return None
    else:
        pas = input("Give me your password: ")
        while True:
            if pas == all_account[index].password:
                return index
            else:
                pas = input("Wrong password. Please try again: ")


#ΠΡΟΣΘΕΤΟΥΜΕ ΝΕΟ ΛΟΓΑΡΙΑΣΜΟ
def add_new_account():
    name = input('Give me your full name: ').upper()
    while True:
        try:
            mon = float(input('Give me the balance of the Account (It should be >= 0): '))
            if mon >= 0:
                break
            else:
                print("The value should be >= 0. Please try again.")
        except ValueError:
            print("Wrong input. Please give a valid number.")

    while True:
        try:
            id = int(input("Give me your 5 digit ID number: "))

            while True:
                if id in all_id:
                    id = int(input("The ID already exists. Please give me a new ID: "))
                else:
                    break

            if 10000 <= id <= 99999:
                break
            else:
                print("ID should be a 5 digit number.")
        except ValueError:
            print("Please enter a valid 5 digit ID number.")

    passw = input("Give me your password: ")

    # Create new Bank_Account instance
    na = Bank_Account(name, mon, id, passw, expenses=0, groceries=0, utilities=0, entertainment=0, transportation=0)

    # Append the new account to the in-memory lists
    all_account.append(na)
    all_id.append(id)

    # Save the new account to the CSV
    CSV_FILE.save([na])


#ΜΕΝΟΥ ΕΠΙΛΟΓΩΝ
def menu():

    print("------------------------------")
    print('Press :')
    print("1. ADD NEW ACCOUNT")
    print('2. DEPOSIT')
    print("3. WITHDRAW")
    print('4. SHOW BANK DETAILS')
    print('5. DELETE ACCOUNT')
    print('6. EXIT')
    print("------------------------------")

    while True:
        try:
            choice = int(input("What would you like to do?(Press a number from 1-6): "))
            if 1 <= choice <= 6:
                return choice
            else:
                print("Wrong input. Please give a number between 1 and 6.")
        except ValueError:
            print("You did not give me a number. Please give me a number between 1 and 6.")


def main():

    cont = 'y'
    while True:
        try:
            new_acc = int(input("Would you like to make a new account?Press 1 for yes else press any other number: "))
            break
        except ValueError:
            print('Wrong input.Please give me a number!\n')

    #ΕΛΕΓΧΟΣ ΓΙΑ ΤΟ ΑΜΑ ΕΙΝΑΙ ΝΑ ΠΡΟΣΘΕΣΟΥΜΕ ΛΟΓΑΡΙΑΣΜΟ
    if new_acc == 1:
        CSV_FILE.initialize()
        add_new_account()
        cont = input("Do you want to make some moves in your new account?(y/n)").lower()
        if cont == 'y':
            a = len(all_account)-1
            while True:
                    print("\n")
                    ch = menu()
                    if ch == 1:
                        add_new_account()

                    elif ch == 2:
                        amount = all_account[a].deposit()
                        CSV_FILE.new_dep(a,amount)

                    elif ch == 3:
                        amount = all_account[a].withdraw()
                        CSV_FILE.new_with(a,amount)
                        cat = input("Give me the category the money will be used to(groceries/utilities/entertainment"
                                    "/transportation) : ").capitalize()
                        CSV_FILE.add_expense(a, amount, cat)

                    elif ch == 4:
                        all_account[a].show_details()

                    elif ch == 5:
                            id_r = int(input("Give me the ID of the Account you want to delete : "))
                            CSV_FILE.clear(id_r)
                    else:
                        print("Exiting...")
                        return



    else:
        CSV_FILE.initialize()
        print("In order to make any movements with your account you will need to give me you ID and your password.\n")
        a = check()
        if a is not None:

            while True:
                print("\n")
                ch = menu()

                if ch == 2:
                    amount = all_account[a].deposit()
                    CSV_FILE.new_dep(a,amount)

                elif ch == 3:
                    amount = all_account[a].withdraw()
                    CSV_FILE.new_with(a,amount)
                    cat = input("Give me the category the money will be used to(groceries/utilities/entertainment"
                                "/transportation) : ").capitalize()
                    CSV_FILE.add_expense(a,amount,cat)

                    diag = input("Would you like to see a diagram of your expenses?(y/n) : ").lower()
                    if diag == 'y':
                        create_pie_chart(a)

                elif ch == 4:

                    all_account[a].show_details()

                elif ch == 5:

                    id_r = int(input("Give me the ID of the Account you want to delete : "))
                    CSV_FILE.clear(id_r)

                else:

                    print("Exiting...")
                    return


if __name__ == '__main__':
    main()

