# Mohi Industries ERP - Quick Reference Card

## 🚀 Quick Commands

### Start Application
```bash
cd mohi-erp
docker-compose up -d
```

### Stop Application
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f web
```

### Reset Database
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec web python scripts/db/init_db.py
```

### Backup Database
```bash
docker-compose exec db pg_dump -U mohi_admin mohi_erp > backup.sql
```

### Restore Database
```bash
docker-compose exec -T db psql -U mohi_admin mohi_erp < backup.sql
```

## 🔑 Default Credentials

**Username:** admin  
**Password:** admin123

⚠️ **Change immediately in production!**

## 📱 Access URLs

| Environment | URL |
|-------------|-----|
| Development | http://localhost:5000 |
| Production | https://your-domain.com |

## 🗂️ Key Modules

| Module | URL | Purpose |
|--------|-----|---------|
| Dashboard | `/` | Overview & stats |
| Distributors | `/distributors` | Manage distributors |
| Products | `/inventory/products` | Product catalog |
| Orders | `/orders` | Order management |
| Inventory | `/inventory` | Stock levels |
| Batches | `/inventory/batches` | FSSAI tracking |
| Expiring | `/inventory/batches/expiring` | Expiry alerts |

## 📊 Database Tables

| Table | Purpose |
|-------|---------|
| users | User authentication |
| company | Company profile (GSTIN, FSSAI) |
| distributors | Distributor network |
| product_categories | Bakery, Pickles, Water |
| products | Product master |
| warehouses | Storage locations |
| inventory | Stock levels |
| batches | FSSAI batch tracking |
| orders | Sales orders |
| order_items | Order line items |

## 🇮🇳 Indian Compliance

### GST Rates
- **Bakery:** 5%
- **Pickles:** 12%
- **Water:** 18%

### HSN Codes
- **Bakery:** 19059020
- **Pickles:** 20019000
- **Water:** 22021000

### Required Fields
- GSTIN (15 digits)
- PAN (10 digits)
- FSSAI License (14 digits)
- State Code (2 digits)

## 📦 Product Categories

| Category | Code | Shelf Life | GST |
|----------|------|------------|-----|
| Bakery Products | BAK | 3-5 days | 5% |
| Pickles | PCK | 12 months | 12% |
| Mohi Neer Water | WAT | 6 months | 18% |

## 💼 Business Rules

| Rule | Value |
|------|-------|
| Minimum Order Value | ₹25,000 |
| Distributor Margin | 12-18% |
| Expiry Alert | 30 days |
| Batch Tracking | Mandatory |
| FEFO | First Expiry First Out |

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables |
| `config.py` | Application config |
| `docker-compose.yml` | Development setup |
| `docker-compose.prod.yml` | Production setup |

## 📝 Common Tasks

### Add New Distributor
1. Go to Distributors → Add Distributor
2. Fill business details
3. Add GSTIN, PAN
4. Set margin % (12-18%)
5. Set credit limit
6. Save

### Create Order
1. Go to Orders → New Order
2. Select distributor
3. Add products & quantities
4. System calculates GST
5. Confirm order

### Check Expiring Batches
1. Dashboard → Expiring Soon (Red button)
2. Or: Inventory → Batches → Filter by expiry

### Generate Invoice
1. Go to Orders
2. Click on order number
3. Click "Generate Invoice"
4. Print or download PDF

## 🐛 Troubleshooting

### Can't access application?
```bash
docker-compose ps  # Check if running
docker-compose logs web  # Check errors
```

### Database connection error?
```bash
docker-compose restart db
sleep 10
docker-compose restart web
```

### Forgot admin password?
```bash
docker-compose exec web python
>>> from app import create_app, db
>>> from app.models import User
>>> app = create_app()
>>> with app.app_context():
...     user = User.query.filter_by(username='admin').first()
...     user.set_password('newpassword')
...     db.session.commit()
```

### Port 5000 already in use?
Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Change 5000 to 8080
```

## 📞 Support Contacts

| Type | Contact |
|------|---------|
| Email | info@mohiindustries.in |
| Phone | +91 9262650010 |
| Website | https://mohiindustries.in |

## 🔐 Security Checklist

- [ ] Change default admin password
- [ ] Update SECRET_KEY in .env
- [ ] Update database password
- [ ] Enable firewall (ufw)
- [ ] Setup SSL certificate
- [ ] Configure automated backups
- [ ] Update company GSTIN, PAN, FSSAI

## 📈 Performance Tips

1. **Database:** Add indexes on frequently queried columns
2. **Caching:** Enable Redis for session storage
3. **Static Files:** Use CDN for CSS/JS
4. **Images:** Compress product images
5. **Queries:** Use pagination for large datasets

## 🔄 Update Application

```bash
cd mohi-erp
git pull origin main
docker-compose down
docker-compose build
docker-compose up -d
```

## 💾 Backup Schedule

| Frequency | What | Command |
|-----------|------|---------|
| Daily | Database | `pg_dump` |
| Weekly | Full backup | `tar -czf` |
| Monthly | Archive | Copy to cloud |

## 📊 Reports Available

- Sales by distributor
- Sales by product
- Sales by territory
- Inventory status
- Expiring batches
- Outstanding payments
- GST summary (GSTR-1, GSTR-3B)
- Batch traceability

## 🎯 Key Metrics to Monitor

- Total active distributors
- Pending orders
- Low stock items
- Expiring batches (30 days)
- Outstanding receivables
- Daily production
- Order fulfillment rate

## 🔗 Useful Links

- [Full Documentation](README.md)
- [Quick Start Guide](START.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Feature List](FEATURES.md)
- [Architecture](ARCHITECTURE.md)

---

**Print this page and keep it handy!** 📄

**ॐ श्री गणेशाय नमः** 🙏
