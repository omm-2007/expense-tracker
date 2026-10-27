import json
import os
import tkinter as tk
from tkinter import ttk
from datetime import date

if os.path.exists("expenses.json"):
    with open("expenses.json", "r") as file:
        expense = json.load(file)
else:
    expense = []

if os.path.exists("budget.json"):
    with open("budget.json", "r") as file:
        budget = json.load(file)
else:
    budget = 0


def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expense, file, indent=4)


def monthly_total():
    this_month = str(date.today())[:7]
    total = 0
    for e in expense:
        if e.get("date", "")[:7] == this_month:
            total += e["amount"]
    return total


def refresh_ui():
    expense_list.delete(0, tk.END)
    for e in expense:
        row = f"{e['item']} - {e['amount']} | {e.get('category', 'Uncategorized')} | {e.get('date', 'No date')}"
        expense_list.insert(tk.END, row)

    total = monthly_total()
    if budget > 0:
        total_label.config(text=f"This month: {total} / Budget: {budget}")
    else:
        total_label.config(text=f"This month: {total} (no budget set)")

    if budget > 0 and total > budget:
        total_label.config(fg="red")
    else:
        total_label.config(fg="black")


def add_expense():
    item = item_entry.get().strip()
    if item == "":
        status_label.config(text="Enter an item name!")
        return

    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            status_label.config(text="Amount must be greater than zero!")
            return
    except ValueError:
        status_label.config(text="Enter numbers only!")
        return

    category = category_box.get().strip().title()
    if category == "":
        category = "Other"

    expense.append({
        "item": item,
        "category": category,
        "amount": amount,
        "date": str(date.today())
    })
    save_expenses()

    item_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    status_label.config(text="Saved! 💾")
    refresh_ui()


def delete_expense():
    selected = expense_list.curselection()
    if not selected:
        status_label.config(text="Select an expense first!")
        return

    removed = expense.pop(selected[0])
    save_expenses()
    status_label.config(text=f"Deleted {removed['item']}")
    refresh_ui()


def set_budget():
    global budget
    try:
        new_budget = float(budget_entry.get())
        if new_budget <= 0:
            status_label.config(text="Budget must be greater than zero!")
            return
    except ValueError:
        status_label.config(text="Enter numbers only!")
        return

    budget = new_budget
    with open("budget.json", "w") as file:
        json.dump(budget, file)

    budget_entry.delete(0, tk.END)
    status_label.config(text="Budget saved! 💾")
    refresh_ui()


window = tk.Tk()
window.title("Expense Tracker")
window.geometry("460x620")

tk.Label(window, text="What did you spend on?").pack()
item_entry = tk.Entry(window, width=30)
item_entry.pack()

tk.Label(window, text="Amount:").pack()
amount_entry = tk.Entry(window, width=30)
amount_entry.pack()

tk.Label(window, text="Category:").pack()
category_box = ttk.Combobox(window, values=["Food", "Travel", "Shopping", "Other"], width=27)
category_box.set("Other")
category_box.pack()

tk.Button(window, text="Add Expense", command=add_expense).pack(pady=6)

status_label = tk.Label(window, text="")
status_label.pack()

total_label = tk.Label(window, text="", font=("Arial", 11, "bold"))
total_label.pack(pady=4)

expense_list = tk.Listbox(window, width=60, height=14)
expense_list.pack(padx=10)

tk.Button(window, text="Delete selected", command=delete_expense).pack(pady=6)

tk.Label(window, text="Monthly budget:").pack()
budget_entry = tk.Entry(window, width=30)
budget_entry.pack()
tk.Button(window, text="Set budget", command=set_budget).pack(pady=6)

refresh_ui()
window.mainloop()