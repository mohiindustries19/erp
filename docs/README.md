# Mohi Industries ERP System

**ॐ श्री गणेशाय नमः**

<div align="center">

![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

**A lightweight, web-based ERP system built specifically for Mohi Industries**

*FMCG Manufacturing | Bakery | Pickles | Packaged Water*

[Quick Start](#-quick-start) • [Features](#-features) • [Deployment](#-deployment) • [Documentation](#-documentation)

</div>

---

## 🎯 Overview

Complete ERP solution for **Mohi Industries** - an FMCG manufacturing company producing:
- 🍞 **Bakery Products** (3-5 days shelf life)
- 🥒 **Pickles** (12 months shelf life)  
- 💧 **Mohi Neer Packaged Water** (6 months shelf life)

Built with **Indian compliance** at its core - GST, FSSAI, TDS/TCS ready.

## ✨ Features

### 🏪 Core Modules
- **Distributor Management** - Territory mapping, margins (12-18%), credit limits
- **Order Management** - Daily bakery orders + bulk orders, MOQ enforcement (₹25,000)
- **Inventory Management** - Multi-warehouse, real-time stock levels
- **Batch Tracking** - FSSAI compliance, expiry alerts, FEFO
- **Production Planning** - Daily schedules, BOM, quality control
- **Finance & Accounting** - GST invoices, payment tracking, TDS/TCS

### 🇮🇳 Indian Compliance
- ✅ **GST** - CGST/SGST/IGST calculation, e-invoice ready, GSTR reports
- ✅ **FSSAI** - Batch/lot tracking, manufacturing & expiry dates, traceability
- ✅ **TDS/TCS** - Automatic calculation, Form 26Q/27EQ data
- ✅ **Legal Metrology** - MRP compliance, pack size tracking

### 🎨 User Experience
- Modern, clean interface
- Mobile responsive
- Fast loading (<2s)
- Intuitive navigation
- Print-friendly invoices

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- 2GB RAM minimum
- 10GB disk space

### Installation (1 Minute)

```bash
# 1. Navigate to project
cd mohi-erp

# 2. Start services
docker-compose up -d

# 3. Wait 30 seconds for database initialization
sleep 30

# 4. Initialize database with sample data
docker-compose exec web python scripts/db/init_db.py

# 5. Open browser
# http://localhost:5000
# Login: admin / admin123
```

**Note on code updates:**
- Local dev with `docker-compose.yml` uses a bind-mount (`.:/app`), so code changes apply immediately inside the container.
- Production (Railway / `docker-compose.prod.yml`) builds a Docker image, so code changes require a **rebuild/redeploy**.

That's it! 🎉

## 📦 What's Included

### Sample Data Loaded
- **7 Products** (Bakery, Pickles, Water)
- **2 Distributors** (Mumbai, Delhi)
- **3 Warehouses** (Mumbai, Delhi, Bangalore)
- **Sample Batches** with FSSAI tracking
- **Admin User** (username: admin, password: admin123)

### Pre-configured
- GST rates (5%, 12%, 18%)
- HSN codes for all products
- Shelf life tracking
- Margin calculations
- Credit limit management

## 🏗️ Tech Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| Backend | Python 3.11 + Flask | Lightweight, easy to maintain |
| Database | PostgreSQL 15 | Robust, ACID compliant |
| Frontend | Tailwind CSS + Alpine.js | Modern, responsive |
| Deployment | Docker Compose | One-command deployment |
| Production | Gunicorn | Multi-worker support |

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│         Web Browser (Any Device)        │
└──────────────┬──────────────────────────┘
               │ HTTPS
               ▼
┌─────────────────────────────────────────┐
│      Flask Application (Python)         │
│  ┌─────────────────────────────────┐   │
│  │ Routes → Business Logic → ORM   │   │
│  └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │ SQL
               ▼
┌─────────────────────────────────────────┐
│      PostgreSQL Database                │
│  (All ERP data with ACID compliance)    │
└─────────────────────────────────────────┘
```

## 🚀 Deployment

### Option 1: VPS (Recommended)
**Providers:** DigitalOcean, Linode, Hetzner  
**Cost:** $5-20/month  
**Setup Time:** 15 minutes

```bash
# SSH into your server
ssh root@your-server-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone and deploy
git clone <your-repo>
cd mohi-erp
cp .env.example .env
nano .env  # Edit your details

docker-compose -f docker-compose.prod.yml up -d
docker-compose exec web python scripts/db/init_db.py
```

### Option 2: PaaS (Easiest)
**Providers:** Render.com, Railway.app  
**Cost:** $10-15/month  
**Setup Time:** 5 minutes

1. Push code to GitHub
2. Connect to Render/Railway
3. Add PostgreSQL database
4. Deploy!

### Option 3: Local Server
**Hardware:** Old PC/Laptop  
**Cost:** Free (electricity only)  
**Best For:** Factory deployment

Same as VPS setup, works offline!

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [START.md](START.md) | Quick start guide |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Detailed deployment instructions |
| [FEATURES.md](FEATURES.md) | Complete feature list |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project overview |

## 🗂️ Project Structure

```
mohi-erp/
├── app/
│   ├── models/              # Database models
│   │   ├── user.py         # Authentication
│   │   ├── company.py      # Company (GSTIN, FSSAI)
│   │   ├── distributor.py  # Distributor network
│   │   ├── product.py      # Products & categories
│   │   ├── inventory.py    # Stock & batches
│   │   └── order.py        # Orders with GST
│   ├── routes/             # API endpoints
│   │   ├── auth.py         # Login/logout
│   │   ├── main.py         # Dashboard
│   │   ├── distributor.py  # Distributor CRUD
│   │   ├── inventory.py    # Inventory management
│   │   └── orders.py       # Order processing
│   └── templates/          # HTML templates
├── docker-compose.yml      # Development
├── docker-compose.prod.yml # Production
├── scripts/              # Helper scripts
│   └── db/init_db.py      # Database setup
└── requirements.txt       # Dependencies
```

## 🔒 Security

- ✅ Password hashing (Werkzeug)
- ✅ Session management (Flask-Login)
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ XSS protection (Flask auto-escaping)
- ✅ CSRF protection (Flask-WTF)
- ✅ Role-based access control

## 📈 Performance

- **Page Load:** <2 seconds
- **Concurrent Users:** 100+
- **Database:** Optimized with indexes
- **Scalability:** Horizontal scaling ready

## 💰 Cost Comparison

| Solution | Cost | Time | Maintenance |
|----------|------|------|-------------|
| Custom Development | ₹5-10 lakhs | 6-12 months | High |
| Odoo/SAP | ₹2-5 lakhs/year | 3-6 months | High |
| **Mohi ERP** | **₹400-1500/month** | **1 minute** | **Low** |

## 🎯 Key Benefits

- ✅ **100% Indian Compliance** - GST, FSSAI, TDS/TCS
- ✅ **Easy Deployment** - One command setup
- ✅ **Low Cost** - $5-20/month hosting
- ✅ **No Licensing Fees** - Open source
- ✅ **Customizable** - Full source code access
- ✅ **Offline Capable** - Works on local server
- ✅ **Mobile Friendly** - Responsive design

## 🤝 Support

- 📧 **Email:** info@mohiindustries.in
- 📱 **Phone:** +91 9262650010
- 🌐 **Website:** https://mohiindustries.in

## 📝 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

Built with:
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Tailwind CSS](https://tailwindcss.com/) - UI framework
- [Alpine.js](https://alpinejs.dev/) - JavaScript framework
- [Docker](https://www.docker.com/) - Containerization

---

<div align="center">

**Built with ❤️ for Indian FMCG Manufacturing**

*May Lord Ganesha bless Mohi Industries with prosperity!* 🙏

**ॐ श्री गणेशाय नमः**

</div>
