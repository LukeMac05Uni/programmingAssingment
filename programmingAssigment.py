import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os

# Terminal color codes for visual feedback in the terminal
green = '\033[92m'  # green text
red = '\033[91m'    # red text
reset = '\033[0m'   # reset text color

# File to store and load transactions
fileName = "budgetData.xlsx"

# Default categories for income and expenses
defaultCategories = {
    "income": ["Salary", "Bonus", "Investment", "Gift"],
    "expense": ["Groceries", "Rent", "Utilities", "Transport", "Dining", "Healthcare"]
}

def loadData():
    if os.path.exists(fileName):
        df = pd.read_excel(fileName)  # Load existing data
    else:
        # Create a new empty DataFrame with expected columns
        df = pd.DataFrame(columns=["Type", "Amount", "Description", "Date", "Month", "Category"])
    
    # Ensure "Amount" is float for calculations
    if "Amount" in df.columns:
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0).astype(float)

    return df

def saveData(df):
    df.to_excel(fileName, index=False)

# Add a new transaction (income or expense)
def addTransaction(df):

    # Ask user for the type of transaction
    while True:
        transactionType = input("Enter type (income/expense): ").strip().lower()
        if transactionType in ["income", "expense"]:
            break
        else:
            print(f"{red}Invalid type. Please enter 'income' or 'expense'.{reset}")

    # Get the amount from the user
    while True:
        try:
            amount = float(input("Enter amount: "))
            break
        except ValueError:
            print(f"{red}Invalid amount. Please enter a numeric value.{reset}")

    # Get description from the user
    description = input("Enter description: ")

    # Ask user to choose or enter a category
    print(f"\nSelect a category for this {transactionType}:")
    categories = defaultCategories[transactionType]
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    print(f"{len(categories)+1}. Other (custom category)")

    while True:
        try:
            choice = int(input("Choose a category number: "))
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                break
            elif choice == len(categories) + 1:
                category = input("Enter custom category: ").strip()
                break
            else:
                print(f"{red}Invalid choice. Please try again.{reset}")
        except ValueError:
            print(f"{red}Please enter a valid number.{reset}")

    # Allow user to enter a custom date, or use the current date
    useCustomDate = input("Use custom date? (y/n): ").strip().lower()
    if useCustomDate == "y":
        while True:
            try:
                year = int(input("Enter year (e.g. 2025): "))
                month = int(input("Enter month (1-12): "))
                day = int(input("Enter day (1-31): "))
                date = datetime.datetime(year, month, day)
                break
            except ValueError:
                print(f"{red}Invalid date. Please enter valid numbers.{reset}")
    else:
        date = datetime.datetime.now()

    # Format the date and month
    dateStr = date.strftime("%d-%m-%Y")
    monthStr = date.strftime("%m-%Y")

    # Add the new transaction to the DataFrame
    newEntry = pd.DataFrame([[transactionType, amount, description, dateStr, monthStr, category]],
                             columns=["Type", "Amount", "Description", "Date", "Month", "Category"])
    df = pd.concat([df, newEntry], ignore_index=True)

    # Save changes and confirm
    saveData(df)
    print(f"{green}Transaction added{reset}\n")
    return df

# Display all transactions to the user
def viewTransactions(df):
    if df.empty:
        print(f"{red}No transactions found.{reset}\n")
    else:
        displayData = ["Type", "Amount", "Description", "Category", "Date"]
        print(df[displayData].to_string(index=True), "\n")

# Main menu loop: allows users to choose actions
def main():
    df = loadData()  # Load existing data or create new
    while True:
        # Menu options
        print("\n==== Personal Budget Monitor ====")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Exit")
        choice = input("Choose an option: ")

        # Menu logic
        if choice == "1":
            df = addTransaction(df)
        elif choice == "2":
            viewTransactions(df)
        elif choice == "3":
            print(f"{green}Goodbye{reset}")
            break
        else:
            print(f"{red}Invalid choice. Please try again.{reset}\n")


main()