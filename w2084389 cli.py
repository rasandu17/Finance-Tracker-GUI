import json
from datetime import datetime
import finance_tracker_gui 


# Global dictionary to store transactions
transactions = {}

# File handling functions
def load_transactions():
    #Load transactions from transactions.json file
    try:
        with open('transactions.json', 'r') as file:
            transaction = json.load(file)
            print("Transactions loaded successfully.")
            return transaction
    except FileNotFoundError:
        print("No transactions file found.")
        return {}

#Save transactions
def save_transactions():
    #Open the transactions.json in writing mode
    with open('transactions.json', 'w') as file:
        #Save the transactions to the file
        json.dump(transactions, file, indent=4)


# Feature implementations
def add_transaction():
    amount = 0
    category = ''
    date = ''
    #Get input for amount,category,date
    while True:
        method = input("How would you like to input your transactions?\nFor bulk input, please enter 'B'.\nFor inputting transactions one by one, please enter 'I'.\nYour choice: ").upper()
        if method in ['B','I']:#check user input 
                pass
                break
        else:
            print("Invalid input method!")
    #if user wants to input bulk transaction
    if method == 'B':
        filename = input("Enter the file name with format: ")   
        read_bulk_transactions_from_file(filename) #call the function to read bulk transactions from file
        
    
    #if user wants to input transaction one by one
    else:
        category = input("Enter category: ")
        #Get input for amount,category,date
        while True: #looping until user enters an amount
            try:
                amount = float(input("Enter amount: "))
                amount = round(amount, 2)
                break
            except ValueError:
                print("Please enter an amount!")

        date = get_valid_date_input("Enter date (YYYY-MM-DD): ")

        #Add new transaction to the dictionary
        transaction_id = len(transactions) + 1

        # Check if the transaction type exists in transactions, if not, create it
        if category not in transactions:
            transactions[category] = []
        
        # Add the transaction to the list for the expense type
        transaction = {'amount': amount, 'date':  date}
        transactions[category].append(transaction) #append the transaction to the list
        print("Transaction added successfully.")
        save_transactions()



    

#Display transaction history
def view_transactions():
    # View all transactions in the transactions dictionary.
    if not transactions:
        print("No transactions found to display.")
        return

    print("Transaction History")
    category_count = 1
    # Loop through each category and its transactions
    for category, transactions_list in transactions.items():
        
        print("-" * 35) #print 35 dashes
        print(f"{category_count}. Category: {category}")
        count = 1
        # Loop through each transaction in the category
        for transaction in transactions_list:
            print(f"{count}.")
            print("Amount   : ", transaction['amount'])
            print("Date     : ", transaction['date'])
            count += 1
        category_count += 1


#Update a new transaction to a existing transaction
def update_transaction():
    view_transactions()  # Display all current transactions
    global transactions

    if transactions:
        # Get the category and sub-transaction ID to update
        trans_id = get_valid_id_input("\nEnter the category ID to update: ") - 1
        category_list = list(transactions.keys())
        
        if 0 <= trans_id < len(category_list):
            category = category_list[trans_id]
            category_transactions = transactions[category]

            sub_id = get_valid_id_input(f"Enter the sub-transaction ID in '{category}' to update: ") - 1
            
            if 0 <= sub_id < len(category_transactions):
                transaction_details = category_transactions[sub_id]
                
                # Ask what the user wants to change
                change_option = input("Select to change (category/amount/date): ").lower()

                if change_option == "category":
                    new_category = input("Enter the new category: ")

                    # Create a new dictionary with the updated category
                    updated_expenses = {}
                    for key, value in transactions.items():
                        if key == category:
                            # Change the key to the new category
                            updated_expenses[new_category] = value
                        else:
                            updated_expenses[key] = value  # Keep other keys unchanged

                    # Update the original dictionary without reassigning
                    transactions.clear()
                    transactions.update(updated_expenses)

                elif change_option == "amount":
                    while True:
                        try:
                            new_amount = float(input("Enter the new amount: "))
                            transaction_details["amount"] = new_amount
                            break
                        except ValueError:
                            print("Invalid amount. Please enter a valid number.")

                elif change_option == "date":
                    new_date = get_valid_date_input("Enter the new transaction date (YYYY-MM-DD): ")
                    transaction_details["date"] = new_date

                save_transactions()  # Save changes to the file
                print("Transaction successfully updated!")
                return
            
            else:
                print("Sub-transaction ID not found.")

        else:
            print("Category ID not found.")

    else:
        print("No transactions yet.")




#Delete a transacction from a transaction list
def delete_transaction():
    view_transactions()

    # Ask user for category index
    del_id = get_valid_id_input("Enter the transaction ID to delete: ")
    # Check if the category ID is a valid index
    category_list = list(transactions.keys())
    if 1 <= del_id <= len(category_list):
        category = category_list[del_id - 1]
        transactions_list = transactions[category]

        # Ask user for transaction index
        sub_id = get_valid_id_input(f"Enter the sub transaction ID to delete in '{category}': ")
        # Check if the transaction ID is a valid index
        if 1 <= sub_id <= len(transactions_list):
            del transactions_list[sub_id - 1]
            
            save_transactions()
            print("Transaction deleted successfully.")

        else:
            print("Invalid sub transaction ID.")
    else:
        print("Invalid Transaction ID.")
    

#Read bulk transactions from a text file
def read_bulk_transactions_from_file(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Split the line by comma to get the expense type, amount, and date
                category, amount, date = line.strip().split(',')
                
                # Convert the amount to a float
                amount = float(amount)
                
                # If the expense type is not in the transactions dictionary, add it
                if category not in transactions:
                    transactions[category] = []
                
                # Add the transaction to the list for the expense type
                transactions[category].append({'amount': amount, 'date' : date})
            print("Bulk transactions added successfully.")
            save_transactions()
    
    #Error handling
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except ValueError:
        print("Invalid data format. Type, amount, and date must be separated by commas.")
    
#Get valid integer ID
def get_valid_id_input(message):
    while True:
        try:
            value = int(input(message)) #Get integer input from user
            return value
        except ValueError:
            print("Please enter a valid integer!")


#Get valid date input
def get_valid_date_input(message):
    while True:
        try:
            date = input(message) #Get date input from user 
            datetime.strptime(date, "%Y-%m-%d")
            return date  
        except ValueError:
            print("Invalid date format")


#Display summary of transactions
def display_summary():
    #Check if transactions are empty
    if not transactions:
        print("No transactions found.")
        return
    else:
        print("\nCategory - Total Expenses (Rs.)")
        print("-" * 35)
        
        total_expenses_all = 0
        # Loop through each category and its transactions
        for category, category_transactions in transactions.items():
            total_expenses = sum(transaction["amount"] for transaction in category_transactions)
            print(f"{category} - {total_expenses:.2f}")
            total_expenses_all += total_expenses
        
        print("-" * 35)
        print(f"Total Expenses - {total_expenses_all:.2f}")


#Main menu
def main_menu():
    #Load transactions at the start 
    transactions.update(load_transactions())  
    
    #Display choice

    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Open GUI")
        print("7. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary()
        elif choice == '6':
            print("GUI loaded succesfully")
            finance_tracker_gui.main()
            
        elif choice == '7':
            print("Exiting program.")
            save_transactions()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
    save_transactions()  







