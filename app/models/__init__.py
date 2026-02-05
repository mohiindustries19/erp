"""
Database Models for Mohi Industries ERP
"""
from app.models.user import User
from app.models.company import Company
from app.models.distributor import Distributor
from app.models.product import Product, ProductCategory
from app.models.inventory import Inventory, Batch, Warehouse
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.document import Document
from app.models.accounting import (
    Account, JournalEntry, JournalEntryAccount, FiscalYear, AccountingSettings,
    AccountingEntry, Expense, ExpenseCategory,  # Backward compatibility models
    ChartOfAccounts, FinancialYear  # Aliases
)
from app.models.purchasing import Vendor, PurchaseOrder, PurchaseOrderItem, VendorBill, VendorBillItem, VendorPayment
from app.models.qc import QualityCheckTemplate, QualityCheckItem, BatchQualityCheck
from app.models.settings import AppSettings, UserSettings
from app.models.goods import Goods

__all__ = [
    'User', 'Company', 'Distributor',
    'Product', 'ProductCategory',
    'Inventory', 'Batch', 'Warehouse',
    'Order', 'OrderItem',
    'Payment',
    'Document',
    'Account', 'JournalEntry', 'JournalEntryAccount', 'FiscalYear', 'AccountingSettings',
    'AccountingEntry', 'Expense', 'ExpenseCategory',  # Backward compatibility
    'ChartOfAccounts', 'FinancialYear',  # Aliases
    'Vendor', 'PurchaseOrder', 'PurchaseOrderItem', 'VendorBill', 'VendorBillItem', 'VendorPayment',
    'QualityCheckTemplate', 'QualityCheckItem', 'BatchQualityCheck',
    'AppSettings', 'UserSettings',
    'Goods'
]
