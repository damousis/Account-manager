import pandas as pd
from Account import Bank_Account


class CSV_FILE:
    filename = "Expenses_tracker.csv"
    columns = ['Holder', 'Balance', 'ID', 'Password', 'Expenses', 'Groceries', 'Utilities', 'Entertainment',
               'Transportation']

    @classmethod
    def initialize(cls):
        try:
            df = pd.read_csv(cls.filename)

            if df.empty:
                raise ValueError("Empty file")

            # Convert necessary columns to numeric
            df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')
            df['ID'] = pd.to_numeric(df['ID'], errors='coerce').astype(int)
            df['Expenses'] = pd.to_numeric(df['Expenses'], errors='coerce')
            df['Groceries'] = pd.to_numeric(df['Groceries'], errors='coerce')
            df['Utilities'] = pd.to_numeric(df['Utilities'], errors='coerce')
            df['Entertainment'] = pd.to_numeric(df['Entertainment'], errors='coerce')
            df['Transportation'] = pd.to_numeric(df['Transportation'], errors='coerce')

            return df
        except (FileNotFoundError, ValueError, pd.errors.EmptyDataError):
            # Create an empty DataFrame if file is missing or empty
            df = pd.DataFrame(columns=cls.columns)
            df.to_csv(cls.filename, index=False)
            return df

    @classmethod
    def save(cls, account_or_accounts):
        # Load current data
        df = cls.initialize()

        if isinstance(account_or_accounts, Bank_Account):
            account_or_accounts = [account_or_accounts]

        # Add new account data
        new_data = []
        for acc in account_or_accounts:
            # Prepare the new account's data
            new_row = {
                'Holder': acc.holder,
                'Balance': acc.balance,
                'ID': acc.id,
                'Password': acc.password,
                'Expenses': acc.expenses,
                'Groceries': acc.groceries,
                'Utilities': acc.utilities,
                'Entertainment': acc.entertainment,
                'Transportation': acc.transportation
            }
            new_data.append(new_row)

        new_df = pd.DataFrame(new_data)

        # Concatenate the new account data to the existing DataFrame
        df = pd.concat([df, new_df], ignore_index=True)

        # Save the updated DataFrame back to the CSV
        df.to_csv(cls.filename, index=False)

    @classmethod
    def load(cls):
        df = cls.initialize()
        accounts = []
        for _, row in df.iterrows():
            accounts.append(
                Bank_Account(
                    row['Holder'], float(row['Balance']), int(row['ID']), row['Password'],
                    float(row['Expenses']), float(row['Groceries']), float(row['Utilities']),
                    float(row['Entertainment']), float(row['Transportation'])
                )
            )
        return accounts

    @classmethod
    def clear(cls, id_remove):
        df = pd.read_csv(cls.filename)

        if id_remove not in df['ID'].values:
            print("The ID was not found!")
            return

        df = df[df['ID'] != id_remove]
        df.to_csv(cls.filename, index=False)
        print(f"The account with ID: {id_remove} has been successfully deleted.")

    @classmethod
    def new_with(cls, pos, am):
        df = pd.read_csv(cls.filename)

        df['Expenses'] = pd.to_numeric(df['Expenses'], errors='coerce')
        df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')

        df.at[pos,'Balance'] -= am
        df.at[pos,'Expenses'] += am

        df.to_csv(cls.filename, index=False)

    @classmethod
    def new_dep(cls, pos, am):
        # Load the CSV file
        df = pd.read_csv(cls.filename)

        # Ensure 'Expenses' column is numeric
        df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')

        # Add the amount `am` to the specific position's 'Expenses'
        df.at[pos, 'Balance'] += am  # Add the amount to the existing value

        # Save the updated DataFrame back to the CSV
        df.to_csv(cls.filename, index=False)

    @classmethod
    def add_expense(cls,pos,am,cat):

        df = pd.read_csv(cls.filename)
        df[cat] = pd.to_numeric(df[cat],errors='coerce')

        df.at[pos,cat] += am

        df.to_csv(cls.filename,index=False)



















