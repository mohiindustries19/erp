"""
Accounting Models - Double Entry Bookkeeping System
Based on Frappe Books accounting structure
"""
from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint, Index, func
from decimal import Decimal

class Account(db.Model):
    """
    General Ledger (Chart of Accounts) - Tree structure for accounting
    Supports 5 root types: Asset, Liability, Equity, Income, Expense
    """
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False, index=True)
    account_number = db.Column(db.String(20), unique=True, index=True)
    
    # Root Type: Asset, Liability, Equity, Income, Expense
    root_type = db.Column(db.String(20), nullable=False, index=True)
    
    # Account Type: Bank, Cash, Receivable, Payable, Tax, etc.
    account_type = db.Column(db.String(50))
    
    # Tree Structure
    parent_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    is_group = db.Column(db.Boolean, default=False)
    
    # Nested Set Model (for tree queries)
    lft = db.Column(db.Integer, default=0)
    rgt = db.Column(db.Integer, default=0)
    
    # Additional Info
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    parent_account = db.relationship('Account', remote_side=[id], backref='child_accounts')
    # Don't use backref here - let AccountingEntry and Expense define their own relationships
    
    @property
    def current_balance(self):
        """Get current balance from accounting entries"""
        result = db.session.query(
            func.sum(AccountingEntry.debit - AccountingEntry.credit)
        ).filter(AccountingEntry.account_id == self.id).scalar()
        return result or Decimal('0')
    
    @property
    def opening_balance(self):
        """Opening balance in the account's natural direction (always >= 0).

        Asset/Expense: debit-balance -> returns (debit-credit)
        Liability/Equity/Income: credit-balance -> returns (credit-debit)
        """
        signed = self.opening_balance_signed
        return signed if self.is_debit else (Decimal('0') - signed)

    @property
    def opening_balance_signed(self):
        """Opening balance as signed ledger delta (debit-credit)."""
        result = db.session.query(
            func.sum(AccountingEntry.debit - AccountingEntry.credit)
        ).filter(
            AccountingEntry.account_id == self.id,
            AccountingEntry.reference_type == 'opening_balance',
            AccountingEntry.reference_id == self.id,
        ).scalar()
        return result or Decimal('0')
    
    @property
    def is_debit(self):
        """Asset and Expense accounts have debit balance"""
        return self.root_type in ['Asset', 'Expense']
    
    @property
    def is_credit(self):
        """Liability, Equity, and Income accounts have credit balance"""
        return not self.is_debit
    
    @property
    def full_path(self):
        """Get full account path"""
        if self.parent_account:
            return f"{self.parent_account.full_path} > {self.name}"
        return self.name
    
    def get_balance(self, as_of_date=None):
        """Calculate account balance"""
        return self.current_balance
    
    def __repr__(self):
        return f'<Account {self.name} ({self.root_type})>'


class JournalEntry(db.Model):
    """
    Journal Entry - Main accounting transaction document
    Supports double-entry bookkeeping
    """
    __tablename__ = 'journal_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    entry_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Entry Type
    entry_type = db.Column(db.String(50), nullable=False, default='Journal Entry')
    # Options: Journal Entry, Bank Entry, Cash Entry, Credit Note, Debit Note, etc.
    
    # Date
    date = db.Column(db.Date, nullable=False, index=True)
    
    # Status: draft, submitted, cancelled
    status = db.Column(db.String(20), default='draft', index=True)
    
    # References
    reference_number = db.Column(db.String(100))
    reference_date = db.Column(db.Date)
    user_remark = db.Column(db.Text)
    
    # Linked Documents (for auto-generated entries)
    reference_type = db.Column(db.String(50))  # Order, Payment, Invoice, etc.
    reference_id = db.Column(db.Integer)
    
    # User tracking
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    submitted_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_at = db.Column(db.DateTime)
    
    # Relationships
    accounts = db.relationship('JournalEntryAccount', backref='journal_entry', 
                              lazy='dynamic', cascade='all, delete-orphan')
    created_by = db.relationship('User', foreign_keys=[created_by_id])
    submitted_by = db.relationship('User', foreign_keys=[submitted_by_id])
    
    def validate_double_entry(self):
        """Validate that debits equal credits"""
        total_debit = sum(acc.debit for acc in self.accounts)
        total_credit = sum(acc.credit for acc in self.accounts)
        
        if abs(total_debit - total_credit) > Decimal('0.01'):
            raise ValueError(f"Debits ({total_debit}) must equal Credits ({total_credit})")
        
        return True
    
    def submit(self, user_id):
        """Submit the journal entry (post to ledger)"""
        if self.status != 'draft':
            raise ValueError("Only draft entries can be submitted")
        
        self.validate_double_entry()
        
        self.status = 'submitted'
        self.submitted_by_id = user_id
        self.submitted_at = datetime.utcnow()
        
        db.session.commit()
    
    def cancel(self):
        """Cancel a submitted entry"""
        if self.status != 'submitted':
            raise ValueError("Only submitted entries can be cancelled")
        
        self.status = 'cancelled'
        db.session.commit()
    
    @property
    def total_debit(self):
        return sum(acc.debit for acc in self.accounts)
    
    @property
    def total_credit(self):
        return sum(acc.credit for acc in self.accounts)
    
    def __repr__(self):
        return f'<JournalEntry {self.entry_number} - {self.entry_type}>'


