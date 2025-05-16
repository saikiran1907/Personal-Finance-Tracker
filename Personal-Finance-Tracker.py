import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import json
import os
import datetime
import matplotlib.pyplot as plt

DATA_FILE = 'finance_data.json'


# Load existing data or create new
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return []


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


# Add transaction (income/expense)
def add_transaction(transaction_type):
    amount = simpledialog.askfloat(f"Add {transaction_type}", f"Enter amount:")
    if amount is None or amount <= 0:
        messagebox.showerror("Invalid Input", "Amount must be positive!")
        return

    category = simpledialog.askstring(f"{transaction_type} Category", "Enter category:")
    if not category:
        messagebox.showerror("Invalid Input", "Category cannot be empty!")
        return

    date = datetime.datetime.now().strftime('%Y-%m-%d')

    transaction = {
        'type': transaction_type,
        'amount': amount,
        'category': category,
        'date': date
    }

    data.append(transaction)
    save_data(data)
    messagebox.showinfo("Success", f"{transaction_type} added successfully!")


# View Summary
def view_summary():
    income = sum(item['amount'] for item in data if item['type'] == 'Income')
    expenses = sum(item['amount'] for item in data if item['type'] == 'Expense')
    balance = income - expenses

    summary_text = f"Total Income: ${income:.2f}\nTotal Expenses: ${expenses:.2f}\nRemaining Balance: ${balance:.2f}"
    messagebox.showinfo("Financial Summary", summary_text)


# View Category Report
def view_category_report():
    expense_data = {}
    for item in data:
        if item['type'] == 'Expense':
            expense_data[item['category']] = expense_data.get(item['category'], 0) + item['amount']

    if not expense_data:
        messagebox.showinfo("No Data", "No expenses to show.")
        return

    categories = list(expense_data.keys())
    amounts = list(expense_data.values())

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Category')
    plt.show()


# App Window Setup
app = tk.Tk()
app.title("Personal Finance Tracker")
app.geometry("400x400")
app.configure(bg="#87CEEB")

# Load Data
data = load_data()

# UI Elements
title_label = tk.Label(app, text="Finance Tracker Dashboard", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
title_label.pack(pady=20)

add_income_btn = tk.Button(app, text="Add Income", command=lambda: add_transaction('Income'), width=20, height=2)
add_income_btn.pack(pady=10)

add_expense_btn = tk.Button(app, text="Add Expense", command=lambda: add_transaction('Expense'), width=20, height=2)
add_expense_btn.pack(pady=10)

view_summary_btn = tk.Button(app, text="View Summary", command=view_summary, width=20, height=2)
view_summary_btn.pack(pady=10)

view_report_btn = tk.Button(app, text="View Category Report", command=view_category_report, width=20, height=2)
view_report_btn.pack(pady=10)

exit_btn = tk.Button(app, text="Exit", command=app.quit, width=20, height=2)
exit_btn.pack(pady=10)

# Run the App
app.mainloop()
