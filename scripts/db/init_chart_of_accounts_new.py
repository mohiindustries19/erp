#!/usr/bin/env python3
"""
Initialize Chart of Accounts for Mohi Industries
Based on Frappe Books structure with Indian compliance
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from app.models.accounting import Account, AccountingSettings, FiscalYear
from datetime import date

def create_chart_of_accounts():
    """Create standard Chart of Accounts for Indian FMCG business"""
    
    print("🏗️  Creating Chart of Accounts...")
    
    # Root Accounts (5 types)
    accounts_data = {
        # ASSETS
        'Assets': {
            'root_type': 'Asset',
            'is_group': True,
            'children': {
                'Current Assets': {
                    'account_type': None,
                    'is_group': True,
                    'children': {
                        'Bank Accounts': {
                            'account_type': 'Bank',
                            'is_group': True,
                            'children': {
                                'HDFC Bank': {'account_type': 'Bank', 'account_number': '1001'},
                                'ICICI Bank': {'account_type': 'Bank', 'account_number': '1002'},
                            }
                        },
                        'Cash': {
                            'account_type': 'Cash',
                            'is_group': True,
                            'children': {
                                'Cash in Hand': {'account_type': 'Cash', 'account_number': '1010'},
                                'Petty Cash': {'account_type': 'Cash', 'account_number': '1011'},
                            }
                        },
                        'Accounts Receivable': {
                            'account_type': 'Receivable',
                            'is_group': True,
                            'children': {
                                'Debtors': {'account_type': 'Receivable', 'account_number': '1020'},
                            }
                        },
                        'Stock Assets': {
                            'account_type': 'Stock',
                            'is_group': True,
                            'children': {
                                'Finished Goods': {'account_type': 'Stock', 'account_number': '1030'},
                                'Raw Materials': {'account_type': 'Stock', 'account_number': '1031'},
                            }
                        },
                        'Tax Assets': {
                            'account_type': 'Tax',
                            'is_group': True,
                            'children': {
                                'GST Input': {'account_type': 'Tax', 'account_number': '1040'},
                                'TDS Receivable': {'account_type': 'Tax', 'account_number': '1041'},
                            }
                        },
                    }
                },
                'Fixed Assets': {
                    'account_type': 'Fixed Asset',
                    'is_group': True,
                    'children': {
                        'Plant and Machinery': {'account_type': 'Fixed Asset', 'account_number': '1100'},
                        'Furniture and Fixtures': {'account_type': 'Fixed Asset', 'account_number': '1101'},
                        'Vehicles': {'account_type': 'Fixed Asset', 'account_number': '1102'},
                    }
                },
            }
        },
        
        # LIABILITIES
        'Liabilities': {
            'root_type': 'Liability',
            'is_group': True,
            'children': {
                'Current Liabilities': {
                    'account_type': None,
                    'is_group': True,
                    'children': {
                        'Accounts Payable': {
                            'account_type': 'Payable',
                            'is_group': True,
                            'children': {
                                'Creditors': {'account_type': 'Payable', 'account_number': '2001'},
                            }
                        },
                        'Tax Liabilities': {
                            'account_type': 'Tax',
                            'is_group': True,
                            'children': {
                                'GST Output': {'account_type': 'Tax', 'account_number': '2010'},
                                'TDS Payable': {'account_type': 'Tax', 'account_number': '2011'},
                            }
                        },
                    }
                },
                'Long Term Liabilities': {
                    'account_type': None,
                    'is_group': True,
                    'children': {
                        'Bank Loans': {'account_type': None, 'account_number': '2100'},
                        'Unsecured Loans': {'account_type': None, 'account_number': '2101'},
                    }
                },
            }
        },
        
        # EQUITY
        'Equity': {
            'root_type': 'Equity',
            'is_group': True,
            'children': {
                'Capital Account': {'account_type': 'Equity', 'account_number': '3001'},
                'Retained Earnings': {'account_type': 'Equity', 'account_number': '3002'},
                'Drawings': {'account_type': 'Equity', 'account_number': '3003'},
            }
        },
        
        # INCOME
        'Income': {
            'root_type': 'Income',
            'is_group': True,
            'children': {
                'Direct Income': {
                    'account_type': 'Income Account',
                    'is_group': True,
                    'children': {
                        'Sales': {'account_type': 'Income Account', 'account_number': '4001'},
                        'Export Sales': {'account_type': 'Income Account', 'account_number': '4002'},
                    }
                },
                'Indirect Income': {
                    'account_type': 'Income Account',
                    'is_group': True,
                    'children': {
                        'Interest Income': {'account_type': 'Income Account', 'account_number': '4100'},
                        'Other Income': {'account_type': 'Income Account', 'account_number': '4101'},
                    }
                },
            }
        },
        
        # EXPENSES
        'Expense': {
            'root_type': 'Expense',
            'is_group': True,
            'children': {
                'Direct Expenses': {
                    'account_type': 'Cost of Goods Sold',
                    'is_group': True,
                    'children': {
                        'Cost of Goods Sold': {'account_type': 'Cost of Goods Sold', 'account_number': '5001'},
                        'Purchase': {'account_type': 'Cost of Goods Sold', 'account_number': '5002'},
                        'Freight and Forwarding': {'account_type': 'Cost of Goods Sold', 'account_number': '5003'},
                    }
                },
                'Indirect Expenses': {
                    'account_type': 'Expense Account',
                    'is_group': True,
                    'children': {
                        'Salary': {'account_type': 'Expense Account', 'account_number': '5100'},
                        'Rent': {'account_type': 'Expense Account', 'account_number': '5101'},
                        'Electricity': {'account_type': 'Expense Account', 'account_number': '5102'},
                        'Telephone': {'account_type': 'Expense Account', 'account_number': '5103'},
                        'Office Expenses': {'account_type': 'Expense Account', 'account_number': '5104'},
                        'Marketing Expenses': {'account_type': 'Expense Account', 'account_number': '5105'},
                        'Bank Charges': {'account_type': 'Expense Account', 'account_number': '5106'},
                        'Depreciation': {'account_type': 'Depreciation', 'account_number': '5107'},
                    }
                },
            }
        },
    }
    
    def create_account_tree(data, parent=None, lft_counter=[0]):
        """Recursively create account tree"""
        for name, details in data.items():
            lft_counter[0] += 1
            lft = lft_counter[0]
            
            # Create account
            account = Account(
                name=name,
                root_type=details.get('root_type', parent.root_type if parent else None),
                account_type=details.get('account_type'),
                account_number=details.get('account_number'),
                parent_account=parent,
                is_group=details.get('is_group', False),
                lft=lft,
                is_active=True
            )
            
            db.session.add(account)
            db.session.flush()  # Get the ID
            
            # Create children
            if 'children' in details:
                create_account_tree(details['children'], account, lft_counter)
            
            lft_counter[0] += 1
            account.rgt = lft_counter[0]
        
        return lft_counter[0]
    
    # Create all accounts
    create_account_tree(accounts_data)
    db.session.commit()
    
    print("Chart of Accounts created successfully.")
    
    # Count accounts
    total_accounts = Account.query.count()
    root_accounts = Account.query.filter_by(parent_account=None).count()
    leaf_accounts = Account.query.filter_by(is_group=False).count()
    
    print(f"   Total Accounts: {total_accounts}")
    print(f"   Root Accounts: {root_accounts}")
    print(f"   Leaf Accounts: {leaf_accounts}")


def create_default_settings():
    """Create default accounting settings"""
    
    print("\nCreating Accounting Settings...")
    
    # Get default accounts
    cash_account = Account.query.filter_by(name='Cash in Hand').first()
    bank_account = Account.query.filter_by(name='HDFC Bank').first()
    receivable_account = Account.query.filter_by(name='Debtors').first()
    payable_account = Account.query.filter_by(name='Creditors').first()
    income_account = Account.query.filter_by(name='Sales').first()
    expense_account = Account.query.filter_by(name='Cost of Goods Sold').first()
    gst_output = Account.query.filter_by(name='GST Output').first()
    gst_input = Account.query.filter_by(name='GST Input').first()
    
    settings = AccountingSettings(
        setup_complete=True,
        default_cash_account=cash_account,
        default_bank_account=bank_account,
        default_receivable_account=receivable_account,
        default_payable_account=payable_account,
        default_income_account=income_account,
        default_expense_account=expense_account,
        gst_output_account=gst_output,
        gst_input_account=gst_input
    )
    
    db.session.add(settings)
    db.session.commit()
    
    print("Accounting Settings created.")


def create_fiscal_year():
    """Create current fiscal year"""
    
    print("\nCreating Fiscal Year...")
    
    # Indian fiscal year: April to March
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
    
    print(f"Fiscal Year created: {fy.name}")


def main():
    """Main initialization function"""
    from app.models.accounting import Account as AccountModel
    
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("MOHI INDUSTRIES - ACCOUNTING SYSTEM INITIALIZATION")
        print("="*60 + "\n")
        
        # Check if already initialized
        if AccountModel.query.first():
            print("Chart of Accounts already exists.")
            response = input("Do you want to recreate it? (yes/no): ")
            if response.lower() != 'yes':
                print("Initialization cancelled.")
                return
            
            # Drop all accounting tables
            print("\nDropping existing accounting data...")
            db.session.execute(db.text('DELETE FROM journal_entry_accounts'))
            db.session.execute(db.text('DELETE FROM journal_entries'))
            db.session.execute(db.text('DELETE FROM accounting_settings'))
            db.session.execute(db.text('DELETE FROM fiscal_years'))
            db.session.execute(db.text('DELETE FROM accounts'))
            db.session.commit()
            print("Old data removed.\n")
        
        # Create chart of accounts
        create_chart_of_accounts()
        
        # Create settings
        create_default_settings()
        
        # Create fiscal year
        create_fiscal_year()
        
        print("\n" + "="*60)
        print("ACCOUNTING SYSTEM INITIALIZED SUCCESSFULLY")
        print("="*60)
        print("\nNext Steps:")
        print("   1. Review the Chart of Accounts")
        print("   2. Create opening balances via Journal Entry")
        print("   3. Start recording transactions")
        print("\n")


if __name__ == '__main__':
    main()
