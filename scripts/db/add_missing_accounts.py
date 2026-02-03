"""
Add missing accounts to existing Chart of Accounts
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from app.models.accounting import Account

def add_missing_accounts():
    """Add accounts that don't exist yet"""
    
    app = create_app()
    with app.app_context():
        # First, show existing accounts
        existing = Account.query.all()
        print(f"Existing Accounts ({len(existing)}):")
        print("=" * 60)
        for acc in existing:
            print(f"   {acc.root_type:12} | {acc.account_number or 'N/A':12} | {acc.name}")
        print("=" * 60)
        
        # Define all necessary accounts
        all_accounts = [
            # EXPENSES - Most important for your use case
            {'name': 'Cost of Goods Sold', 'account_number': 'COGS', 'root_type': 'Expense', 'account_type': 'Cost of Goods Sold'},
            {'name': 'Salary Expense', 'account_number': 'SAL', 'root_type': 'Expense', 'account_type': 'Salary'},
            {'name': 'Rent Expense', 'account_number': 'RENT', 'root_type': 'Expense', 'account_type': 'Rent'},
            {'name': 'Electricity Expense', 'account_number': 'ELEC', 'root_type': 'Expense', 'account_type': 'Utilities'},
            {'name': 'Water Expense', 'account_number': 'WATER', 'root_type': 'Expense', 'account_type': 'Utilities'},
            {'name': 'Telephone Expense', 'account_number': 'PHONE', 'root_type': 'Expense', 'account_type': 'Communication'},
            {'name': 'Internet Expense', 'account_number': 'NET', 'root_type': 'Expense', 'account_type': 'Communication'},
            {'name': 'Office Supplies', 'account_number': 'SUPPLIES', 'root_type': 'Expense', 'account_type': 'Office'},
            {'name': 'Printing & Stationery', 'account_number': 'PRINT', 'root_type': 'Expense', 'account_type': 'Office'},
            {'name': 'Fuel Expense', 'account_number': 'FUEL', 'root_type': 'Expense', 'account_type': 'Transportation'},
            {'name': 'Vehicle Maintenance', 'account_number': 'VEH-MAINT', 'root_type': 'Expense', 'account_type': 'Transportation'},
            {'name': 'Transportation Expense', 'account_number': 'TRANS', 'root_type': 'Expense', 'account_type': 'Transportation'},
            {'name': 'Freight & Delivery', 'account_number': 'FREIGHT', 'root_type': 'Expense', 'account_type': 'Transportation'},
            {'name': 'Advertising Expense', 'account_number': 'ADV', 'root_type': 'Expense', 'account_type': 'Marketing'},
            {'name': 'Marketing Expense', 'account_number': 'MKTG', 'root_type': 'Expense', 'account_type': 'Marketing'},
            {'name': 'Sales Commission', 'account_number': 'COMM', 'root_type': 'Expense', 'account_type': 'Sales'},
            {'name': 'Legal & Professional Fees', 'account_number': 'LEGAL', 'root_type': 'Expense', 'account_type': 'Professional'},
            {'name': 'Accounting Fees', 'account_number': 'ACCT-FEE', 'root_type': 'Expense', 'account_type': 'Professional'},
            {'name': 'Consulting Fees', 'account_number': 'CONSULT', 'root_type': 'Expense', 'account_type': 'Professional'},
            {'name': 'Repairs & Maintenance', 'account_number': 'REPAIR', 'root_type': 'Expense', 'account_type': 'Maintenance'},
            {'name': 'Building Maintenance', 'account_number': 'BLDG-MAINT', 'root_type': 'Expense', 'account_type': 'Maintenance'},
            {'name': 'Insurance Expense', 'account_number': 'INS', 'root_type': 'Expense', 'account_type': 'Insurance'},
            {'name': 'Bank Charges', 'account_number': 'BANK-CHG', 'root_type': 'Expense', 'account_type': 'Bank'},
            {'name': 'Interest Expense', 'account_number': 'INT-EXP', 'root_type': 'Expense', 'account_type': 'Interest'},
            {'name': 'Depreciation Expense', 'account_number': 'DEPR-EXP', 'root_type': 'Expense', 'account_type': 'Depreciation'},
            {'name': 'Income Tax Expense', 'account_number': 'TAX', 'root_type': 'Expense', 'account_type': 'Tax'},
            {'name': 'Miscellaneous Expense', 'account_number': 'MISC', 'root_type': 'Expense', 'account_type': 'Other'},
            {'name': 'Bad Debts', 'account_number': 'BAD-DEBT', 'root_type': 'Expense', 'account_type': 'Other'},
            {'name': 'Discount Given', 'account_number': 'DISC-OUT', 'root_type': 'Expense', 'account_type': 'Discount'},
            {'name': 'Travel Expense', 'account_number': 'TRAVEL', 'root_type': 'Expense', 'account_type': 'Travel'},
            {'name': 'Meals & Entertainment', 'account_number': 'MEALS', 'root_type': 'Expense', 'account_type': 'Entertainment'},
            
            # ASSETS
            {'name': 'Petty Cash', 'account_number': 'PETTY', 'root_type': 'Asset', 'account_type': 'Cash'},
            {'name': 'Prepaid Expenses', 'account_number': 'PREPAID', 'root_type': 'Asset', 'account_type': 'Prepaid'},
            {'name': 'Furniture & Fixtures', 'account_number': 'FURN', 'root_type': 'Asset', 'account_type': 'Fixed Asset'},
            {'name': 'Vehicles', 'account_number': 'VEH', 'root_type': 'Asset', 'account_type': 'Fixed Asset'},
            {'name': 'Equipment', 'account_number': 'EQUIP', 'root_type': 'Asset', 'account_type': 'Fixed Asset'},
            {'name': 'Computers', 'account_number': 'COMP', 'root_type': 'Asset', 'account_type': 'Fixed Asset'},
            
            # INCOME
            {'name': 'Service Revenue', 'account_number': 'SERVICE', 'root_type': 'Income', 'account_type': 'Service'},
            {'name': 'Interest Income', 'account_number': 'INT-IN', 'root_type': 'Income', 'account_type': 'Interest'},
            {'name': 'Other Income', 'account_number': 'OTHER-IN', 'root_type': 'Income', 'account_type': 'Other'},
            {'name': 'Discount Received', 'account_number': 'DISC-IN', 'root_type': 'Income', 'account_type': 'Discount'},
            
            # LIABILITIES
            {'name': 'TDS Payable', 'account_number': 'TDS', 'root_type': 'Liability', 'account_type': 'Tax'},
            {'name': 'Salary Payable', 'account_number': 'SAL-PAY', 'root_type': 'Liability', 'account_type': 'Payable'},
            {'name': 'Short Term Loan', 'account_number': 'STL', 'root_type': 'Liability', 'account_type': 'Loan'},
            {'name': 'Long Term Loan', 'account_number': 'LTL', 'root_type': 'Liability', 'account_type': 'Loan'},
            
            # EQUITY
            {'name': 'Retained Earnings', 'account_number': 'RE', 'root_type': 'Equity', 'account_type': 'Retained Earnings'},
            {'name': 'Drawings', 'account_number': 'DRAW', 'root_type': 'Equity', 'account_type': 'Drawings'},
        ]
        
        # Get existing account names
        existing_names = {acc.name.lower() for acc in existing}
        existing_numbers = {acc.account_number.lower() if acc.account_number else None for acc in existing}
        
        # Add missing accounts
        print("\nAdding Missing Accounts...")
        print("=" * 60)
        
        added_count = 0
        for acc_data in all_accounts:
            # Check if account already exists by name or number
            if acc_data['name'].lower() in existing_names:
                continue
            if acc_data['account_number'].lower() in existing_numbers:
                continue
            
            try:
                account = Account(
                    name=acc_data['name'],
                    account_number=acc_data['account_number'],
                    root_type=acc_data['root_type'],
                    account_type=acc_data.get('account_type'),
                    is_group=False,
                    is_active=True,
                    description=f"{acc_data['root_type']} - {acc_data['name']}"
                )
                db.session.add(account)
                added_count += 1
                print(f"OK  {acc_data['root_type']:12} | {acc_data['account_number']:12} | {acc_data['name']}")
            except Exception as e:
                print(f"ERROR creating {acc_data['name']}: {str(e)}")
        
        if added_count > 0:
            db.session.commit()
            print("=" * 60)
            print(f"Successfully added {added_count} new accounts.")
        else:
            print("=" * 60)
            print("No new accounts to add. All accounts already exist.")
        
        # Show final summary
        print("\nFinal Summary:")
        for root_type in ['Asset', 'Liability', 'Equity', 'Income', 'Expense']:
            count = Account.query.filter_by(root_type=root_type).count()
            print(f"   {root_type:12}: {count:3} accounts")
        
        total = Account.query.count()
        print(f"\n   Total: {total} accounts")
        print("\nChart of Accounts is ready.")

if __name__ == '__main__':
    add_missing_accounts()
