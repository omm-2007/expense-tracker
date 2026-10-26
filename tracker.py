expense = []

while True:
    print("1. Add expense")
    print("2. View expenses")
    print("3. Exit")
    choice = input("Choose: ")
    
    if choice == "3":
        print("Exiting...")
        break
    
    if choice == "1":
        item = input("What did you spend on? ")
        amount = float(input("How much did you spend? "))
        entry = {"item": item, "amount": amount}
        expense.append(entry)
        print("Added!")
        
    elif choice == "2":
        total = 0
        for entry in expense:
            print(entry["item"], "-", entry["amount"])
            total = total + entry["amount"]
            print("Total spent:", total)
                