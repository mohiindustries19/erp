#!/usr/bin/env python3
"""
Simple Accounting Initialization - Direct DB approach
"""
import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import db
from app.models.accounting import Account, AccountingSettings, FiscalYear
from datetime import date
from flask import Flask
from config import Config

def create_simple_app():
    """Create minimal Flask app for initialization"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def init_accounting():
    """Initialize accounting system"""
    app = create_simple_app()
    
    with app.app_context():
        print("\nInitializing Accounting System...\n")
        
        # Create tables
        db.create_all()
        print("Tables created")
        
        # Check if already exists
        if Account.query.first():
            print("Accounts already exist. Skipping...")
            return
        
        print("Creating Chart of Accounts...")
        
        # Create root accounts
        assets = Account(name='Assets', root_type='Asset', is_group=True, lft=1, rgt=20)
        liabilities = Account(name='Liabilities', root_type='Liability', is_group=True, lft=21, rgt=40)
        equity = Account(name='Equity', root_type='Equity', is_group=True, lft=41, rgt=50)
        income = Account(name='Income', root_type='Income', is_group=True, lft=51, rgt=60)
        expense = Account(name='Expense', root_type='Expense', is_group=True, lft=61, rgt=80)
        
        db.session.add_all([assets, liabilities, equity, income, expense])
        db.session.flush()
        
        # Create essential accounts
        cash = Account(name='Cash in Hand', root_type='Asset', account_type='Cash', 
                      parent_account=assets, account_number='1001')
        bank = Account(name='HDFC Bank', root_type='Asset', account_type='Bank',
                      parent_account=assets, account_number='1002')
        debtors = Account(name='Debtors', root_type='Asset', account_type='Receivable',
                         parent_account=assets, account_number='1003')
        
        creditors = Account(name='Creditors', root_type='Liability', account_type='Payable',
                           parent_account=liabilities, account_number='2001')
        gst_output = Account(name='GST Output', root_type='Liability', account_type='Tax',
                            parent_account=liabilities, account_number='2002')
        gst_input = Account(name='GST Input', root_type='Asset', account_type='Tax',
                           parent_account=assets, account_number='1004')
        
        capital = Account(name='Capital Account', root_type='Equity', account_type='Equity',
                         parent_account=equity, account_number='3001')
        
        sales = Account(name='Sales', root_type='Income', account_type='Income Account',
                       parent_account=income, account_number='4001')
        
        cogs = Account(name='Cost of Goods Sold', root_type='Expense', account_type='Cost of Goods Sold',
                      parent_account=expense, account_number='5001')
        
        db.session.add_all([cash, bank, debtors, creditors, gst_output, gst_input, 
                           capital, sales, cogs])
        db.session.commit()
        
        print(f"Created {Account.query.count()} accounts")
        
        # Create settings
        settings = AccountingSettings(
            setup_complete=True,
            default_cash_account=cash,
            default_bank_account=bank,
            default_receivable_account=debtors,
            default_payable_account=creditors,
            default_income_account=sales,
            default_expense_account=cogs,
            gst_output_account=gst_output,
            gst_input_account=gst_input
        )
        db.session.add(settings)
        
        # Create fiscal year
        current_year = date.today().year
        if date.today().month < 4:
            current_year -= 1
        
        fy = FiscalYear(
            name=f'FY {current_year}-{current_year + 1}',
            start_date=date(current_year, 4, 1),
            end_date=date(current_year + 1, 3, 31),
            is_active=True
        )
        db.session.add(fy)
        db.session.commit()
        
        print(f"Fiscal Year: {fy.name}")
        print("\nAccounting System Initialized Successfully.\n")

if __name__ == '__main__':
    init_accounting()
