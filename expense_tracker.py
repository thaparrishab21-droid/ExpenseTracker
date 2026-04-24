import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date TEXT,
    note TEXT
)
""")
conn.commit()

# Function to add expense
def add_expense():
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    date = input("Enter date (YYYY-MM-DD): ")
    note = input("Enter note: ")

    cursor.execute(
        "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (amount, category, date, note)
    )
    conn.commit()
    print("Expense added successfully!")

# Function to view expenses
def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    records = cursor.fetchall()

    if not records:
        print("No expenses found.")
        return

    print("\nID | Amount | Category | Date | Note")
    print("----------------------------------------")
    for row in records:
        print(row)

# Function to delete expense
def delete_expense():
    expense_id = int(input("Enter expense ID to delete: "))
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    print("Expense deleted!")

#Function to update expense
def update_expense():
    expense_id = int(input("Enter expense ID to update: "))

    new_amount = float(input("Enter new amount: "))
    new_category = input("Enter new category: ")
    new_date = input("Enter new date (YYYY-MM-DD): ")
    new_note = input("Enter new note: ")

    cursor.execute(
        "UPDATE expenses SET amount = ?, category = ?, date = ?, note = ? WHERE id = ?",
        (new_amount, new_category, new_date, new_note, expense_id)
    )
    conn.commit()
    print("Expense updated successfully!")

#Function to category summary
def category_summary():
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses GROUP BY category"
    )
    result = cursor.fetchall()

    if not result:
        print("No expenses found")
        return

    print("\nCategory-wise Summary:")
    for row in result:
        print(f"{row[0]} : {row[1]}")

#Function for monthly summary
def monthly_summary():
    cursor.execute(
        "SELECT strftime('%Y-%m', date), SUM(amount) FROM expenses GROUP BY strftime('%Y-%m', date)"
    )
    result = cursor.fetchall()

    if not result:
        print("No expenses found")
        return

    print("\nMonthly Summary:")
    for row in result:
        print(f"{row[0]} : {row[1]}")

#GRAPH
import matplotlib.pyplot as plt

def monthly_expense_graph():
    cursor.execute(
        "SELECT strftime('%Y-%m', date), SUM(amount) FROM expenses GROUP BY strftime('%Y-%m', date)"
    )
    result = cursor.fetchall()

    if not result:
        print("No expenses found")
        return

    months = []
    amounts = []

    for row in result:
        months.append(row[0])
        amounts.append(row[1])

    plt.bar(months, amounts)
    plt.xlabel("Month")
    plt.ylabel("Total Expense")
    plt.title("Monthly Expense Summary")
    plt.show()

#Total expenses
def total_expense():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    result = cursor.fetchone()

    if result[0] is None:
        print("No expenses found.")
    else:
        print(f"\nTotal Expense = ₹ {result[0]}")

#delete all
def delete_all_expenses():
    confirm = input("Are you sure you want to delete ALL expenses? (yes/no): ")

    if confirm.lower() != "yes":
        print("Operation cancelled")
        return

    cursor.execute("DELETE FROM expenses")
    conn.commit()
    print("All expenses deleted successfully!")



# Main menu
while True:
    print("\n==== EXPENSE TRACKER ====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Update Expense")
    print("5. Category Summary")
    print("6. Monthly Summary")
    print("7. Monthly Expense Graph")
    print("8. View Total expense")
    print("9. Delete All")
    print("10. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        delete_expense()
    elif choice == "4":
        update_expense()
    elif choice=="5":
        category_summary()
    elif choice=="6":
        monthly_summary()
    elif choice=="7":
        monthly_expense_graph()
    elif choice=="8":
        total_expense()
    elif choice=="9":
        delete_all_expenses()
    elif choice=="10":
        print("Goodbye")
        break
    else:
        print("Invalid choice! Try again.")
