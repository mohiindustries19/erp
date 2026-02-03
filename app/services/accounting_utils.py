"""Accounting helpers.

This project currently uses `AccountingEntry` as the ledger table for most UI/reports.
These helpers standardize how system accounts are resolved/created and how common
postings are produced (sales, receipts, expenses, opening balances).
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from sqlalchemy import func

from app import db
from app.models.accounting import AccountingEntry, Account, AccountingSettings


@dataclass(frozen=True)
class PostingLine:
    account: Account
    debit: Decimal
    credit: Decimal
    account_head: str
    description: str


def _dec(value) -> Decimal:
    if value is None:
        return Decimal('0')
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def get_or_create_account(
    *,
    name: str,
    root_type: str,
    account_type: Optional[str] = None,
    account_number: Optional[str] = None,
    description: Optional[str] = None,
) -> Account:
    """Find an active account by name (case-insensitive), else create it."""
    existing = Account.query.filter(func.lower(Account.name) == name.lower()).first()
    if existing:
        # Keep root/account_type aligned if not set.
        if root_type and existing.root_type != root_type:
            existing.root_type = root_type
        if account_type and not existing.account_type:
            existing.account_type = account_type
        if description and not existing.description:
            existing.description = description
        db.session.flush()
        return existing

    account = Account(
        name=name,
        account_number=account_number,
        root_type=root_type,
        account_type=account_type,
        description=description,
        is_active=True,
    )
    db.session.add(account)
    db.session.flush()
    return account


def get_or_create_settings() -> AccountingSettings:
    settings = AccountingSettings.query.first()
    if settings:
        return settings
    settings = AccountingSettings(setup_complete=False)
    db.session.add(settings)
    db.session.flush()
    return settings


def resolve_cash_account() -> Account:
    settings = get_or_create_settings()
    if settings.default_cash_account_id:
        account = Account.query.get(settings.default_cash_account_id)
        if account:
            return account
    return get_or_create_account(name='Cash', root_type='Asset', account_type='Cash')


def resolve_bank_account() -> Account:
    settings = get_or_create_settings()
    if settings.default_bank_account_id:
        account = Account.query.get(settings.default_bank_account_id)
        if account:
            return account
    return get_or_create_account(name='Bank', root_type='Asset', account_type='Bank')


def resolve_receivable_account() -> Account:
    settings = get_or_create_settings()
    if settings.default_receivable_account_id:
        account = Account.query.get(settings.default_receivable_account_id)
        if account:
            return account
    return get_or_create_account(name='Accounts Receivable', root_type='Asset', account_type='Receivable')


def resolve_payable_account(vendor_name: Optional[str] = None) -> Account:
    """Resolve a generic AP account; vendor-specific AP should be separate if desired."""
    settings = get_or_create_settings()
    if settings.default_payable_account_id:
        account = Account.query.get(settings.default_payable_account_id)
        if account:
            return account
    if vendor_name:
        return get_or_create_account(
            name=f'Accounts Payable - {vendor_name}',
            root_type='Liability',
            account_type='Payable',
        )
    return get_or_create_account(name='Accounts Payable', root_type='Liability', account_type='Payable')


def resolve_sales_account() -> Account:
    return get_or_create_account(name='Sales', root_type='Income', account_type='Sales')


def resolve_purchases_account() -> Account:
    return get_or_create_account(name='Purchases', root_type='Expense', account_type='Purchases')


def resolve_output_cgst() -> Account:
    return get_or_create_account(name='Output CGST', root_type='Liability', account_type='Tax')


def resolve_output_sgst() -> Account:
    return get_or_create_account(name='Output SGST', root_type='Liability', account_type='Tax')


def resolve_output_igst() -> Account:
    return get_or_create_account(name='Output IGST', root_type='Liability', account_type='Tax')


def resolve_input_cgst() -> Account:
    return get_or_create_account(name='Input CGST', root_type='Asset', account_type='Tax')


def resolve_input_sgst() -> Account:
    return get_or_create_account(name='Input SGST', root_type='Asset', account_type='Tax')


def resolve_input_igst() -> Account:
    return get_or_create_account(name='Input IGST', root_type='Asset', account_type='Tax')


def resolve_opening_balance_offset_account() -> Account:
    # Standard offset for opening balances.
    return get_or_create_account(name='Opening Balance Equity', root_type='Equity', account_type='Equity')


def resolve_payment_account(payment_mode: Optional[str]) -> Account:
    mode = (payment_mode or '').strip().lower()
    if mode in {'cash'}:
        return resolve_cash_account()
    # treat everything else as bank-like for now (upi/cheque/card/bank_transfer)
    return resolve_bank_account()


def create_accounting_entry(
    *,
    entry_date,
    reference_type: str,
    reference_id: int,
    account: Account,
    debit: Decimal,
    credit: Decimal,
    account_head: Optional[str] = None,
    description: str = '',
    created_by: Optional[int] = None,
) -> AccountingEntry:
    entry = AccountingEntry(
        entry_date=entry_date,
        reference_type=reference_type,
        reference_id=reference_id,
        account_id=account.id,
        account_head=account_head or account.name,
        debit=float(debit),
        credit=float(credit),
        description=description,
        created_by=created_by,
    )
    db.session.add(entry)
    return entry


def delete_posting(reference_type: str, reference_id: int) -> None:
    AccountingEntry.query.filter_by(reference_type=reference_type, reference_id=reference_id).delete()


def post_opening_balance(*, account: Account, amount_natural: Decimal, as_of_date, created_by: Optional[int] = None) -> None:
    """Post opening balance for a single account.

    `amount_natural` is positive in the account's natural direction:
    - Asset/Expense: debit
    - Liability/Equity/Income: credit
    """
    delete_posting('opening_balance', account.id)

    amount_natural = _dec(amount_natural)
    if abs(amount_natural) < Decimal('0.0001'):
        return

    offset = resolve_opening_balance_offset_account()

    is_debit_nature = account.root_type in {'Asset', 'Expense'}

    if is_debit_nature:
        debit = amount_natural
        credit = Decimal('0')
        offset_debit = Decimal('0')
        offset_credit = amount_natural
    else:
        debit = Decimal('0')
        credit = amount_natural
        offset_debit = amount_natural
        offset_credit = Decimal('0')

    description = f'Opening balance for {account.name}'
    create_accounting_entry(
        entry_date=as_of_date,
        reference_type='opening_balance',
        reference_id=account.id,
        account=account,
        debit=debit,
        credit=credit,
        description=description,
        created_by=created_by,
    )
    create_accounting_entry(
        entry_date=as_of_date,
        reference_type='opening_balance',
        reference_id=account.id,
        account=offset,
        debit=offset_debit,
        credit=offset_credit,
        description=description,
        created_by=created_by,
    )
