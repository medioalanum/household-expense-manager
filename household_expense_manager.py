import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"

def prepare_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow(["date", "description", "amount"])

def read_expenses():
    prepare_file()
    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        expenses = list(csv.DictReader(file))
    for expense in expenses:
        expense["amount"] = float(expense["amount"])
    return expenses

def add_expense():
    while True:
        try:
            date = datetime.strptime(input("Date (DD/MM/YYYY): ").strip(), "%d/%m/%Y").strftime("%d/%m/%Y")
            break
        except ValueError:
            print("Enter a valid date in DD/MM/YYYY format.")
    description = input("Description: ").strip()
    while not description:
        print("Description cannot be empty.")
        description = input("Description: ").strip()
    while True:
        try:
            amount = round(float(input("Amount: ").strip().replace(",", ".")), 2)
            if amount > 0 and amount < float("inf"):
                break
            print("Enter a positive, finite amount.")
        except ValueError:
            print("Enter a valid number, for example 12.50.")
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        csv.writer(file).writerow([date, description, f"{amount:.2f}"])
    print("Expense saved.")

def show_monthly_report():
    totals = {}
    for expense in read_expenses():
        month = datetime.strptime(expense["date"], "%d/%m/%Y").strftime("%Y-%m")
        totals[month] = totals.get(month, 0) + expense["amount"]
    if not totals:
        print("No expenses have been recorded yet.")
        return
    print("Monthly report")
    for month in sorted(totals):
        print(f"{month}: {totals[month]:.2f}")

def show_top_expenses():
    expenses = sorted(read_expenses(), key=lambda expense: expense["amount"], reverse=True)
    if not expenses:
        print("No expenses have been recorded yet.")
        return
    print("Top 10 expenses")
    for expense in expenses[:10]:
        print(f"{expense['date']} | {expense['description']} | {expense['amount']:.2f}")

def main():
    prepare_file()
    while True:
        print("\nHousehold Expense Manager")
        print("1. Add an expense")
        print("2. Monthly report")
        print("3. Top 10 expenses")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1": add_expense()
        elif choice == "2": show_monthly_report()
        elif choice == "3": show_top_expenses()
        elif choice == "0": print("Goodbye."); break
        else: print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
