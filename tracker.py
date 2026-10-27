import json 
import os
from datetime import date
def show_monthly_total(expense):
        this_month = str(date.today())[:7]
        total_spent = 0
        for e in expense:
            if e.get("date", "")[:7] == this_month:
                total_spent = total_spent + e["amount"]
        print("Total so far:", total_spent)
        return total_spent
def suggest_category(item):
    item = item.lower()

    if any(word in item for word in ["pizza", "food", "burger", "coffee"]):
        return "Food"
    elif any(word in item for word in ["bus", "train", "taxi", "uber"]):
        return "Travel"
    elif any(word in item for word in ["shirt", "shoes", "shopping"]):
        return "Shopping"
    else:
        return "Other"

if os.path.exists("expenses.json"):
    with open("expenses.json", "r") as file:
        expense = json.load(file)
    print("Loaded expenses:", expense)
else:
    expense = []
    
if os.path.exists("budget.json"):
    with open("budget.json", "r") as file:
        budget = json.load(file)
        
else:
    budget = 0            

print("File location:", os.path.abspath("expenses.json"))

while True:
    print("1. Add expense")
    print("2. View expenses")
    print("3. Delete expense")
    print("4. Edit expense")
    print("5. Category-wise summary")
    print("6. Filter expenses by date")
    print("7. Set monthly budget")
    print("8. Exit")
    choice = input("Choose: ")
    
    if choice == "8":
        print("Exiting...")
        break

    if choice == "1":
        item = input("What did you spend on? ")
        category = suggest_category(item)

        print("Suggested category:", category)
        confirm = input("Use this category? (y/n): ").lower()

        if confirm == "n":
            category = input("Enter your category: ")

        try:
            amount = float(input("How much did you spend? "))
            if amount <= 0:
                print("Amount must be greater than zero!")
                continue
        except ValueError:
            print("Invalid amount! Enter numbers only.")
            continue

        entry = {
            "item": item,
            "category": category,
            "amount": amount,
            "date": str(date.today())
        }
        expense.append(entry)

        with open("expenses.json", "w") as file:
            json.dump(expense, file, indent=4)

        print("Added and saved! 💾")
        total_spent = show_monthly_total(expense)
        if budget > 0 and total_spent > budget:
            print("Warning: You have exceeded your monthly budget! ⚠️")    
        

    elif choice == "2":
        total = 0

        if not expense:
            print("No expenses recorded yet!")

        else:
            for entry in expense:
                print(entry["item"], "-", entry["amount"], "| Category:", entry.get("category", "Uncategorized"), "| Date:", entry.get("date", "No date"))
                total += entry["amount"]

            print("Total spent:", total)

    elif choice == "3":
        if not expense:
            print("No expenses to delete!")

        else:
            for i, entry in enumerate(expense, start=1):
                print(i, entry["item"], "-", entry["amount"], "| Category:", entry.get("category", "Uncategorized"), "| Date:", entry.get("date", "No date"))

            try:
                delete_choice = int(input("Enter expense number to delete: "))
            except ValueError:
                print("Invalid input! Enter a number.")
                continue

            if 1 <= delete_choice <= len(expense):
                removed = expense.pop(delete_choice - 1)

                with open("expenses.json", "w") as file:
                    json.dump(expense, file, indent=4)

                print(removed["item"], "deleted successfully!")

            else:
                print("Invalid expense number!")

    elif choice == "4":
        if not expense:
            print("No expenses to edit!")
        else:
            for i, entry in enumerate(expense, start=1):
                print(i, entry["item"], "-", entry["amount"], "| Category:", entry.get("category", "Uncategorized"), "| Date:", entry.get("date", "No date"))

            try:
                edit_choice = int(input("Enter expense number to edit: "))
            except ValueError:
                print("Invalid input! Enter a number.")
                continue

            if 1 <= edit_choice <= len(expense):
                entry = expense[edit_choice - 1]

                entry["item"] = input("Enter new expense name: ")

                try:
                    new_amount = float(input("Enter new amount: "))
                    if new_amount <= 0:
                        print("Amount must be greater than zero!")
                        continue
                except ValueError:
                    print("Invalid amount! Enter numbers only.")
                    continue

                entry["amount"] = new_amount

                with open("expenses.json", "w") as file:
                    json.dump(expense, file, indent=4)

                print("Expense updated successfully! ✅")
            else:
                print("Invalid expense number!")

    elif choice == "5":
        if not expense:
            print("No expenses recorded yet!")
        else:
            categories = {}

            for entry in expense:
                category = entry.get("category", "Uncategorized")
                categories[category] = categories.get(category, 0) + entry["amount"]

            print("\n--- Category-wise Summary ---")
            for category, total in categories.items():
                print(category, ":", total)
    
    elif choice == "6":
        search_date = input("Enter date to filter (2026-10-27): ")
        
        found = False
        for entry in expense:
            if entry.get("date") == search_date:
                print(entry["item"], "-", entry["amount"], "| Category:", entry.get("category", "Uncategorized"), "| Date:", entry.get("date", "No date"))
                found = True

        if not found:
            print("No expenses found for the specified date.")
            
    elif choice == "7":
        try:
            budget = float(input("Enter your monthly budget: "))
            
            if budget <= 0:
                print("Budget must be greater than zero!")
                continue
            with open("budget.json", "w") as file:
                    json.dump(budget, file) 
                    
            print("Monthly budget saved successfully! 💾")    
                
        except ValueError:
            print("Invalid budget! Enter numbers only.")
            continue