"""
Setup Chart of Accounts for Mohi Industries ERP
Creates all necessary accounts for a complete ERP system
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from app.models.accounting import Account
from datetime import datetime

def setup_chart_of_accounts():
    """Create complete chart of accounts"""
    
    app = create_app()
    with app.app_context():
        # Check if accounts already exist
        existing = Account.query.count()
        if existing > 0:
            print(f"Found {existing} existing accounts. Skipping to avoid duplicates.")
            print("   Delete existing accounts first if you want to recreate them.")
            return
        
        accounts = [
            # ==================== ASSETS ====================
            # Current Assets
            {'name': 'Cash', 'account_number': 'CASH', 'root_type': 'Asset', 'account_type': 'Cash', 'is_group': False},
            {'name': 'Bank Account', 'account_number': 'BANK', 'root_type': 'Asset', 'account_type': 'Bank', 'is_group': False},
            {'name': 'Petty Cash', 'account_number': 'PETTY', 'root_type': 'Asset', 'account_type': 'Cash', 'is_group': False},
            {'name': 'Accounts Receivable', 'account_number': 'AR', 'root_type': 'Asset', 'account_type': 'Receivable', 'is_group': False},
            {'name': 'Inventory', 'account_number': 'INV', 'root_type': 'Asset', 'account_type': 'Stock', 'is_group': False},
            {'name': 'Prepaid Expenses', 'account_number': 'PREPAID', 'root_type': 'Asset', 'account_type': 'Prepaid', 'is_group': False},
            
            # Fixed Assets
            {'name': 'Furniture & Fixtures', 'account_number': 'FURN', 'root_type': 'Asset', 'account_type': 'Fixed Asset', 'is_group': False},
            {'name': 'Vehicles', 'account_number': 'VEH', 'root_type': 'Asset', 'account_type': 'Fixed Asset', 'is_group': False},
            {'name': 'Equipment', 'account_number': 'EQUIP', 'root_type': 'Asset', 'account_type': 'Fixed Asset', 'is_group': False},
            {'name': 'Computers', 'account_number': 'COMP', 'root_type': 'Asset', 'account_type': 'Fixed Asset', 'is_group': False},
            {'name': 'Accumulated Depreciation', 'account_number': 'DEPR', 'root_type': 'Asset', 'account_type': 'Accumulated Depreciation', 'is_group': False},
            
            # ==================== LIABILITIES ====================
            # Current Liabilities
            {'name': 'Accounts Payable', 'account_number': 'AP', 'root_type': 'Liability', 'account_type': 'Payable', 'is_group': False},
            {'name': 'GST Output', 'account_number': 'GST-OUT', 'root_type': 'Liability', 'account_type': 'Tax', 'is_group': False},
            {'name': 'GST Input', 'account_number': 'GST-IN', 'root_type': 'Asset', 'account_type': 'Tax', 'is_group': False},
            {'name': 'TDS Payable', 'account_number': 'TDS', 'root_type': 'Liability', 'account_type': 'Tax', 'is_group': False},
            {'name': 'Salary Payable', 'account_number': 'SAL-PAY', 'root_type': 'Liability', 'account_type': 'Payable', 'is_group': False},
            {'name': 'Short Term Loan', 'account_number': 'STL', 'root_type': 'Liability', 'account_type': 'Loan', 'is_group': False},
            
            # Long Term Liabilities
            {'name': 'Long Term Loan', 'account_number': 'LTL', 'root_type': 'Liability', 'account_type': 'Loan', 'is_group': False},
            
            # ==================== EQUITY ====================
            {'name': 'Capital', 'account_number': 'CAP', 'root_type': 'Equity', 'account_type': 'Capital', 'is_group': False},
            {'name': 'Retained Earnings', 'account_number': 'RE', 'root_type': 'Equity', 'account_type': 'Retained Earnings', 'is_group': False},
            {'name': 'Drawings', 'account_number': 'DRAW', 'root_type': 'Equity', 'account_type': 'Drawings', 'is_group': False},
            
            # ==================== INCOME ====================
            {'name': 'Sales Revenue', 'account_number': 'SALES', 'root_type': 'Income', 'account_type': 'Sales', 'is_group': False},
            {'name': 'Service Revenue', 'account_number': 'SERVICE', 'root_type': 'Income', 'account_type': 'Service', 'is_group': False},
            {'name': 'Interest Income', 'account_number': 'INT-IN', 'root_type': 'Income', 'account_type': 'Interest', 'is_group': False},
            {'name': 'Other Income', 'account_number': 'OTHER-IN', 'root_type': 'Income', 'account_type': 'Other', 'is_group': False},
            {'name': 'Discount Received', 'account_number': 'DISC-IN', 'root_type': 'Income', 'account_type': 'Discount', 'is_group': False},
            
            # ==================== EXPENSES ====================
            # Operating Expenses
            {'name': 'Cost of Goods Sold', 'account_number': 'COGS', 'root_type': 'Expense', 'account_type': 'Cost of Goods Sold', 'is_group': False},
            {'name': 'Salary Expense', 'account_number': 'SAL', 'root_type': 'Expense', 'account_type': 'Salary', 'is_group': False},
            {'name': 'Rent Expense', 'account_number': 'RENT', 'root_type': 'Expense', 'account_type': 'Rent', 'is_group': False},
            {'name': 'Electricity Expense', 'account_number': 'ELEC', 'root_type': 'Expense', 'account_type': 'Utilities', 'is_group': False},
            {'name': 'Water Expense', 'account_number': 'WATER', 'root_type': 'Expense', 'account_type': 'Utilities', 'is_group': False},
            {'name': 'Telephone Expense', 'account_number': 'PHONE', 'root_type': 'Expense', 'account_type': 'Communication', 'is_group': False},
            {'name': 'Internet Expense', 'account_number': 'NET', 'root_type': 'Expense', 'account_type': 'Communication', 'is_group': False},
            {'name': 'Office Supplies', 'account_number': 'SUPPLIES', 'root_type': 'Expense', 'account_type': 'Office', 'is_group': False},
            {'name': 'Printing & Stationery', 'account_number': 'PRINT', 'root_type': 'Expense', 'account_type': 'Office', 'is_group': False},
            
            # Transportation & Vehicle
            {'name': 'Fuel Expense', 'account_number': 'FUEL', 'root_type': 'Expense', 'account_type': 'Transportation', 'is_group': False},
            {'name': 'Vehicle Maintenance', 'account_number': 'VEH-MAINT', 'root_type': 'Expense', 'account_type': 'Transportation', 'is_group': False},
            {'name': 'Transportation Expense', 'account_number': 'TRANS', 'root_type': 'Expense', 'account_type': 'Transportation', 'is_group': False},
            {'name': 'Freight & Delivery', 'account_number': 'FREIGHT', 'root_type': 'Expense', 'account_type': 'Transportation', 'is_group': False},
            
            # Marketing & Sales
            {'name': 'Advertising Expense', 'account_number': 'ADV', 'root_type': 'Expense', 'account_type': 'Marketing', 'is_group': False},
            {'name': 'Marketing Expense', 'account_number': 'MKTG', 'root_type': 'Expense', 'account_type': 'Marketing', 'is_group': False},
            {'name': 'Sales Commission', 'account_number': 'COMM', 'root_type': 'Expense', 'account_type': 'Sales', 'is_group': False},
            
            # Professional Services
            {'name': 'Legal & Professional Fees', 'account_number': 'LEGAL', 'root_type': 'Expense', 'account_type': 'Professional', 'is_group': False},
            {'name': 'Accounting Fees', 'account_number': 'ACCT-FEE', 'root_type': 'Expense', 'account_type': 'Professional', 'is_group': False},
            {'name': 'Consulting Fees', 'account_number': 'CONSULT', 'root_type': 'Expense', 'account_type': 'Professional', 'is_group': False},
            
            # Maintenance & Repairs
            {'name': 'Repairs & Maintenance', 'account_number': 'REPAIR', 'root_type': 'Expense', 'account_type': 'Maintenance', 'is_group': False},
            {'name': 'Building Maintenance', 'account_number': 'BLDG-MAINT', 'root_type': 'Expense', 'account_type': 'Maintenance', 'is_group': False},
            
            # Insurance
            {'name': 'Insurance Expense', 'account_number': 'INS', 'root_type': 'Expense', 'account_type': 'Insurance', 'is_group': False},
            
            # Bank & Finance
            {'name': 'Bank Charges', 'account_number': 'BANK-CHG', 'root_type': 'Expense', 'account_type': 'Bank', 'is_group': False},
            {'name': 'Interest Expense', 'account_number': 'INT-EXP', 'root_type': 'Expense', 'account_type': 'Interest', 'is_group': False},
            {'name': 'Loan Processing Fees', 'account_number': 'LOAN-FEE', 'root_type': 'Expense', 'account_type': 'Bank', 'is_group': False},
            
            # Depreciation
            {'name': 'Depreciation Expense', 'account_number': 'DEPR-EXP', 'root_type': 'Expense', 'account_type': 'Depreciation', 'is_group': False},
            
            # Taxes
            {'name': 'Income Tax Expense', 'account_number': 'TAX', 'root_type': 'Expense', 'account_type': 'Tax', 'is_group': False},
            {'name': 'Property Tax', 'account_number': 'PROP-TAX', 'root_type': 'Expense', 'account_type': 'Tax', 'is_group': False},
            
            # Other Expenses
            {'name': 'Miscellaneous Expense', 'account_number': 'MISC', 'root_type': 'Expense', 'account_type': 'Other', 'is_group': False},
            {'name': 'Bad Debts', 'account_number': 'BAD-DEBT', 'root_type': 'Expense', 'account_type': 'Other', 'is_group': False},
            {'name': 'Discount Given', 'account_number': 'DISC-OUT', 'root_type': 'Expense', 'account_type': 'Discount', 'is_group': False},
            {'name': 'Penalties & Fines', 'account_number': 'PENALTY', 'root_type': 'Expense', 'account_type': 'Other', 'is_group': False},
            
            # Employee Benefits
            {'name': 'Employee Benefits', 'account_number': 'EMP-BEN', 'root_type': 'Expense', 'account_type': 'Salary', 'is_group': False},
            {'name': 'Staff Welfare', 'account_number': 'WELFARE', 'root_type': 'Expense', 'account_type': 'Salary', 'is_group': False},
            {'name': 'Training & Development', 'account_number': 'TRAIN', 'root_type': 'Expense', 'account_type': 'Salary', 'is_group': False},
            
            # Travel & Entertainment
            {'name': 'Travel Expense', 'account_number': 'TRAVEL', 'root_type': 'Expense', 'account_type': 'Travel', 'is_group': False},
            {'name': 'Hotel & Accommodation', 'account_number': 'HOTEL', 'root_type': 'Expense', 'account_type': 'Travel', 'is_group': False},
            {'name': 'Meals & Entertainment', 'account_number': 'MEALS', 'root_type': 'Expense', 'account_type': 'Entertainment', 'is_group': False},
        ]
        
        print("Creating Chart of Accounts...")
        print("=" * 60)
        
        created_count = 0
        for acc_data in accounts:
            try:
                account = Account(
                    name=acc_data['name'],
                    account_number=acc_data['account_number'],
                    root_type=acc_data['root_type'],
                    account_type=acc_data.get('account_type'),
                    is_group=acc_data.get('is_group', False),
                    is_active=True,
                    description=f"{acc_data['root_type']} - {acc_data['name']}"
                )
                db.session.add(account)
                created_count += 1
                print(f"OK  {acc_data['root_type']:12} | {acc_data['account_number']:12} | {acc_data['name']}")
            except Exception as e:
                print(f"ERROR creating {acc_data['name']}: {str(e)}")
        
        db.session.commit()
        
        print("=" * 60)
        print(f"Successfully created {created_count} accounts.")
        print("\nSummary:")
        
        # Count by type
        for root_type in ['Asset', 'Liability', 'Equity', 'Income', 'Expense']:
            count = Account.query.filter_by(root_type=root_type).count()
            print(f"   {root_type:12}: {count:3} accounts")
        
        print("\nChart of Accounts setup complete.")
        print("   You can now record expenses and manage accounting.")

if __name__ == '__main__':
    setup_chart_of_accounts()
