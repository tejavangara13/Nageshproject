import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

class FinanceManager:
    def __init__(self, db_name="finance.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT CHECK(type IN ('Income', 'Expense')),
            category TEXT,
            amount REAL,
            date DATE DEFAULT (DATE('now'))
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_transaction(self, t_type, category, amount):
        self.conn.execute(
            "INSERT INTO transactions (type, category, amount) VALUES (?, ?, ?)",
            (t_type, category.capitalize(), float(amount))
        )
        self.conn.commit()
        print(f"Added {t_type}: {category} - ${amount:.2f}")

    def get_summary(self):
        df = pd.read_sql_query("SELECT * FROM transactions", self.conn)
        if df.empty:
            print("No transactions recorded yet.")
            return

        total_income = df[df['type'] == 'Income']['amount'].sum()
        total_expense = df[df['type'] == 'Expense']['amount'].sum()
        savings = total_income - total_expense

        print("\n" + "="*35)
        print("        FINANCIAL SUMMARY")
        print("="*35)
        print(f"Total Income   : ${total_income:,.2f}")
        print(f"Total Expenses : ${total_expense:,.2f}")
        print(f"Net Savings    : ${savings:,.2f}")

        # Recommendations based on 50/30/20 rule
        print("\n--- Recommendations ---")
        if total_income > 0:
            savings_rate = (savings / total_income) * 100
            print(f"Current Savings Rate: {savings_rate:.1f}%")
            if savings_rate < 20:
                print(" Warning: Your savings are below the suggested 20% mark. Review your expenses!")
            else:
                print(" Great job! You are maintaining a healthy savings rate.")
        print("="*35 + "\n")

    def plot_expenses(self):
        df = pd.read_sql_query("SELECT * FROM transactions WHERE type='Expense'", self.conn)
        if df.empty:
            print("No expenses to plot.")
            return

        category_data = df.groupby('category')['amount'].sum()
        plt.figure(figsize=(6, 6))
        category_data.plot(kind='pie', autopct='%1.1f%%', startangle=140)
        plt.title("Expense Breakdown by Category")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    manager = FinanceManager()
    
    # Adding demo transactions
    manager.add_transaction("Income", "Salary", 3000.00)
    manager.add_transaction("Income", "Freelancing", 500.00)
    manager.add_transaction("Expense", "Rent", 900.00)
    manager.add_transaction("Expense", "Groceries", 350.00)
    manager.add_transaction("Expense", "Utilities", 150.00)
    manager.add_transaction("Expense", "Entertainment", 200.00)
    
    # View summary & chart
    manager.get_summary()
    manager.plot_expenses()