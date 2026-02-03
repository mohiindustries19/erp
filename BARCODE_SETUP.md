# Barcode System Setup Guide

## Installation

### 1. Install Required Python Packages

```bash
pip install python-barcode[images] reportlab pillow
```

Or add to requirements.txt:
```
python-barcode[images]==0.15.1
reportlab==4.0.7
Pillow==10.1.0
```

### 2. Run Database Migration

```bash
# From mohi-erp directory
flask db upgrade
```

Or run the SQL manually:
```sql
ALTER TABLE products ADD COLUMN ean_barcode VARCHAR(13);
ALTER TABLE products ADD COLUMN barcode_source VARCHAR(32);
ALTER TABLE products ADD COLUMN barcode_registered_date DATE;
CREATE UNIQUE INDEX ix_products_ean_barcode ON products(ean_barcode);
```

## Features

### 1. EAN-13 Barcode Generation
- Auto-generate sequential EAN-13 barcodes
- Manual entry for GS1-registered barcodes
- Check digit validation
- Duplicate prevention

### 2. Barcode Management
- View barcode on product page
- Download barcode image (PNG)
- Update/remove barcodes
- Track barcode source (GS1/Reseller/Internal)

### 3. Label Printing
- Professional product labels with:
  - EAN-13 barcode
  - Product name
  - MRP
  - Pack size
  - Batch number (optional)
  - Mfg/Exp dates (optional)
- Print multiple labels on A4 sheet (40mm x 25mm)
- Export as PDF

### 4. Bulk Operations
- Generate barcodes for multiple products
- Select products without barcodes
- Sequential generation with company prefix

## Usage

### Access Barcode Features

1. **From Products List:**
   - Click "📊 Barcode" button next to any product
   - Click "📊 Bulk Barcodes" in header for bulk generation

2. **Barcode Management Page:**
   - View current barcode
   - Auto-generate new barcode
   - Manually enter GS1 barcode
   - Download barcode image
   - Print labels

### Company Prefix Configuration

**Default:** `890123456` (India country code + sample prefix)

**To Update:**
1. Register with GS1 India: https://www.gs1india.org
2. Get your company prefix (7-9 digits)
3. Update in:
   - `app/utils/barcode_generator.py` - Line 13: `DEFAULT_COMPANY_PREFIX`
   - Or enter manually when generating barcodes

### GS1 India Registration

**For Retail Sales (Required):**
- Website: https://www.gs1india.org
- Cost: ₹5,000 - ₹25,000/year (based on company size)
- Benefits:
  - Unique company prefix
  - Unlimited product barcodes
  - Accepted by all major retailers
  - Global recognition

**Retailers Requiring GS1:**
- Big Bazaar
- Reliance Fresh/Smart
- D-Mart
- Spencer's
- More Supermarket
- All major retail chains

## API Endpoints

### Product Barcode
- `GET /barcode/product/<id>` - View barcode page
- `POST /barcode/product/<id>/generate` - Auto-generate barcode
- `POST /barcode/product/<id>/update` - Update barcode manually
- `GET /barcode/product/<id>/image` - Download barcode image
- `GET /barcode/product/<id>/label` - Download product label
- `GET /barcode/product/<id>/print-labels?count=10` - Print multiple labels PDF

### Bulk Operations
- `GET /barcode/bulk-generate` - Bulk generation page
- `POST /barcode/bulk-generate` - Generate for selected products

### Validation
- `POST /barcode/validate` - AJAX barcode validation

## Barcode Format

### EAN-13 Structure
```
8 9 0 1 2 3 4 5 6 7 8 9 0
│ │ └─────┬─────┘ └─┬─┘ │
│ │       │         │   └─ Check Digit (auto-calculated)
│ │       │         └───── Product Code (3-5 digits)
│ │       └─────────────── Company Prefix (5-7 digits)
│ └─────────────────────── Country Code (890 = India)
└───────────────────────── Country Code continued
```

### Check Digit Calculation
- Automatically calculated using EAN-13 algorithm
- Validates barcode integrity
- Prevents scanning errors

## Label Specifications

### Standard Retail Label (40mm x 25mm)
- Product name (truncated if long)
- Pack size
- MRP (₹)
- Batch number (if selected)
- Manufacturing date
- Expiry date
- EAN-13 barcode

### A4 Sheet Layout
- Labels per row: 5
- Labels per column: 11
- Total per sheet: 55 labels
- Margins: 10mm all sides

## Troubleshooting

### "No module named 'barcode'"
```bash
pip install python-barcode[images]
```

### "No module named 'reportlab'"
```bash
pip install reportlab
```

### "Invalid EAN-13 code"
- Must be exactly 13 digits
- Check digit must be valid
- Use validation endpoint to verify

### "Barcode already exists"
- Each barcode must be unique
- Check if another product has the same code
- Generate new barcode or update existing

### Font errors in labels
- System will use default font if Arial not found
- Install Arial font or update font path in `barcode_generator.py`

## Security Notes

- Only authenticated users can access barcode features
- Barcode validation prevents duplicates
- Company prefix should be kept confidential
- GS1 barcodes should be marked as "gs1" source

## Future Enhancements

- [ ] Barcode scanning for inventory
- [ ] QR code generation
- [ ] Batch barcode printing
- [ ] Barcode history tracking
- [ ] Integration with POS systems
- [ ] Mobile barcode scanning app

## Support

For issues or questions:
1. Check this documentation
2. Verify GS1 registration status
3. Test with internal barcodes first
4. Contact GS1 India for prefix issues
