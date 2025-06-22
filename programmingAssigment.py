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

# Allow the user to update a specific transaction
def updateTransaction(df):
    if df.empty:
        print(f"{red}No transactions to update.{reset}\n")
        return df
    else:
        viewTransactions(df)  # Show current entries
        try:
            index = int(input("Enter the index of transaction to update: "))
            if 0 <= index < len(df):
                transactionType = df.at[index, "Type"]  # get the transaction type

                # Ask what fields to update
                if input("Edit amount? (y/n): ").strip().lower() == "y":
                    df.at[index, "Amount"] = float(input("Enter new amount: "))
                if input("Edit description? (y/n): ").strip().lower() == "y":
                    df.at[index, "Description"] = input("Enter new description: ")
                if input("Edit category? (y/n): ").strip().lower() == "y":
                    print(f"\nSelect a category for this {transactionType}:")
                    categories = defaultCategories.get(transactionType, [])
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
                    df.at[index, "Category"] = category  # <-- Don't forget to assign the new category

                if input("Edit date? (y/n): ").strip().lower() == "y":
                    while True:
                        try:
                            year = int(input("Enter new year (e.g. 2025): "))
                            month = int(input("Enter new month (1-12): "))
                            day = int(input("Enter new day (1-31): "))
                            newDate = datetime.datetime(year, month, day).strftime("%Y-%m-%d")
                            df.at[index, "Date"] = newDate
                            df.at[index, "Month"] = pd.to_datetime(newDate).to_period("M").strftime("%Y-%m")
                            break
                        except ValueError:
                            print(f"{red}Invalid date. Please try again.{reset}")
                saveData(df)
                print(f"{green}Transaction updated{reset}\n")
            else:
                print(f"{red}Invalid index{reset}\n")
        except ValueError:
            print(f"{red}Please enter a valid number.{reset}\n")
        return df

# Delete a specific transaction by index
def deleteTransaction(df):
    if df.empty:
        print(f"{red}No transactions to delete.{reset}\n")
        return df
    else:
        viewTransactions(df)
        try:
            index = int(input("Enter the index of transaction to delete: "))
            if 0 <= index < len(df):
                df = df.drop(index).reset_index(drop=True)
                saveData(df)
                print(f"{green}Transaction deleted{reset}\n")
            else:
                print(f"{red}Invalid index{reset}\n")
        except ValueError:
            print(f"{red}Please enter a valid number.{reset}\n")
        return df

# Calculate and display total income, expense, and current balance
def showBalance(df):
    income = df[df["Type"] == "income"]["Amount"].sum()
    expense = df[df["Type"] == "expense"]["Amount"].sum()
    balance = income - expense
    print(f"{green}Total Income: £{income:.2f}{reset}")
    print(f"{red}Total Expense: £{expense:.2f}{reset}")
    print(f"Current Balance: £{balance:.2f}\n")

# Generate a pie chart comparing total income and expenses
def showGraph(df):
    if df.empty:
        print(f"{red}No data for graph.{reset}\n")
        return
    summary = df.groupby("Type")["Amount"].sum()
    summary.plot(kind="pie", autopct='%1.1f%%', startangle=90)
    plt.title("Income vs Expenses")
    plt.ylabel("")  # Hides the y-axis label
    plt.show()

# Generate a bar chart showing monthly income and expense summary
def showMonthlySummary(df):
    if df.empty:
        print(f"{red}No data available.{reset}\n")
        return

    # Parse date and update Month field
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    # Group by month and type
    summary = df.groupby(["Month", "Type"])["Amount"].sum().unstack(fill_value=0)

    # Plot bar chart
    summary.plot(kind="bar", figsize=(10, 5))
    plt.title("Monthly Income vs Expenses")
    plt.xlabel("Month")
    plt.ylabel("Amount (£)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(title="Type")
    plt.show()

# Main menu loop: allows users to choose actions
def main():
    df = loadData()  # Load existing data or create new
    while True:
        # Menu options
        print("\n==== Personal Budget Monitor ====")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Show Balance")
        print("6. Show Pie Chart (Total Income vs Expenses)")
        print("7. Show Bar Chart (Monthly Summary)")
        print("8. Exit")
        choice = input("Choose an option: ")

        # Menu logic
        if choice == "1":
            df = addTransaction(df)
        elif choice == "2":
            viewTransactions(df)
        elif choice == "3":
            df = updateTransaction(df)
        elif choice == "4":
            df = deleteTransaction(df)
        elif choice == "5":
            showBalance(df)
        elif choice == "6":
            showGraph(df)
        elif choice == "7":
            showMonthlySummary(df)
        elif choice == "8":
            print(f"{green}Goodbye{reset}")
            break
        else:
            print(f"{red}Invalid choice. Please try again.{reset}\n")


main()