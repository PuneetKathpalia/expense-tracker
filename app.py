from sqlalchemy import create_engine, Column, Integer, String, Float, Date, func
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Database Setup
# Using SQLite with SQLAlchemy ORM to manage expenses and budgets
Base = declarative_base()
engine = create_engine('sqlite:///expenses.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


# --- Database Models ---

class Expense(Base):
    """Table to store user expenses"""
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    category = Column(String)      # Example: Food, Transport, Entertainment
    amount = Column(Float)         # Expense amount
    date = Column(Date)            # Date of the expense


class Budget(Base):
    """Table to store monthly budgets for each category"""
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True)
    category = Column(String)      # Category name
    month = Column(String)         # Month in format YYYY-MM
    amount = Column(Float)         # Budget limit for that month/category


# Create tables if they don't exist
Base.metadata.create_all(engine)
print("Database connected")


# Functions for App Features 

def set_budget():
    """Set or update a budget for a category in a given month"""
    category = input("Enter category: ").strip()
    month = input("Enter month (YYYY-MM): ").strip()
    amount = float(input("Enter budget amount: "))

    # Check if budget already exists for this category + month
    budget = session.query(Budget).filter_by(category=category, month=month).first()
    if budget:
        budget.amount = amount  # Update if exists
    else:
        budget = Budget(category=category, month=month, amount=amount)
        session.add(budget)     # Create new budget entry
    session.commit()
    print(f"Budget set for {category} in {month}: {amount}")


def add_expense():
    """Add a new expense record"""
    category = input("Enter category: ").strip()
    amount = float(input("Enter expense amount: "))
    date_str = input("Enter date (YYYY-MM-DD, leave empty for today): ").strip()

    # If no date given, use today's date
    date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.today().date()

    # Create and save expense record
    expense = Expense(category=category, amount=amount, date=date)
    session.add(expense)
    session.commit()
    print(f"Expense added: {amount} for {category} on {date}")


def check_budget_alert():
    """Check if spending in a category for a given month is within budget or not """
    month = input("Enter month (YYYY-MM): ").strip()
    category = input("Enter category: ").strip()

    # Find budget record
    budget = session.query(Budget).filter_by(category=category, month=month).first()
    if not budget:
        print(f"No budget found for {category} in {month}")
        return

# Calculate total spent in that category + month
    total_spent = session.query(func.sum(Expense.amount)).filter(
        func.strftime('%Y-%m', Expense.date) == month,
        Expense.category == category
    ).scalar() or 0

    print(f"{category} budget: {budget.amount}, spent: {total_spent}")

    # Alerts
    if total_spent > budget.amount:
        print("Budget exceeded!")
    elif total_spent >= 0.9 * budget.amount:
        print("Warning: You have spent 90% of your budget.")


def monthly_report():
    """Show report of expenses per category for a given month"""
    month = input("Enter month (YYYY-MM): ").strip()
    expenses = session.query(Expense.category, func.sum(Expense.amount)).filter(
        func.strftime('%Y-%m', Expense.date) == month
    ).group_by(Expense.category).all()

    print(f"Expense report for {month}:")
    for cat, total in expenses:
        budget = session.query(Budget).filter_by(category=cat, month=month).first()
        budget_amt = budget.amount if budget else 0
        print(f"{cat}: Spent {total}, Budget {budget_amt}")

# Main Menu
while True:
    print("\n==== Expense Tracker Menu ====")
    print("1. Set Budget")
    print("2. Add Expense")
    print("3. Check Budget Alert")
    print("4. Monthly Report")
    print("5. Exit")

    choice = input("Choose an option (1-5): ").strip()

    if choice == '1':
        set_budget()
    elif choice == '2':
        add_expense()
    elif choice == '3':
        check_budget_alert()
    elif choice == '4':
        monthly_report()
    elif choice == '5':
        print("BYE bye")
        break
    else:
        print("Invalid choice, please try again.")
