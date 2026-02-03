# 🚀 Barcode System - Quick Start Guide

## ⚡ 3-Step Setup

### Step 1: Install (2 minutes)
```bash
cd mohi-erp
install_barcode.bat
```

### Step 2: Configure Company Prefix (1 minute)
Edit `app/utils/barcode_generator.py` line 13:
```python
DEFAULT_COMPANY_PREFIX = "890123456"  # Your GS1 prefix
```

### Step 3: Start Using! (Immediate)
1. Go to Products page
2. Click "📊 Barcode" on any product
3. Click "⚡ Generate Barcode"
4. Done! ✅

---

## 🎯 Common Tasks

### Generate Barcode for One Product
1. Products → Click "📊 Barcode"
2. Enter company prefix
3. Click "⚡ Generate Barcode"
4. Download or print labels

### Generate Barcodes for Many Products
1. Products → Click "📊 Bulk Barcodes"
2. Select products
3. Click "⚡ Generate Selected Barcodes"
4. Done!

### Print Product Labels
1. Open product barcode page
2. Click "🖨️ Print Labels"
3. Choose quantity (1-100)
4. Download PDF
5. Print on A4 paper

### Enter GS1-Registered Barcode
1. Products → Click "📊 Barcode"
2. Scroll to "Manual Entry"
3. Enter 13-digit EAN code
4. Select "GS1 Registered"
5. Click "💾 Save Barcode"

---

## 📋 Barcode Format

```
8901234567890
│││└────┬────┘│
│││     │     └─ Check digit (auto)
│││     └─────── Product code (yours)
││└───────────── Company prefix (GS1)
│└────────────── India code
└─────────────── India code
```

---

## 🏪 For Retail Sales

### Required: GS1 Registration
- **Website:** https://www.gs1india.org
- **Cost:** ₹5,000-₹25,000/year
- **Get:** Unique company prefix
- **Use:** Generate unlimited barcodes

### Accepted By:
✅ Big Bazaar
✅ Reliance Fresh/Smart
✅ D-Mart
✅ Spencer's
✅ More Supermarket
✅ All major retail chains

---

## 🎨 Label Contents

Standard retail label includes:
- ✅ EAN-13 barcode
- ✅ Product name
- ✅ MRP (₹)
- ✅ Pack size
- ✅ Batch number
- ✅ Mfg/Exp dates

**Size:** 40mm x 25mm (standard retail)
**Format:** PDF on A4 sheet

---

## ⚠️ Important Notes

1. **Testing:** Use "Internal" source for testing
2. **Production:** Use "GS1" source for retail
3. **Unique:** Each barcode must be unique
4. **Validation:** System auto-validates check digit
5. **Duplicates:** System prevents duplicate barcodes

---

## 🔧 Troubleshooting

### "No module named 'barcode'"
```bash
pip install python-barcode[images]
```

### "Invalid EAN-13 code"
- Must be exactly 13 digits
- Check digit must be valid
- Use validation to verify

### "Barcode already exists"
- Each product needs unique barcode
- Check if another product has it
- Generate new barcode

---

## 📞 Quick Links

- **GS1 India:** https://www.gs1india.org
- **Full Guide:** `BARCODE_SETUP.md`
- **Complete Docs:** `BARCODE_SYSTEM_COMPLETE.md`

---

## ✅ Ready to Sell in Retail!

Your products are now ready for:
- Malls
- Supermarkets
- Retail chains
- Online marketplaces

**Happy Selling! 🎉**
