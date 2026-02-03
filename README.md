# 🏭 Mohi Industries ERP

**Complete ERP System for Food Manufacturing & Distribution**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)]()

---

## 🎯 Overview

Mohi Industries ERP is a comprehensive enterprise resource planning system designed specifically for food manufacturing and distribution businesses in India. Built with Flask and PostgreSQL, it handles everything from inventory management to GST compliance.

---

## ✨ Key Features

### 📦 Inventory Management
- Product catalog with categories
- Multi-warehouse support
- Batch tracking with expiry dates
- Stock level alerts & reorder points
- EAN-13 barcode generation
- Professional retail labels

### 🏪 Distribution Management
- Distributor onboarding & KYC
- Territory-based distribution
- Credit limit management
- Performance tracking
- Customer satisfaction scoring

### 📋 Order Processing
- Order creation & tracking
- Distributor-wise orders
- Payment tracking (pending/partial/paid)
- GST calculations (CGST/SGST/IGST)
- Invoice generation

### 🔬 Quality Control
- Batch-wise QC checks
- Multiple test parameters
- Pass/Fail tracking
- QC reports & certificates
- Batch recall management

### 💰 Financial Management
- Payment tracking & reminders
- GST compliance & reports
- Receivables management
- Payment history
- Bank reconciliation

### 📊 Analytics & Reports
- Sales analytics
- Distributor performance
- Inventory reports
- Payment tracking
- GST reports
- Excel exports

### 🤖 Advanced Features
- AI chat assistant (Groq)
- Email notifications
- WhatsApp integration (Twilio)
- Document generation (PDF)
- Barcode printing
- Multi-user with role-based access

---

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/mohi-erp.git
cd mohi-erp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your settings

# Initialize database
flask db upgrade
python init_railway_db.py

# Run application
python run.py
```

Access at: http://localhost:5000

**Default Login:**
- Username: `admin`
- Password: `admin123`

---

## 🚂 Deploy to Railway

**Quick Deploy (3 Steps):**

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - New Project → Deploy from GitHub
   - Add PostgreSQL database

3. **Set Environment Variables**
   ```
   SECRET_KEY=your-secret-key
   FLASK_ENV=production
   AUTO_CREATE_DB=true
   ```

**Detailed Guide:** See [DEPLOY_NOW.md](DEPLOY_NOW.md)

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

### Frontend
- **CSS**: Tailwind CSS
- **JavaScript**: Vanilla JS
- **Charts**: Chart.js
- **Icons**: Emoji & Unicode

### Integrations
- **AI**: Groq API
- **Email**: Flask-Mail (SMTP)
- **WhatsApp**: Twilio API
- **Barcode**: python-barcode
- **PDF**: ReportLab, WeasyPrint
- **Excel**: openpyxl, pandas

---

## 📋 Requirements

- Python 3.11+
- PostgreSQL 15+
- 512MB RAM minimum
- 1GB storage minimum

---

## 🔧 Configuration

### Environment Variables

```env
# Flask
SECRET_KEY=your-secret-key
FLASK_ENV=production

# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Company Details
COMPANY_NAME=Mohi Industries
COMPANY_GSTIN=10GANPS5418H1ZJ
COMPANY_PHONE=+91 9262650010
COMPANY_EMAIL=info@mohiindustries.in
FSSAI_LICENSE=10423110000282

# Barcode
BARCODE_COMPANY_PREFIX=890123456

# Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# WhatsApp (Optional)
WHATSAPP_ENABLED=false
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
```

---

## 📁 Project Structure

```
mohi-erp/
├── app/
│   ├── __init__.py          # App factory
│   ├── models/              # Database models
│   ├── routes/              # Route blueprints
│   ├── templates/           # Jinja2 templates
│   ├── static/              # CSS, JS, images
│   └── utils/               # Helper functions
├── migrations/              # Database migrations
├── config.py                # Configuration
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── Procfile                 # Railway start command
├── runtime.txt              # Python version
└── README.md                # This file
```

---

## 🔒 Security

- ✅ Password hashing (Werkzeug)
- ✅ CSRF protection (Flask-WTF)
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ Rate limiting (Flask-Limiter)
- ✅ Secure session management
- ✅ Environment-based secrets

---

## 📊 Database Schema

### Core Tables
- `users` - User accounts & authentication
- `companies` - Company profile
- `products` - Product catalog
- `batches` - Batch tracking
- `inventory` - Stock levels
- `warehouses` - Warehouse locations
- `distributors` - Distributor management
- `orders` - Order processing
- `payments` - Payment tracking
- `batch_quality_checks` - QC records

---

## 🎨 Features by Module

### Inventory Module
- Products, Categories, Warehouses
- Batch tracking with expiry
- Stock alerts & reorder points
- Barcode generation & printing

### Distribution Module
- Distributor onboarding
- Territory management
- Credit limits & terms
- Performance tracking

### Orders Module
- Order creation & tracking
- GST calculations
- Invoice generation
- Payment tracking

### QC Module
- Batch quality checks
- Test parameters
- Pass/Fail tracking
- QC certificates

### Analytics Module
- Sales dashboard
- Distributor performance
- Inventory reports
- Payment tracking

---

## 🌐 Indian Compliance

### GST Compliance
- ✅ CGST/SGST/IGST calculations
- ✅ State-wise GST handling
- ✅ GST reports & returns
- ✅ GSTIN validation

### FSSAI Compliance
- ✅ License tracking
- ✅ Batch traceability
- ✅ Expiry date management
- ✅ Product labeling

### Legal Metrology
- ✅ MRP display on labels
- ✅ Net weight declaration
- ✅ Manufacturing date
- ✅ Best before date

---

## 📱 Mobile Responsive

All pages are mobile-responsive with Tailwind CSS. Works on:
- 📱 Mobile phones
- 📱 Tablets
- 💻 Laptops
- 🖥️ Desktops

---

## 🤝 Contributing

This is a proprietary project for Mohi Industries. Internal contributions welcome.

---

## 📄 License

Proprietary - All rights reserved by Mohi Industries

---

## 📞 Support

- **Email**: info@mohiindustries.in
- **Phone**: +91 9262650010
- **Address**: B-61, P-1, BIADA, Hajipur, Vaishali, Bihar - 844102

---

## 🙏 Credits

**Developed for Mohi Industries**

Built with ❤️ using Flask, PostgreSQL, and Tailwind CSS

---

## 📚 Documentation

- [Deployment Guide](DEPLOY_NOW.md)
- [Railway Deployment](RAILWAY_DEPLOYMENT.md)
- [Barcode System](BARCODE_SYSTEM_COMPLETE.md)
- [Professional Labels](PROFESSIONAL_LABEL_COMPLETE.md)

---

**ॐ श्री गणेशाय नमः** 🙏
