import json
import os
import tkinter as tk
from datetime import date

if os.path.exists("expenses.json"):
    with open("expenses.json", "r") as file:
        expense = json.load(file)
else:
    expense = []

window = tk.Tk()
window.title("Expense Tracker")
window.geometry("400x300")

label = tk.Label(window, text="What did you spend on?")
label.pack()

item_entry = tk.Entry(window)
item_entry.pack()

amount_label = tk.Label(window, text="Amount:")
amount_label.pack()

amount_entry = tk.Entry(window)
amount_entry.pack()

status_label = tk.Label(window, text="")
status_label.pack()

expense_list = tk.Listbox(window, width=50)
expense_list.pack()

def refresh_list():
    expense_list.delete(0, tk.END)
    for e in expense:
        expense_list.insert(tk.END, e["item"] + " - " + str(e["amount"]))


def add_expense():
    item = item_entry.get()

    try:
        amount = float(amount_entry.get())
    except ValueError:
        status_label.config(text="Enter numbers only!")
        return

    expense.append({
        "item": item,
        "amount": amount,
        "date": date.today().strftime("%Y-%m-%d")
    })

    with open("expenses.json", "w") as file:
        json.dump(expense, file, indent=4)

        status_label.config(text="Saved! 💾")
        item_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
    

button = tk.Button(window, text="Add Expense", command=add_expense)
button.pack()

refresh_list()

window.mainloop()