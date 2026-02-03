# Complete Accounting System for Mohi ERP

## Overview

This document explains the complete accounting and financial management system implemented in Mohi ERP. The system provides full visibility into your business finances with daily expense tracking, profit/loss statements, balance sheets, and more.

---

## Features

### 1. **Chart of Accounts**
Complete list of all account heads organized by:
- **Assets**: Cash, Bank, Inventory, Fixed Assets, GST ITC
- **Liabilities**: Accounts Payable, GST Payable, TDS, Loans
- **Equity**: Owner's Capital, Retained Earnings
- **Income**: Sales (Bakery, Pickles, Water), Other Income
- **Expenses**: Raw Materials, Salaries, Rent, Utilities, etc.

### 2. **Daily Expense Entry**
Record all business expenses with:
- Expense date and amount
- Vendor details (Name, GSTIN)
- Invoice number and date
- GST calculation (CGST/SGST or IGST)
- Payment mode (Cash, Bank, Cheque, UPI)
- Expense category
- Bill attachment support
- Approval workflow

### 3. **Ledger (Account Statement)**
View complete transaction history for any account:
- All debits and credits
- Running balance
- Date-wise filtering
- Opening and closing balance

### 4. **Profit & Loss Statement**
See your business profitability:
- Total Income (Sales by product category)
- Total Expenses (by category)
- Net Profit/Loss
- Date range filtering
- Financial year wise

### 5. **Balance Sheet**
Complete financial position:
- Assets (Current + Fixed)
- Liabilities (Current + Long-term)
- Equity
- As on any date

### 6. **Cash Flow Statement**
Track cash movement:
- Cash Inflows (Payments received)
- Cash Outflows (Expenses paid)
- Net Cash Flow
- Date range filtering

### 7. **Day Book**
All transactions for any specific day:
- All debits and credits
- Total verification
- Quick daily reconciliation

### 8. **Accounting Dashboard**
Quick overview:
- Today's transactions count
- This month's income
- This month's expenses
- Cash balance
- Bank balance
- Pending expenses

---

## Chart of Accounts Structure

### Assets (What You Own)

#### Current Assets
- **CASH** - Cash in Hand (₹50,000)
- **BANK** - Bank Account (₹5,00,000)
- **AR** - Accounts Receivable (Debtors)
- **INV** - Inventory - Raw Materials (₹2,00,000)
- **INV-FG** - Inventory - Finished Goods (₹3,00,000)
- **INV-PKG** - Inventory - Packaging (₹50,000)
- **GST-ITC** - GST Input Tax Credit
- **TDS-REC** - TDS Receivable

#### Fixed Assets
- **LAND** - Land & Building (₹20,00,000)
- **PLANT** - Plant & Machinery (₹15,00,000)
- **VEHICLE** - Vehicles (₹8,00,000)
- **FURNITURE** - Furniture & Fixtures (₹1,00,000)
- **COMPUTER** - Computers & IT (₹1,50,000)

### Liabilities (What You Owe)

#### Current Liabilities
- **AP** - Accounts Payable (Creditors)
- **GST-OUT** - GST Output Tax Payable
- **TDS-PAY** - TDS Payable
- **SAL-PAY** - Salary Payable
- **PF-PAY** - PF Payable
- **ESI-PAY** - ESI Payable

#### Long-term Liabilities
- **LOAN-BANK** - Bank Loan (₹5,00,000)
- **LOAN-OTHER** - Other Loans

### Equity (Owner's Investment)
- **CAPITAL** - Owner's Capital (₹50,00,000)
- **RETAINED** - Retained Earnings
- **DRAWINGS** - Owner's Drawings

### Income (Revenue)

#### Direct Income
- **SALES-BAK** - Sales - Bakery Products (GST 5%)
- **SALES-PKL** - Sales - Pickles (GST 12%)
- **SALES-WTR** - Sales - Mohi Neer Water (GST 18%)
- **SALES-OTHER** - Sales - Other Products (GST 18%)

#### Indirect Income
- **INT-INC** - Interest Income
- **OTHER-INC** - Other Income
- **DISC-REC** - Discount Received

### Expenses (Costs)

