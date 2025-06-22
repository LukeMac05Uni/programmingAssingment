import pandas as pd
import matplotlib.pyplot as plt
import os

# Terminal color codes for visual feedback in the terminal
green = '\033[92m'  # green text
red = '\033[91m'    # red text
reset = '\033[0m'   # reset text color

# File to store and load transactions
fileName = "budgetData.xlsx"

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