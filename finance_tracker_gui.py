import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime


# Define the GUI class
class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")

        self.columns = ['Category', 'Date', 'Amount']  # Define the column names
        self.create_widgets()  # Create the widgets

        self.transactions = self.load_transactions("transactions.json") # Load transactions from file
        self.sort_reverse = {} # Dictionary to store sort order for each column
        for col in self.columns:
            self.sort_reverse[col] = False # Default to ascending sort for each column

    
    def create_widgets(self):
        # Main title
        main_title = ttk.Label(self.root, text="Personal Finance Tracker", font=("Helvetica", 16, "bold"))
        main_title.pack(pady=10)

        # Frame for table and scrollbar
        self.frame_table = ttk.Frame(self.root)
        self.frame_table.pack(fill=tk.BOTH, expand=True)

        # Treeview for displaying transactions
        self.table_trv = ttk.Treeview(self.frame_table, columns=self.columns, show='headings')

        # Set up column headings with sorting functionality
        for col in self.columns:
            self.table_trv.heading(col, text=col, command=lambda c=col: self.sort_column(c))

        self.table_trv.pack(side='left', pady=10, padx=10, fill='both', expand=True)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self.frame_table, orient='vertical', command=self.table_trv.yview)
        scrollbar.pack(side='right', fill='y')
        self.table_trv.configure(yscrollcommand=scrollbar.set)

        # Frame for buttons
        self.frame_b = ttk.Frame(self.root)  # Define the frame for buttons
        self.frame_b.pack(fill=tk.BOTH, expand=True)

        # Search bar and button
        self.entry_box = ttk.Entry(self.frame_b, width=20)
        self.entry_box.pack(side='left', padx=10)
        self.search_button = ttk.Button(self.frame_b, text="Search", command=self.search_transactions)
        self.search_button.pack(side='left', pady=5)

        # Refresh button
        self.refresh_button = ttk.Button(self.frame_b, text="Refresh", command=self.confirm_refresh)
        self.refresh_button.pack(side='left', pady=10)


    #Load transactions from a file
    def load_transactions(self, filename):
        try:
            with open(filename, 'r') as file:
                transaction = json.load(file)
                return transaction
        except FileNotFoundError:
            return {}


    # Save transactions to a file
    def display_transactions(self, transactions):
        # Clear existing entries
        self.table_trv.delete(*self.table_trv.get_children())

        # Add transactions to the Treeview
        for category, category_transactions in transactions.items():
            for transaction in category_transactions: # Loop through each transaction in the category
                date = transaction['date']
                amount = transaction['amount']
                self.table_trv.insert("", 'end', values=(category, date, amount))


    # Search for transactions
    def search_transactions(self):
        # Get the search term and clear the Treeview
        search_term = self.entry_box.get().lower()

        # Check if the search term is empty
        if not search_term:
            messagebox.showerror("Empty", "Search term cannot be empty.")
            return
        # Clear the Treeview
        self.table_trv.delete(*self.table_trv.get_children())

        # Filter and display the matching transactions
        found = False  # Flag to indicate if any results were found
        for category, category_transactions in self.transactions.items():
            for transaction in category_transactions:
                if (search_term in category.lower() or
                    search_term == transaction['date'].lower() or
                    search_term == str(transaction['amount'])):  # Check if the search term matches the category, date, or amount
                    self.table_trv.insert("", 'end', values=(category, transaction['date'], transaction['amount']))
                    found = True  # Set the flag to True if any results are found

        # If no results were found, display a message box
        if not found:
            messagebox.showinfo("No Results", "No transactions found ")


    # Confirm before refreshing all transactions
    def confirm_refresh(self):
        # Confirm before refreshing all transactions
        confirm = messagebox.askyesno("Refresh", "Do you want to refresh all transactions?")
        if confirm:
            self.display_transactions(self.transactions)


    # Sort transactions by column
    def sort_column(self, col):
        # Get the current sort order for the column
        reverse = self.sort_reverse[col]
        self.sort_by_column(col, reverse)
        self.sort_reverse[col] = not reverse  # Toggle the sort order


    # Sort transactions by column
    def sort_by_column(self, col, reverse):
        # Combine all transactions into a single list
        all_transactions = []
        for category, category_transactions in self.transactions.items(): # Loop through each category
            for transaction in category_transactions: 
                transaction['category'] = category # Add the category to the transaction
                all_transactions.append(transaction) 

        # Sort transactions based on the selected column
        if col == 'Date':
            # Sort by date
            all_transactions.sort(key=lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%d'), reverse=reverse)
        elif col == 'Amount':
            # Sort by amount
            all_transactions.sort(key=lambda x: x['amount'], reverse=reverse)
        elif col == 'Category':
            # Sort by category
            all_transactions.sort(key=lambda x: x['category'].lower().strip(), reverse=reverse)

        # Clear the Treeview and insert sorted transactions
        self.table_trv.delete(*self.table_trv.get_children())

        # Insert sorted transactions into the Treeview
        for transaction in all_transactions: 
            category = transaction['category']
            date = transaction['date']
            amount = transaction['amount']
            self.table_trv.insert("", 'end', values=(category, date, amount))

# Main function
def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    app.display_transactions(app.transactions)
    root.mainloop()

if __name__ == "__main__":
    main()
