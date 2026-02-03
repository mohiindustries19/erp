import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sqlalchemy.exc import IntegrityError
from app import create_app, db
from app.models.accounting import ChartOfAccounts

def fix_accounts():
    app = create_app()
    with app.app_context():
        print("Starting Chart of Accounts Cleanup (Safe Mode)...")
        
        # 1. Define the Standard Map (Good Accounts)
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
            try:
                # Check if account number exists
                account = ChartOfAccounts.query.filter_by(account_number=code).first()
                
                if not account:
                    # Check if NAME exists (to avoid unique constraint error on name)
                    existing_name = ChartOfAccounts.query.filter_by(name=name).first()
                    if existing_name:
                        print(f"  [!] Name '{name}' already exists with code {existing_name.account_number}. Updating code to {code}...")
                        existing_name.account_number = code
                        existing_name.root_type = root_type
                        existing_name.description = desc
                        existing_name.is_active = True
                        db.session.add(existing_name)
                    else:
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
                    # Account with this CODE exists
                    if account.name != name:
                        # Check if the TARGET name is already taken by ANOTHER account
                        name_conflict = ChartOfAccounts.query.filter(ChartOfAccounts.name == name, ChartOfAccounts.id != account.id).first()
                        if name_conflict:
                            print(f"  [!] Cannot rename {account.name} ({code}) to {name} because {name} already exists as code {name_conflict.account_number}.")
                            print(f"  [*] Renaming conflict account {name} to {name} (Old)...")
                            name_conflict.name = f"{name} (Old)"
                            db.session.add(name_conflict)
                            db.session.flush() # Apply rename first
                        
                        print(f"  [*] Updating Name: {account.name} -> {name}")
                        account.name = name
                        
                    if not account.is_active:
                         print(f"  [^] Reactivating: {code}")
                         account.is_active = True
                    
                    account.description = desc
                
                db.session.commit()
                
            except Exception as e:
                db.session.rollback()
                print(f"  [!] Error processing {code} - {name}: {str(e)}")

        # 3. Identify and Deactivate Legacy Text Codes
        print("\nDeactivating Legacy Text-Based Accounts...")
        try:
            all_accounts = ChartOfAccounts.query.all()
            legacy_count = 0
            
            for acc in all_accounts:
                if acc.account_number and not acc.account_number.isdigit():
                    if acc.is_active:
                        print(f"  [-] Deactivating Legacy: {acc.account_number} - {acc.name}")
                        acc.is_active = False
                        legacy_count += 1
                        db.session.add(acc)
            
            db.session.commit()
            print(f"\nCleanup Complete. {legacy_count} legacy accounts deactivated.")
            
        except Exception as e:
            db.session.rollback()
            print(f"  [!] Error during deactivation: {str(e)}")

if __name__ == "__main__":
    fix_accounts()