#### Direct Expenses (COGS)
- **PUR-RM** - Purchase - Raw Materials (GST 5%)
- **PUR-PKG** - Purchase - Packaging (GST 18%)
- **FREIGHT-IN** - Freight Inward (GST 18%)
- **LABOUR-DIR** - Direct Labour
- **FACTORY-EXP** - Factory Expenses (GST 18%)

#### Indirect Expenses (Operating)
- **SAL-ADMIN** - Salary - Administrative Staff
- **SAL-SALES** - Salary - Sales Staff
- **RENT** - Rent Expense (GST 18%)
- **ELECTRICITY** - Electricity Charges (GST 18%)
- **WATER** - Water Charges (GST 18%)
- **TELEPHONE** - Telephone & Internet (GST 18%)
- **FUEL** - Fuel & Vehicle Expenses (GST 18%)
- **REPAIR** - Repairs & Maintenance (GST 18%)
- **INSURANCE** - Insurance (GST 18%)
- **LEGAL** - Legal & Professional Fees (GST 18%)
- **AUDIT** - Audit Fees (GST 18%)
- **STATIONERY** - Stationery & Printing (GST 18%)
- **ADVERTISING** - Advertising & Marketing (GST 18%)
- **FREIGHT-OUT** - Freight Outward (GST 18%)
- **BANK-CHARGES** - Bank Charges (GST 18%)
- **INT-EXP** - Interest Expense
- **DEPRECIATION** - Depreciation
- **MISC-EXP** - Miscellaneous Expenses (GST 18%)

---

## Double-Entry Accounting

Every transaction creates TWO entries (Debit and Credit) to maintain balance.

### Example 1: Recording a Sale (Order)
```
When Order #ORD20250126001 for ₹10,000 is created:

Debit:  Accounts Receivable (AR)     ₹10,000  [Asset increases]
Credit: Sales - Bakery (SALES-BAK)   ₹10,000  [Income increases]
```

### Example 2: Recording Payment Received
```
When Payment #PAY20250126001 for ₹10,000 is received:

Debit:  Cash/Bank Account            ₹10,000  [Asset increases]
Credit: Accounts Receivable (AR)     ₹10,000  [Asset decreases]
```

### Example 3: Recording an Expense
```
When Electricity Bill of ₹5,000 + ₹900 GST = ₹5,900 is paid:

Debit:  Electricity Expense          ₹5,900   [Expense increases]
Credit: Bank Account                 ₹5,900   [Asset decreases]
```

### Example 4: Recording Raw Material Purchase
```
When Raw Material worth ₹20,000 + ₹1,000 GST = ₹21,000 is purchased:

Debit:  Purchase - Raw Materials     ₹20,000  [Expense increases]
Debit:  GST Input Tax Credit         ₹1,000   [Asset increases]
Credit: Bank Account                 ₹21,000  [Asset decreases]
```

---

## How to Use

### Step 1: Initialize Chart of Accounts

After setting up the database, run:

```bash
cd mohierp/mohi-erp
docker-compose exec web python scripts/db/init_chart_of_accounts.py
```

This will create all standard account heads with opening balances.

### Step 2: Record Daily Expenses

1. Go to **Accounting > Expenses > Add Expense**
2. Fill in:
   - Expense Date
   - Select Account (e.g., Electricity, Rent, Salary)
   - Amount (without GST)
   - Check "GST Applicable" if needed
   - Vendor Name and GSTIN
   - Invoice Number and Date
   - Payment Mode
   - Category
   - Description
3. Click **Save**

The system will:
- Auto-calculate GST (CGST/SGST or IGST)
- Generate expense number
- Create accounting entries
- Update account balances

### Step 3: View Reports

#### Profit & Loss
- Go to **Accounting > Reports > Profit & Loss**
- Select date range (default: current financial year)
- View Income vs Expenses
- See Net Profit/Loss

#### Balance Sheet
- Go to **Accounting > Reports > Balance Sheet**
- Select "As on Date"
- View Assets, Liabilities, Equity

#### Cash Flow
- Go to **Accounting > Reports > Cash Flow**
- Select date range
- View Cash In vs Cash Out

#### Day Book
- Go to **Accounting > Reports > Day Book**
- Select date
- View all transactions for that day

