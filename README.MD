# Expense Tracker (Python + SQLite + SQLAlchemy)

A simple Python app to track daily expenses and set monthly budgets.  
It runs in the terminal and uses SQLite as the database.

## Features
- Add expenses (category, amount, date)  
- Set monthly budgets per category  
- Alerts when spending crosses 90% or exceeds budget  
- View monthly spending reports  

## Installation

git clone <repo-link>
cd expense-tracker
pip install -r requirements.txt
python app.py

## Run with Docker
docker build -t expense-tracker .
docker run -it expense-tracker

##Example Usage
- Set a budget → Option 1
- Add an expense → Option 2
- Check alerts → Option 3
- View report → Option 4

## Technologies

-- Python 3.11
-- SQLite
-- SQLAlchemy
-- Docker