class JournalEntryAccount(db.Model):
    """
    Journal Entry Account Line - Individual debit/credit entries
    """
    __tablename__ = 'journal_entry_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    journal_entry_id = db.Column(db.Integer, db.ForeignKey('journal_entries.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    
    # Amounts
    debit = db.Column(db.Numeric(15, 2), default=0, nullable=False)
    credit = db.Column(db.Numeric(15, 2), default=0, nullable=False)
    
    # Description
    description = db.Column(db.Text)
    
    # Constraints: Either debit or credit must be non-zero, but not both
    __table_args__ = (
        CheckConstraint('(debit > 0 AND credit = 0) OR (credit > 0 AND debit = 0)', 
                       name='check_debit_or_credit'),
        Index('idx_je_account', 'journal_entry_id', 'account_id'),
    )
    
    def __repr__(self):
        amount = self.debit if self.debit > 0 else self.credit
        type_str = 'Dr' if self.debit > 0 else 'Cr'
        return f'<JEAccount {self.account.name} {type_str} {amount}>'


class FiscalYear(db.Model):
    """Fiscal Year configuration"""
    __tablename__ = 'fiscal_years'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<FiscalYear {self.name}>'


class AccountingSettings(db.Model):
    """Accounting configuration and settings"""
    __tablename__ = 'accounting_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Setup
    setup_complete = db.Column(db.Boolean, default=False)
    
    # Default Accounts
    default_cash_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    default_bank_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    default_receivable_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    default_payable_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    default_income_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    default_expense_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    
    # GST Accounts
    gst_output_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    gst_input_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    
    # Relationships
    default_cash_account = db.relationship('Account', foreign_keys=[default_cash_account_id])
    default_bank_account = db.relationship('Account', foreign_keys=[default_bank_account_id])
    default_receivable_account = db.relationship('Account', foreign_keys=[default_receivable_account_id])
    default_payable_account = db.relationship('Account', foreign_keys=[default_payable_account_id])
    default_income_account = db.relationship('Account', foreign_keys=[default_income_account_id])
    default_expense_account = db.relationship('Account', foreign_keys=[default_expense_account_id])
    gst_output_account = db.relationship('Account', foreign_keys=[gst_output_account_id])
    gst_input_account = db.relationship('Account', foreign_keys=[gst_input_account_id])
    
    def __repr__(self):
        return f'<AccountingSettings>'


class AccountingEntry(db.Model):
    """
    Simple Accounting Entry model for backward compatibility
    Used by existing routes - simpler than full double-entry
    """
    __tablename__ = 'accounting_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False, index=True)
    
    # Reference to source transaction
    reference_type = db.Column(db.String(50))  # order, payment, expense, etc.
    reference_id = db.Column(db.Integer)
    
    # Account details
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    account_head = db.Column(db.String(200))
    
    # Amounts
    debit = db.Column(db.Numeric(15, 2), default=0, nullable=False)
    credit = db.Column(db.Numeric(15, 2), default=0, nullable=False)
    
    # Description
    description = db.Column(db.Text)
    
    # User tracking
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    account = db.relationship('Account', foreign_keys=[account_id])
    
    def __repr__(self):
        return f'<AccountingEntry {self.entry_date} {self.account_head}>'


class Expense(db.Model):
    """
    Expense tracking model for backward compatibility
    """
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    expense_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    expense_date = db.Column(db.Date, nullable=False, index=True)
    
    # Account
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    
    # Amount
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    
    # GST
    is_gst_applicable = db.Column(db.Boolean, default=False)
    total_gst = db.Column(db.Numeric(15, 2), default=0)
    cgst_amount = db.Column(db.Numeric(15, 2), default=0)
    sgst_amount = db.Column(db.Numeric(15, 2), default=0)
    igst_amount = db.Column(db.Numeric(15, 2), default=0)
    total_amount = db.Column(db.Numeric(15, 2), nullable=False)
    
    # Vendor details
    vendor_name = db.Column(db.String(200))
    vendor_gstin = db.Column(db.String(15))
    invoice_number = db.Column(db.String(100))
    invoice_date = db.Column(db.Date)
    
    # Payment
    payment_mode = db.Column(db.String(50))  # cash, bank, upi, cheque
    payment_status = db.Column(db.String(50), default='paid')  # paid, pending
    reference_number = db.Column(db.String(100))
    
    # Category and description
    expense_category = db.Column(db.String(100))
    description = db.Column(db.Text)
    remarks = db.Column(db.Text)
    
    # Approval
    approval_status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    
    # User tracking
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    account = db.relationship('Account', foreign_keys=[account_id])
    
    def __repr__(self):
        return f'<Expense {self.expense_number}>'


class ExpenseCategory(db.Model):
    """Master list for expense categories (controlled dropdown)."""
    __tablename__ = 'expense_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ExpenseCategory {self.name}>'


# Backward compatibility aliases for old code
ChartOfAccounts = Account  # Alias for old code
FinancialYear = FiscalYear  # Alias for old code
