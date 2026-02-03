"""Ledger rebuild utilities.

Regenerates `AccountingEntry` rows from source documents (orders, payments, expenses,
vendor bills, vendor payments) for a given date range.

Safety defaults:
- Only touches entries whose `reference_type` is one of the supported auto-posted types.
- Does not touch opening balances (reference_type='opening_balance').
- Does not touch unknown/manual reference types.

This is intended as an admin repair tool when the posting logic evolves.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Iterable, Optional

from app import db
from app.models.accounting import AccountingEntry, Expense
from app.models.company import Company
from app.models.order import Order
from app.models.payment import Payment
from app.models.purchasing import VendorBill, VendorPayment
from app.services.accounting_utils import (
    create_accounting_entry,
    delete_posting,
    resolve_input_cgst,
    resolve_input_igst,
    resolve_input_sgst,
    resolve_output_cgst,
    resolve_output_igst,
    resolve_output_sgst,
    resolve_payment_account,
    resolve_purchases_account,
    resolve_receivable_account,
    resolve_sales_account,
    get_or_create_account,
)


@dataclass
class LedgerRebuildSummary:
    deleted_entries: int = 0
    created_entries: int = 0

    orders_processed: int = 0
    orders_skipped: int = 0

    payments_processed: int = 0
    payments_skipped: int = 0

    expenses_processed: int = 0
    expenses_skipped: int = 0

    vendor_bills_processed: int = 0
    vendor_bills_skipped: int = 0

    vendor_payments_processed: int = 0
    vendor_payments_skipped: int = 0


SUPPORTED_REFERENCE_TYPES = {
    'order',
    'payment',
    'expense',
    'vendor_bill',
    'vendor_payment',
}


def _dec(value) -> Decimal:
    if value is None:
        return Decimal('0')
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def _company_state_code(default: str = '27') -> str:
    company = Company.query.first()
    if company and getattr(company, 'state_code', None):
        return str(company.state_code)
    return default


def _gst_split_by_gstin(vendor_gstin: Optional[str], tax_amount: Decimal, company_state_code: str) -> tuple[Decimal, Decimal, Decimal]:
    if not tax_amount or tax_amount <= 0:
        return Decimal('0'), Decimal('0'), Decimal('0')
    gstin = (vendor_gstin or '').strip()
    if len(gstin) >= 2:
        vendor_state_code = gstin[:2]
        if vendor_state_code == company_state_code:
            half = (tax_amount / Decimal('2'))
            return half, half, Decimal('0')
        return Decimal('0'), Decimal('0'), tax_amount
    half = (tax_amount / Decimal('2'))
    return half, half, Decimal('0')


def _resolve_vendor_ap_account(bill: VendorBill):
    vendor = bill.vendor
    if vendor and vendor.ap_account_id:
        account = get_or_create_account(
            name=f'Accounts Payable - {vendor.business_name}',
            root_type='Liability',
            account_type='Payable',
            account_number=f'AP-{vendor.code}',
            description='Current Liabilities',
        )
        if account.id != vendor.ap_account_id:
            vendor.ap_account_id = account.id
            db.session.flush()
        return account

    if not vendor:
        return get_or_create_account(name='Accounts Payable', root_type='Liability', account_type='Payable')

    account = get_or_create_account(
        name=f'Accounts Payable - {vendor.business_name}',
        root_type='Liability',
        account_type='Payable',
        account_number=f'AP-{vendor.code}',
        description='Current Liabilities',
    )
    vendor.ap_account_id = account.id
    db.session.flush()
    return account


def post_order(order: Order, *, created_by: Optional[int] = None) -> int:
    if not order or (order.status or '').lower() == 'cancelled':
        return 0

    delete_posting('order', order.id)

    ar = resolve_receivable_account()
    sales = resolve_sales_account()
    out_cgst = resolve_output_cgst()
    out_sgst = resolve_output_sgst()
    out_igst = resolve_output_igst()

    customer = order.distributor.business_name if getattr(order, 'distributor', None) else 'Customer'
    desc = f'Sale {order.order_number} to {customer}'

    created = 0
    create_accounting_entry(
        entry_date=order.order_date,
        reference_type='order',
        reference_id=order.id,
        account=ar,
        debit=_dec(order.total_amount),
        credit=Decimal('0'),
        description=desc,
        created_by=created_by,
    )
    created += 1
    create_accounting_entry(
        entry_date=order.order_date,
        reference_type='order',
        reference_id=order.id,
        account=sales,
        debit=Decimal('0'),
        credit=_dec(order.taxable_amount),
        description=desc,
        created_by=created_by,
    )
    created += 1

    if _dec(order.cgst_amount) > 0:
        create_accounting_entry(
            entry_date=order.order_date,
            reference_type='order',
            reference_id=order.id,
            account=out_cgst,
            debit=Decimal('0'),
            credit=_dec(order.cgst_amount),
            description=f'{desc} - CGST',
            created_by=created_by,
        )
        created += 1
    if _dec(order.sgst_amount) > 0:
        create_accounting_entry(
            entry_date=order.order_date,
            reference_type='order',
            reference_id=order.id,
            account=out_sgst,
            debit=Decimal('0'),
            credit=_dec(order.sgst_amount),
            description=f'{desc} - SGST',
            created_by=created_by,
        )
        created += 1
    if _dec(order.igst_amount) > 0:
        create_accounting_entry(
            entry_date=order.order_date,
            reference_type='order',
            reference_id=order.id,
            account=out_igst,
            debit=Decimal('0'),
            credit=_dec(order.igst_amount),
            description=f'{desc} - IGST',
            created_by=created_by,
        )
        created += 1

    return created


def post_payment(payment: Payment, *, created_by: Optional[int] = None) -> int:
    if not payment:
        return 0

    delete_posting('payment', payment.id)

    if (payment.status or '').lower() != 'cleared':
        return 0

    amount = _dec(payment.amount)
    if amount <= 0:
        return 0

    debit_account = resolve_payment_account(payment.payment_mode)
    ar_account = resolve_receivable_account()

    order = payment.order
    customer = order.distributor.business_name if order and getattr(order, 'distributor', None) else 'Customer'
    order_number = order.order_number if order else ''
    desc = f'Payment received from {customer} for {order_number}'.strip()

    create_accounting_entry(
        entry_date=payment.payment_date,
        reference_type='payment',
        reference_id=payment.id,
        account=debit_account,
        debit=amount,
        credit=Decimal('0'),
        description=desc,
        created_by=created_by,
    )
    create_accounting_entry(
        entry_date=payment.payment_date,
        reference_type='payment',
        reference_id=payment.id,
        account=ar_account,
        debit=Decimal('0'),
        credit=amount,
        description=desc,
        created_by=created_by,
    )
    return 2


def post_expense(expense: Expense, *, created_by: Optional[int] = None) -> int:
    if not expense:
        return 0

    delete_posting('expense', expense.id)

    amount = _dec(expense.total_amount)
    if amount <= 0:
        return 0

    if not expense.account:
        return 0

    payment_account = resolve_payment_account(expense.payment_mode)
    desc_debit = f'Expense: {expense.description or expense.vendor_name or expense.expense_number}'
    desc_credit = f'Payment for: {expense.description or expense.vendor_name or expense.expense_number}'

    create_accounting_entry(
        entry_date=expense.expense_date,
        reference_type='expense',
        reference_id=expense.id,
        account=expense.account,
        debit=amount,
        credit=Decimal('0'),
        description=desc_debit,
        created_by=created_by,
    )
    create_accounting_entry(
        entry_date=expense.expense_date,
        reference_type='expense',
        reference_id=expense.id,
        account=payment_account,
        debit=Decimal('0'),
        credit=amount,
        description=desc_credit,
        created_by=created_by,
    )
    return 2


def post_vendor_bill(bill: VendorBill, *, created_by: Optional[int] = None) -> int:
    if not bill:
        return 0

    delete_posting('vendor_bill', bill.id)

    if (bill.approval_status or '').lower() != 'approved':
        return 0

    purchases_account = resolve_purchases_account()
    input_cgst = resolve_input_cgst()
    input_sgst = resolve_input_sgst()
    input_igst = resolve_input_igst()
    ap_account = _resolve_vendor_ap_account(bill)

    company_state_code = _company_state_code()
    tax_amount = _dec(bill.tax_amount)
    cgst, sgst, igst = _gst_split_by_gstin(getattr(bill.vendor, 'gstin', None), tax_amount, company_state_code)

    created = 0

    create_accounting_entry(
        entry_date=bill.bill_date,
        reference_type='vendor_bill',
        reference_id=bill.id,
        account=purchases_account,
        debit=_dec(bill.subtotal),
        credit=Decimal('0'),
        description=f'Vendor bill {bill.bill_number} - Purchases',
        created_by=created_by,
    )
    created += 1

    if cgst > 0:
        create_accounting_entry(
            entry_date=bill.bill_date,
            reference_type='vendor_bill',
            reference_id=bill.id,
            account=input_cgst,
            debit=cgst,
            credit=Decimal('0'),
            description=f'Vendor bill {bill.bill_number} - Input CGST',
            created_by=created_by,
        )
        created += 1
    if sgst > 0:
        create_accounting_entry(
            entry_date=bill.bill_date,
            reference_type='vendor_bill',
            reference_id=bill.id,
            account=input_sgst,
            debit=sgst,
            credit=Decimal('0'),
            description=f'Vendor bill {bill.bill_number} - Input SGST',
            created_by=created_by,
        )
        created += 1
    if igst > 0:
        create_accounting_entry(
            entry_date=bill.bill_date,
            reference_type='vendor_bill',
            reference_id=bill.id,
            account=input_igst,
            debit=igst,
            credit=Decimal('0'),
            description=f'Vendor bill {bill.bill_number} - Input IGST',
            created_by=created_by,
        )
        created += 1

    create_accounting_entry(
        entry_date=bill.bill_date,
        reference_type='vendor_bill',
        reference_id=bill.id,
        account=ap_account,
        debit=Decimal('0'),
        credit=_dec(bill.total_amount),
        description=f'Vendor bill {bill.bill_number} - Payable',
        created_by=created_by,
    )
    created += 1

    return created


def post_vendor_payment(vp: VendorPayment, *, created_by: Optional[int] = None) -> int:
    if not vp:
        return 0

    delete_posting('vendor_payment', vp.id)

    if (vp.status or '').lower() != 'cleared':
        return 0

    amount = _dec(vp.amount)
    if amount <= 0:
        return 0

    bill = vp.vendor_bill
    if not bill or not bill.vendor:
        return 0

    ap_account = _resolve_vendor_ap_account(bill)
    credit_account = resolve_payment_account(vp.payment_mode)

    desc = f'Vendor bill {bill.bill_number} - Payment'

    create_accounting_entry(
        entry_date=vp.payment_date,
        reference_type='vendor_payment',
        reference_id=vp.id,
        account=ap_account,
        debit=amount,
        credit=Decimal('0'),
        description=desc,
        created_by=created_by,
    )
    create_accounting_entry(
        entry_date=vp.payment_date,
        reference_type='vendor_payment',
        reference_id=vp.id,
        account=credit_account,
        debit=Decimal('0'),
        credit=amount,
        description=desc,
        created_by=created_by,
    )
    return 2


def _iter_query_in_chunks(query, chunk_size: int = 500) -> Iterable:
    offset = 0
    while True:
        rows = query.limit(chunk_size).offset(offset).all()
        if not rows:
            break
        for row in rows:
            yield row
        offset += chunk_size


def rebuild_ledger(
    *,
    start_date: date,
    end_date: date,
    include_orders: bool = True,
    include_payments: bool = True,
    include_expenses: bool = True,
    include_vendor: bool = True,
    dry_run: bool = True,
    run_as_user_id: Optional[int] = None,
) -> LedgerRebuildSummary:
    """Rebuild auto-posted ledger entries for a date range.

    When `dry_run=True`, no DB changes are committed, but the summary reflects what
    would be deleted/created.
    """

    summary = LedgerRebuildSummary()

    reference_types = set()
    if include_orders:
        reference_types.add('order')
    if include_payments:
        reference_types.add('payment')
    if include_expenses:
        reference_types.add('expense')
    if include_vendor:
        reference_types.update({'vendor_bill', 'vendor_payment'})

    if not reference_types:
        return summary

    delete_q = AccountingEntry.query.filter(
        AccountingEntry.entry_date >= start_date,
        AccountingEntry.entry_date <= end_date,
        AccountingEntry.reference_type.in_(sorted(reference_types)),
    )

    summary.deleted_entries = int(delete_q.count())

    if not dry_run:
        delete_q.delete(synchronize_session=False)

    # Recreate postings from source docs
    if include_orders:
        q = Order.query.filter(Order.order_date >= start_date, Order.order_date <= end_date)
        for order in _iter_query_in_chunks(q):
            created = post_order(order, created_by=run_as_user_id)
            if created:
                summary.orders_processed += 1
                summary.created_entries += created
            else:
                summary.orders_skipped += 1

    if include_payments:
        q = Payment.query.filter(Payment.payment_date >= start_date, Payment.payment_date <= end_date)
        for payment in _iter_query_in_chunks(q):
            created = post_payment(payment, created_by=run_as_user_id)
            if created:
                summary.payments_processed += 1
                summary.created_entries += created
            else:
                summary.payments_skipped += 1

    if include_expenses:
        q = Expense.query.filter(Expense.expense_date >= start_date, Expense.expense_date <= end_date)
        for expense in _iter_query_in_chunks(q):
            created = post_expense(expense, created_by=run_as_user_id)
            if created:
                summary.expenses_processed += 1
                summary.created_entries += created
            else:
                summary.expenses_skipped += 1

    if include_vendor:
        q = VendorBill.query.filter(VendorBill.bill_date >= start_date, VendorBill.bill_date <= end_date)
        for bill in _iter_query_in_chunks(q):
            created = post_vendor_bill(bill, created_by=run_as_user_id)
            if created:
                summary.vendor_bills_processed += 1
                summary.created_entries += created
            else:
                summary.vendor_bills_skipped += 1

        q = VendorPayment.query.filter(VendorPayment.payment_date >= start_date, VendorPayment.payment_date <= end_date)
        for vp in _iter_query_in_chunks(q):
            created = post_vendor_payment(vp, created_by=run_as_user_id)
            if created:
                summary.vendor_payments_processed += 1
                summary.created_entries += created
            else:
                summary.vendor_payments_skipped += 1

    if dry_run:
        db.session.rollback()
    else:
        db.session.commit()

    return summary
