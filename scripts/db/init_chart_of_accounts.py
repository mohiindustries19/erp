"""
Initialize Chart of Accounts with Standard Indian Accounting Heads
Run this after database initialization
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from app.models.accounting import ChartOfAccounts

def init_chart_of_accounts():
    """Initialize standard Chart of Accounts for Indian FMCG business"""
    
    accounts = [
        # ==================== ASSETS ====================
        # Current Assets
        {'code': 'CASH', 'name': 'Cash in Hand', 'type': 'asset', 'group': 'Current Assets', 'opening': 0.0},
        {'code': 'BANK', 'name': 'Bank Account - Current', 'type': 'asset', 'group': 'Current Assets', 'opening': 0.0},
        {'code': 'AR', 'name': 'Accounts Receivable (Debtors)', 'type': 'asset', 'group': 'Current Assets', 'opening': 0.0},
        {'code': 'INV', 'name': 'Inventory - Raw Materials', 'type': 'asset', 'group': 'Current Assets', 'opening': 0.0},
        {'code': 'INV-FG', 'name': 'Inventory - Finished Goods', 'type': 'asset', 'group': 'Current Assets', 'opening': 0.0},
        {'code': 'INV-PKG', 'name': 'Inventory - Packaging Materials', 'type': 'asset', 'group': 'Current Assets', 'opening': 0.0},
        {'code': 'GST-ITC', 'name': 'GST Input Tax Credit', 'type': 'asset', 'group': 'Current Assets', 'opening': 0.0},
        {'code': 'TDS-REC', 'name': 'TDS Receivable', 'type': 'asset', 'group': 'Current Assets', 'opening': 0.0},
        
        # Fixed Assets
        {'code': 'LAND', 'name': 'Land & Building', 'type': 'asset', 'group': 'Fixed Assets', 'opening': 0.0},
        {'code': 'PLANT', 'name': 'Plant & Machinery', 'type': 'asset', 'group': 'Fixed Assets', 'opening': 0.0},
        {'code': 'VEHICLE', 'name': 'Vehicles', 'type': 'asset', 'group': 'Fixed Assets', 'opening': 0.0},
        {'code': 'FURNITURE', 'name': 'Furniture & Fixtures', 'type': 'asset', 'group': 'Fixed Assets', 'opening': 0.0},
        {'code': 'COMPUTER', 'name': 'Computers & IT Equipment', 'type': 'asset', 'group': 'Fixed Assets', 'opening': 0.0},
        
        # ==================== LIABILITIES ====================
        # Current Liabilities
        {'code': 'AP', 'name': 'Accounts Payable (Creditors)', 'type': 'liability', 'group': 'Current Liabilities', 'opening': 0.0},
        {'code': 'GST-OUT', 'name': 'GST Output Tax Payable', 'type': 'liability', 'group': 'Current Liabilities', 'opening': 0.0},
        {'code': 'TDS-PAY', 'name': 'TDS Payable', 'type': 'liability', 'group': 'Current Liabilities', 'opening': 0.0},
        {'code': 'SAL-PAY', 'name': 'Salary Payable', 'type': 'liability', 'group': 'Current Liabilities', 'opening': 0.0},
        {'code': 'PF-PAY', 'name': 'PF Payable', 'type': 'liability', 'group': 'Current Liabilities', 'opening': 0.0},
        {'code': 'ESI-PAY', 'name': 'ESI Payable', 'type': 'liability', 'group': 'Current Liabilities', 'opening': 0.0},
        
        # Long-term Liabilities
        {'code': 'LOAN-BANK', 'name': 'Bank Loan', 'type': 'liability', 'group': 'Long-term Liabilities', 'opening': 0.0},
        {'code': 'LOAN-OTHER', 'name': 'Other Loans', 'type': 'liability', 'group': 'Long-term Liabilities', 'opening': 0.0},
        
        # ==================== EQUITY ====================
        {'code': 'CAPITAL', 'name': 'Owner\'s Capital', 'type': 'equity', 'group': 'Equity', 'opening': 0.0},
        {'code': 'RETAINED', 'name': 'Retained Earnings', 'type': 'equity', 'group': 'Equity', 'opening': 0.0},
        {'code': 'DRAWINGS', 'name': 'Owner\'s Drawings', 'type': 'equity', 'group': 'Equity', 'opening': 0.0},
        
        # ==================== INCOME ====================
        # Direct Income
        {'code': 'SALES-BAK', 'name': 'Sales - Bakery Products', 'type': 'income', 'group': 'Direct Income', 'opening': 0.0, 'gst': True, 'gst_rate': 5.0},
        {'code': 'SALES-PKL', 'name': 'Sales - Pickles', 'type': 'income', 'group': 'Direct Income', 'opening': 0.0, 'gst': True, 'gst_rate': 12.0},
        {'code': 'SALES-WTR', 'name': 'Sales - Mohi Neer Water', 'type': 'income', 'group': 'Direct Income', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'SALES-OTHER', 'name': 'Sales - Other Products', 'type': 'income', 'group': 'Direct Income', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        
        # Indirect Income
        {'code': 'INT-INC', 'name': 'Interest Income', 'type': 'income', 'group': 'Indirect Income', 'opening': 0.0},
        {'code': 'OTHER-INC', 'name': 'Other Income', 'type': 'income', 'group': 'Indirect Income', 'opening': 0.0},
        {'code': 'DISC-REC', 'name': 'Discount Received', 'type': 'income', 'group': 'Indirect Income', 'opening': 0.0},
        
        # ==================== EXPENSES ====================
        # Direct Expenses (Cost of Goods Sold)
        {'code': 'PUR-RM', 'name': 'Purchase - Raw Materials', 'type': 'expense', 'group': 'Direct Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 5.0},
        {'code': 'PUR-PKG', 'name': 'Purchase - Packaging Materials', 'type': 'expense', 'group': 'Direct Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'FREIGHT-IN', 'name': 'Freight Inward', 'type': 'expense', 'group': 'Direct Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'LABOUR-DIR', 'name': 'Direct Labour', 'type': 'expense', 'group': 'Direct Expenses', 'opening': 0.0},
        {'code': 'FACTORY-EXP', 'name': 'Factory Expenses', 'type': 'expense', 'group': 'Direct Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        
        # Indirect Expenses (Operating Expenses)
        {'code': 'SAL-ADMIN', 'name': 'Salary - Administrative Staff', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0},
        {'code': 'SAL-SALES', 'name': 'Salary - Sales Staff', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0},
        {'code': 'RENT', 'name': 'Rent Expense', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'ELECTRICITY', 'name': 'Electricity Charges', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'WATER', 'name': 'Water Charges', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'TELEPHONE', 'name': 'Telephone & Internet', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'FUEL', 'name': 'Fuel & Vehicle Expenses', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'REPAIR', 'name': 'Repairs & Maintenance', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'INSURANCE', 'name': 'Insurance', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'LEGAL', 'name': 'Legal & Professional Fees', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'AUDIT', 'name': 'Audit Fees', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'STATIONERY', 'name': 'Stationery & Printing', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'ADVERTISING', 'name': 'Advertising & Marketing', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'FREIGHT-OUT', 'name': 'Freight Outward', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'BANK-CHARGES', 'name': 'Bank Charges', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
        {'code': 'INT-EXP', 'name': 'Interest Expense', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0},
        {'code': 'DEPRECIATION', 'name': 'Depreciation', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0},
        {'code': 'MISC-EXP', 'name': 'Miscellaneous Expenses', 'type': 'expense', 'group': 'Indirect Expenses', 'opening': 0.0, 'gst': True, 'gst_rate': 18.0},
    ]
    
    print("Initializing Chart of Accounts...")
    
    for acc_data in accounts:
        # Check if account already exists
        existing = ChartOfAccounts.query.filter_by(account_code=acc_data['code']).first()
        if existing:
            print(f"  Account {acc_data['code']} already exists, skipping...")
            continue
        
        account = ChartOfAccounts(
            account_code=acc_data['code'],
            account_name=acc_data['name'],
            account_type=acc_data['type'],
            account_group=acc_data['group'],
            opening_balance=acc_data['opening'],
            current_balance=acc_data['opening'],
            is_gst_applicable=acc_data.get('gst', False),
            gst_rate=acc_data.get('gst_rate', 0.0),
            is_active=True
        )
        
        db.session.add(account)
        print(f"  Created: {acc_data['code']} - {acc_data['name']}")
    
    db.session.commit()
    print("\nChart of Accounts initialized successfully.")
    print(f"Total accounts created: {len(accounts)}")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        init_chart_of_accounts()
