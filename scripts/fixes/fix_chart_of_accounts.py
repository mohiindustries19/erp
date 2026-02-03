import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from app.models.accounting import ChartOfAccounts

def fix_accounts():
    app = create_app()
    with app.app_context():
        print("Starting Chart of Accounts Cleanup...")
        
        # 1. Define the Standard Map (Good Accounts)
        # Format: 'Code': ('Name', 'RootType', 'Description')
        standard_accounts = {
            '5100': ('Salaries and Wages', 'Expense', 'Employee salaries, wages, and bonuses'),
            '5200': ('Rent Expense', 'Expense', 'Office and warehouse rent'),
            '5300': ('Utilities', 'Expense', 'Electricity, water, internet, and phone'),
            '5400': ('Office Supplies', 'Expense', 'Stationery, printing, and general supplies'),
            '5500': ('Transport & Travel', 'Expense', 'Fuel, freight, transportation, and travel'),
            '5600': ('Marketing & Advertising', 'Expense', 'Ads, promotions, and sales commissions'),
            '5700': ('Repairs & Maintenance', 'Expense', 'Vehicle, building, and equipment maintenance'),
            '5800': ('Professional Fees', 'Expense', 'Legal, accounting, and consulting fees'),
            '5900': ('Miscellaneous Expense', 'Expense', 'Other minor expenses'),
            '5910': ('Insurance Expense', 'Expense', 'Business insurance premiums'),
            '5920': ('Bank Charges', 'Expense', 'Bank fees and charges'),
            '5930': ('Interest Expense', 'Expense', 'Interest on loans'),
            '5940': ('Taxes & Licenses', 'Expense', 'Business taxes and license fees'),
            '5950': ('Bad Debts', 'Expense', 'Uncollectible receivables'),
        }

        # 2. Ensure Standard Accounts Exist
        print("\nChecking/Creating Standard Numeric Accounts...")
        for code, (name, root_type, desc) in standard_accounts.items():
            account = ChartOfAccounts.query.filter_by(account_number=code).first()
            if not account:
                print(f"  [+] Creating {code} - {name}")
                account = ChartOfAccounts(
                    account_number=code,
                    name=name,
                    root_type=root_type,
                    description=desc,
                    is_active=True
                )
                db.session.add(account)
            else:
                # Ensure name is standardized conform to our list if it's generic
                # But don't overwrite if user has customized it significantly? 
                # For this cleanup, we force standardization for consistency.
                if account.name != name:
                    print(f"  [*] Updating Name: {account.name} -> {name}")
                    account.name = name
                if not account.is_active:
                     print(f"  [^] Reactivating: {code}")
                     account.is_active = True
        
        db.session.commit()

        # 3. Identify and Deactivate Legacy Text Codes
        # We will look for any account where account_number is NOT numeric (and not one of our standard ones just in case)
        print("\nDeactivating Legacy Text-Based Accounts...")
        
        all_accounts = ChartOfAccounts.query.all()
        legacy_count = 0
        
        for acc in all_accounts:
            # Check if code is non-numeric (Text based like 'SAL', 'ELEC')
            # Using simple check: isdigit()
            if acc.account_number and not acc.account_number.isdigit():
                if acc.is_active:
                    print(f"  [-] Deactivating Legacy: {acc.account_number} - {acc.name}")
                    acc.is_active = False
                    # Update name to indicate it's deprecated to avoid confusion in lookups if they appear anywhere
                    if "(Legacy)" not in acc.name:
                        acc.name = f"{acc.name} (Legacy)"
                    legacy_count += 1
            
            # Use case: User entered '1001' as Number. isdigit() is True. Good.
            # Use case: User entered 'SAL' as Number. isdigit() is False. Bad. Deactivate.

        db.session.commit()
        
        print(f"\nCleanup Complete.")
        print(f" - Standardized Numeric Accounts Verified.")
        print(f" - {legacy_count} Legacy Text Accounts Deactivated.")
        print("Please restart the web container to ensure all caches are cleared.")

if __name__ == "__main__":
    fix_accounts()
