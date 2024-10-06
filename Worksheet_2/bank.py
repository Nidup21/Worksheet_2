# Import the necessary packages. 
import random

# Create a BankAccount class.
class BankAccount:
    # Initializing the account with an ID, passcode, category, and initial funds.
    def __init__(self, account_id, passcode, account_category, funds=0):
        # Assigning
        self.account_id = account_id
        self.passcode = passcode
        self.account_category = account_category
        self.funds = funds

    
    # Adds funds to the account.
    def deposit(self, amount):
        if amount > 0: # making sure that the amount is greater than zero/ positive
            self.funds += amount # Adding the amount tahe was deposited to the funds
            return "Deposit completed."
        return "Invalid amount for deposit."

    # Withdraw from the account 
    def withdraw(self, amount):
        if 0 < amount <= self.funds:
            self.funds -= amount
            return "Withdrawal completed."
        return "Insufficiency of funds or invalid withdrawal sum."

    # withdraw funds from the current account and deposit them into the recipient accoun
    def transfer(self, amount, recipient_account):
        withdrawal_message = self.withdraw(amount)
        if withdrawal_message == "Withdrawal completed.":
            recipient_account.deposit(amount)
            return "Transfer completed."
        return withdrawal_message

    # Initializes a PersonalAccount subclass of BankAccount
class PersonalAccount(BankAccount):
    def __init__(self, account_id, passcode, funds=0):
        super().__init__(account_id, passcode, "Personal", funds)

    # Initializes a BusinessAccount subclass of BankAccount
class BusinessAccount(BankAccount):
    def __init__(self, account_id, passcode, funds=0):
        super().__init__(account_id, passcode, "Business", funds)

    # A simple banking system that loads account data from a file.
class BankingSystem:
    def __init__(self, filename="account.txt"):
        self.filename = filename
        self.accounts = self.load_accounts()  

    # Loads account data from a file and creates account objects for each entry.
    def load_accounts(self):
        accounts = {}
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    account_id, passcode, account_category, funds = line.strip().split(",")
                    funds = float(funds) # Convert funds to float
                    if account_category == "Personal":
                        account = PersonalAccount(account_id, passcode, funds)
                    else:
                        account = BusinessAccount(account_id, passcode, funds)
                    accounts[account_id] = account
        except FileNotFoundError:
            pass
        return accounts
    


    # Saves the current account data to a file, writing each account's details as a comma-separated line.   
    def save_accounts(self):
        with open(self.filename, "w") as file:
            for account in self.accounts.values():
                file.write(f"{account.account_id},{account.passcode},{account.account_category},{account.funds}\n")

    # Creates a new account with a random ID and passcode, then saves the updated accounts to the file.
    def create_account(self, account_type):
        account_id = str(random.randint(10000, 999999))
        passcode = str(random.randint(1000, 9999))
        if account_type == "Personal":
            account = PersonalAccount(account_id, passcode)
        else:
            account = BusinessAccount(account_id, passcode)
        self.accounts[account_id] = account
        self.save_accounts()
        return account

    # Authenticates a user by checking the provided account ID and passcode against stored accounts.
    def login(self, account_id, passcode):
        account = self.accounts.get(account_id)
        if account and account.passcode == passcode:
            return account
        raise ValueError("Account number or password is not recognized")
    
    # Deletes the specified account from the system and saves the updated accounts to the file.
    def delete_account(self, account_id):
        if account_id in self.accounts:
            del self.accounts[account_id]
            self.save_accounts()
        else:
            raise ValueError("Account does not exist")
        
# Main function that initiates the banking system and presents a menu for user interactions.
def main():
    bank = BankingSystem()
    while True:
        print("\nHello. How can I assist you?\n1. Open Account\n2. Login to your Account\n3. Exit")
        choice = input("Enter your choice: ")

        # Handle user login and account operations
        if choice == "1":
            account_type = input("Select account type (1 for Personal, 2 for Business): ")
            if account_type == "1":
                account = bank.create_account("Personal")
            elif account_type == "2":
                account = bank.create_account("Business")
            else:
                print("Unsupported account type")
                continue
            print(f"Account created. Account id: {account.account_id}, Passcode: {account.passcode}")
        
        # Handle user login and provide access to account management options
        elif choice == "2":
            account_id = input("Enter your account id: ")
            passcode = input("Enter your passcode: ")
            try:
                account = bank.login(account_id, passcode)
                while True:
                    print("\n1. Check funds\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Delete Account\n6. Logout")
                    action = input("Enter your choice: ")

                    if action == "1":
                        print(f"Your funds is {account.funds}")

                    elif action == "2":
                        amount = float(input("please input the deposit amount: "))
                        print(account.deposit(amount))
                        bank.save_accounts()

                    elif action == "3":
                        amount = float(input("Please input the withdrawal amount: "))
                        print(account.withdraw(amount))
                        bank.save_accounts()

                    elif action == "4":
                        recipient_id = input("Enter recipient account id: ")
                        amount = float(input("Enter amount to transfer: "))
                        try:
                            recipient_account = bank.accounts[recipient_id]
                            print(account.transfer(amount, recipient_account))
                            bank.save_accounts()
                        except KeyError:
                            print("Recipient account does not exist.")

                    elif action == "5":
                        bank.delete_account(account_id)
                        print("Account deletion successful")
                        break

                    elif action == "6":
                        break

                    else:
                        print("Please select a valid option.")

            except ValueError as e:
                print(e)

        elif choice == "3":
            break

        else:
            print("Please select a valid option..")

# Entry point of the program
if __name__ == "__main__":
    main()

