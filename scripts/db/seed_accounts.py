"""Seed default chart of accounts"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from app.models.accounting import Account

app = create_app()

with app.app_context():
    # Check if accounts exist
    if Account.query.count() > 0:
        print('Accounts already exist, skipping...')
    else:
        accounts_data = [
            # Assets
            {'name': 'Cash', 'account_number': '1001', 'root_type': 'Asset', 'account_type': 'Cash'},
            {'name': 'Bank', 'account_number': '1002', 'root_type': 'Asset', 'account_type': 'Bank'},
            {'name': 'Accounts Receivable', 'account_number': '1100', 'root_type': 'Asset', 'account_type': 'Receivable'},
            {'name': 'Inventory', 'account_number': '1200', 'root_type': 'Asset', 'account_type': 'Stock'},
            
            # Liabilities
            {'name': 'Accounts Payable', 'account_number': '2000', 'root_type': 'Liability', 'account_type': 'Payable'},
            {'name': 'GST Payable', 'account_number': '2100', 'root_type': 'Liability', 'account_type': 'Tax'},
            
            # Equity
            {'name': 'Capital', 'account_number': '3000', 'root_type': 'Equity', 'account_type': 'Equity'},
            {'name': 'Retained Earnings', 'account_number': '3100', 'root_type': 'Equity', 'account_type': 'Equity'},
            
            # Income
            {'name': 'Sales Revenue', 'account_number': '4000', 'root_type': 'Income', 'account_type': 'Income'},
            {'name': 'Other Income', 'account_number': '4100', 'root_type': 'Income', 'account_type': 'Income'},
            
            # Expenses
            {'name': 'Cost of Goods Sold', 'account_number': '5000', 'root_type': 'Expense', 'account_type': 'Cost of Goods Sold'},
            {'name': 'Salaries and Wages', 'account_number': '5100', 'root_type': 'Expense', 'account_type': 'Expense'},
            {'name': 'Rent Expense', 'account_number': '5200', 'root_type': 'Expense', 'account_type': 'Expense'},
            {'name': 'Utilities', 'account_number': '5300', 'root_type': 'Expense', 'account_type': 'Expense'},
            {'name': 'Office Supplies', 'account_number': '5400', 'root_type': 'Expense', 'account_type': 'Expense'},
            {'name': 'Transport Expense', 'account_number': '5500', 'root_type': 'Expense', 'account_type': 'Expense'},
            {'name': 'Marketing Expense', 'account_number': '5600', 'root_type': 'Expense', 'account_type': 'Expense'},
            {'name': 'Maintenance Expense', 'account_number': '5700', 'root_type': 'Expense', 'account_type': 'Expense'},
            {'name': 'Miscellaneous Expense', 'account_number': '5900', 'root_type': 'Expense', 'account_type': 'Expense'},
        ]

        for data in accounts_data:
            acc = Account(**data, is_active=True)
            db.session.add(acc)

        db.session.commit()
        print(f'Created {len(accounts_data)} accounts successfully!')