#### Ledger
- Go to **Accounting > Ledger**
- Select account
- View all transactions with running balance

### Step 4: Monitor Dashboard

- Go to **Accounting > Dashboard**
- Quick view of:
  - Today's transactions
  - Month's income and expenses
  - Cash and bank balances
  - Pending expenses

---

## Automatic Accounting Entries

The system automatically creates accounting entries for:

### 1. **Order Creation**
```
Debit:  Accounts Receivable
Credit: Sales (by product category)
```

### 2. **Payment Received**
```
Debit:  Cash/Bank Account
Credit: Accounts Receivable
```

### 3. **Expense Recorded**
```
Debit:  Expense Account
Credit: Cash/Bank Account
```

### 4. **GST on Expenses**
```
Debit:  Expense Account (Base Amount)
Debit:  GST Input Tax Credit (GST Amount)
Credit: Cash/Bank Account (Total)
```

---

## GST Compliance

### Intra-State Transactions (Same State)
- CGST (Central GST) = GST Rate / 2
- SGST (State GST) = GST Rate / 2
- Example: 18% GST = 9% CGST + 9% SGST

### Inter-State Transactions (Different State)
- IGST (Integrated GST) = Full GST Rate
- Example: 18% GST = 18% IGST

The system automatically determines this based on GSTIN state codes.

---

## Financial Year Management

Indian Financial Year: **April 1 to March 31**

Example:
- FY 2024-25: April 1, 2024 to March 31, 2025
- FY 2025-26: April 1, 2025 to March 31, 2026

All reports default to current financial year.

---

## Key Benefits

### 1. **Daily Visibility**
- Know exactly where your money is going every day
- Track all expenses in real-time
- No surprises at month-end

### 2. **Profit Tracking**
- See profit/loss anytime
- Compare month-to-month
- Identify profitable products

### 3. **Cash Management**
- Monitor cash flow
- Avoid cash crunches
- Plan payments better

### 4. **GST Compliance**
- Automatic GST calculation
- Input Tax Credit tracking
- Ready for GST returns

### 5. **Financial Reports**
- Professional P&L statement
- Balance sheet
- Ready for auditors/banks

### 6. **Decision Making**
- Data-driven decisions
- Identify cost-saving opportunities
- Plan investments

---

## Common Expense Categories

### Manufacturing Business (FMCG)

1. **Raw Materials** - Flour, sugar, spices, etc.
2. **Packaging** - Bottles, labels, boxes, pouches
3. **Labour** - Factory workers, helpers
4. **Utilities** - Electricity, water, gas
5. **Rent** - Factory/office rent
6. **Salaries** - Admin, sales, management
7. **Transportation** - Delivery vehicles, fuel
8. **Marketing** - Advertising, promotions
9. **Maintenance** - Equipment repairs
10. **Professional Fees** - CA, lawyer, consultant

---

## Tips for Best Results

### 1. **Record Daily**
- Enter expenses every day
- Don't wait for month-end
- Keep bills organized

### 2. **Categorize Properly**
- Use correct account heads
- Consistent categorization
- Easier to analyze later

### 3. **Reconcile Regularly**
- Match bank statements weekly
- Verify cash balance daily
- Check GST calculations

### 4. **Review Reports Monthly**
- Check P&L every month
- Compare with previous months
- Identify trends

### 5. **Plan Ahead**
- Use reports for budgeting
- Forecast cash needs
- Plan major expenses

---

## Future Enhancements

1. **GST Returns** - Auto-generate GSTR-1, GSTR-3B
2. **TDS Management** - TDS calculation and filing
3. **Payroll** - Salary processing with PF/ESI
4. **Budget vs Actual** - Compare planned vs actual
5. **Multi-year Comparison** - Year-over-year analysis
6. **Bank Reconciliation** - Auto-match bank statements
7. **Depreciation Schedule** - Auto-calculate depreciation
8. **Financial Ratios** - Liquidity, profitability ratios

---

## Support

For questions or issues:
- Check this documentation
- Review example transactions
- Contact system administrator

---

**Remember**: Good accounting = Good business decisions!

Track every rupee, know your profit, grow your business. 🚀
