# Import Distributors Guide

## Overview
This guide explains how to import your 68 bread distributors into the mohi-erp system.

---

## Files Created

1. **`scripts/imports/import_distributors.py`** - Python script to import distributors
2. **`data/distributors_list.csv`** - Clean CSV file with all distributor data
3. **`IMPORT_DISTRIBUTORS_GUIDE.md`** - This guide

---

## Distributor Data Summary

**Total Distributors:** 68  
**Locations Covered:**
- Patna (19 distributors)
- Vaishali (18 distributors)
- Nalanda (5 distributors)
- Darbhanga (4 distributors)
- Chapra (4 distributors)
- Nawada (2 distributors)
- Motihari (2 distributors)
- Others (14 distributors)

---

## How to Import

### Step 1: Activate Virtual Environment
```cmd
cd D:\OtherRepos\mohierp\mohi-erp
.venv\Scripts\activate
```

### Step 2: Run Import Script
```cmd
python scripts/imports/import_distributors.py
```

### Step 3: Verify Import
The script will show:
- ✅ Number of distributors added
- 🔄 Number of distributors updated (if already exist)
- ⚠️ Number of distributors skipped (if errors)
- 📊 Total distributors in database

---

## What the Script Does

### 1. Auto-Generate Distributor Codes
- Format: `DIST0001`, `DIST0002`, etc.
- Sequential numbering based on existing distributors

### 2. Set Default Values
- **State:** Bihar
- **State Code:** 10 (Bihar GST code)
- **Margin:** 12%
- **Credit Limit:** ₹50,000
- **Credit Days:** 30 days
- **Payment Terms:** Credit
- **Status:** Active

### 3. Handle Duplicates
- Checks for existing phone numbers
- Updates existing records instead of creating duplicates
- Skips invalid phone numbers (0000000000)

### 4. Normalize Data
- Capitalizes location names (patna → Patna)
- Sets business name = contact person name
- Uses location as territory

---

## After Import

### View Distributors
1. Login to mohi-erp
2. Navigate to **Distributors** menu
3. You should see all 68 distributors listed

### Update Distributor Details
For each distributor, you can add:
- Email address
- GSTIN (if registered)
- PAN number
- Complete address
- Pincode
- Adjust credit limit
- Adjust margin percentage

### Create Orders
Once distributors are imported, you can:
1. Create orders for any distributor
2. Track payments
3. Generate invoices
4. Monitor credit limits

---

## Distributor Fields Populated

| Field | Value | Source |
|-------|-------|--------|
| Code | DIST0001, DIST0002... | Auto-generated |
| Business Name | Hawkar Name | From list |
| Contact Person | Hawkar Name | From list |
| Phone | Contact No | From list |
| City | Location | From list |
| State | Bihar | Default |
| State Code | 10 | Default (Bihar) |
| Territory | Location | From list |
| Margin % | 12% | Default |
| Credit Limit | ₹50,000 | Default |
| Credit Days | 30 | Default |
| Payment Terms | Credit | Default |
| Status | Active | Default |

---

## Fields to Update Later

These fields are set to NULL and can be updated via the UI:

- Email
- GSTIN
- PAN
- Address Line 1
- Address Line 2
- Pincode

---

## Troubleshooting

### Error: "No module named 'app'"
**Solution:** Make sure you're in the correct directory and virtual environment is activated
```cmd
cd D:\OtherRepos\mohierp\mohi-erp
.venv\Scripts\activate
```

### Error: "Database connection failed"
**Solution:** Check if database is running and config is correct in `.env` file

### Duplicate Phone Numbers
**Note:** Some distributors share phone numbers:
- Babloo & Boby: 7903352850
- Multiple entries with same names but different locations

The script handles this by checking phone numbers and updating existing records.

---

## Manual Import Alternative

If you prefer to import via CSV:

### Option 1: Use the CSV file
1. Open `distributors_list.csv`
2. Use the "Add Distributor" form in the UI
3. Copy-paste data for each distributor

### Option 2: Bulk Import (Future Enhancement)
Add a CSV upload feature to the distributors page for bulk imports.

---

## Verification Checklist

After running the import script:

- [ ] Check total distributor count in UI
- [ ] Verify distributor codes are sequential
- [ ] Check a few distributors for correct data
- [ ] Verify phone numbers are correct
- [ ] Check locations are properly capitalized
- [ ] Test creating an order for a distributor
- [ ] Verify credit limit is set to ₹50,000
- [ ] Check margin is set to 12%

---

## Next Steps

1. **Run the import script**
2. **Review imported distributors** in the UI
3. **Update missing details** (email, GSTIN, complete address)
4. **Adjust credit limits** based on distributor size
5. **Adjust margins** based on agreements
6. **Start creating orders** for your distributors

---

## Support

If you encounter any issues:
1. Check the error message from the script
2. Verify database connection
3. Check if virtual environment is activated
4. Review the `scripts/imports/import_distributors.py` script for any modifications needed

---

**Ready to Import?** Run the script now:
```cmd
cd D:\OtherRepos\mohierp\mohi-erp
.venv\Scripts\activate
python scripts/imports/import_distributors.py
```
