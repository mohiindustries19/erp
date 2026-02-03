# 🚀 Quick Start Guide - Mohi Industries ERP

**ॐ श्री गणेशाय नमः**

## 1-Minute Setup

```bash
# Step 1: Navigate to project
cd mohi-erp

# Step 2: Start everything
docker-compose up -d

# Step 3: Wait 30 seconds for database
# (Go make chai ☕)

# Step 4: Initialize database
docker-compose exec web python scripts/db/init_db.py

# Step 5: Open browser
# http://localhost:5000

# Login: admin / admin123
```

## What You Get

✅ **Complete ERP System** for FMCG Manufacturing
✅ **Indian Compliance** - GST, FSSAI, TDS/TCS ready
✅ **Distributor Management** - Territory, margins, credit limits
✅ **Order Management** - Daily bakery + bulk orders
✅ **Inventory & Batches** - FSSAI batch tracking, expiry alerts
✅ **Multi-warehouse** - Track stock across locations
✅ **Modern UI** - Clean, responsive, mobile-friendly

## Key Features for Mohi Industries

### 1. Distributor Portal
- Onboard new distributors
- Set margins (12-18%)
- Credit limits & payment terms
- Territory management

### 2. Product Management
- **Bakery** - 3-5 days shelf life
- **Pickles** - 12 months shelf life  
- **Mohi Neer Water** - 6 months shelf life
- HSN codes & GST rates configured

### 3. Order Processing
- Daily fresh bakery orders
- Bulk orders for pickles/water
- MOQ enforcement (₹25,000)
- GST invoice generation

### 4. FSSAI Compliance
- Batch/lot tracking
- Manufacturing & expiry dates
- Quality control checkpoints
- Traceability reports

### 5. GST Compliance
- CGST/SGST/IGST calculation
- E-invoice ready format
- GSTR report generation
- HSN code tracking

## Default Data Loaded

**Products:**
- BAK001: White Bread 400g
- BAK002: Brown Bread 400g
- BAK003: Pav Bread 6pcs
- PCK001: Mango Pickle 500g
- PCK002: Mixed Pickle 500g
- WAT001: Mohi Neer 500ml
- WAT002: Mohi Neer 1L

**Distributors:**
- DIST0001: Mumbai Retail Traders
- DIST0002: Delhi Food Distributors

**Warehouses:**
- WH01: Main Factory (Mumbai)
- WH02: Delhi Distribution Center
- WH03: Bangalore Hub

## Next Steps

1. **Update Company Details**
   - Edit `.env` file
   - Add your GSTIN, PAN, FSSAI license

2. **Add Your Products**
   - Go to Products → Add New
   - Set HSN codes, GST rates, shelf life

3. **Add Your Distributors**
   - Go to Distributors → Add New
   - Set margins, credit limits

4. **Start Taking Orders**
   - Go to Orders → New Order
   - Select distributor & products

5. **Track Inventory**
   - View stock levels
   - Monitor expiring batches
   - Generate production plans

## Common Tasks

### Add New Product
Dashboard → Products → Add New Product

### Create Order
Dashboard → New Order → Select Distributor → Add Items

### Check Expiring Batches
Dashboard → Expiring Soon (Red button)

### View Reports
Orders → Filter by date range

## Troubleshooting

**Can't access http://localhost:5000?**
```bash
docker-compose ps  # Check if services are running
docker-compose logs web  # Check for errors
```

**Database error?**
```bash
docker-compose restart db
docker-compose exec web python scripts/db/init_db.py
```

**Need to reset everything?**
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec web python scripts/db/init_db.py
```

## Production Deployment

See `DEPLOYMENT.md` for:
- VPS deployment (DigitalOcean, Linode)
- Cloud deployment (Render, Railway)
- SSL setup
- Backup configuration
- Security checklist

## Support

📧 Email: info@mohiindustries.in
📱 Phone: +91 9262650010
🌐 Website: https://mohiindustries.in

---

**Built with ❤️ for Indian FMCG Manufacturing**

*May Lord Ganesha bless your business with prosperity!* 🙏
