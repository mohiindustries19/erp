# ✅ Pre-Deployment Checklist

## Before You Deploy to Railway

Go through this checklist to ensure everything is ready:

---

## 📋 Code Preparation

- [x] All configuration files created
  - [x] Procfile
  - [x] runtime.txt
  - [x] nixpacks.toml
  - [x] .railwayignore
  - [x] init_railway_db.py

- [x] Code updates completed
  - [x] config.py - DATABASE_URL handling fixed
  - [x] main.py - Health check endpoint added
  - [x] barcode_generator.py - Address updated

- [x] Dependencies verified
  - [x] requirements.txt includes gunicorn
  - [x] All packages have correct versions
  - [x] No conflicting dependencies

---

## 🔐 Security

- [ ] Change SECRET_KEY from default
  - Current: `dev-secret-key-change-in-production`
  - Generate new: `python -c "import secrets; print(secrets.token_hex(32))"`

- [ ] Review sensitive data
  - [ ] No passwords in code
  - [ ] No API keys in code
  - [ ] .env file in .gitignore

- [ ] Admin credentials
  - [ ] Plan to change default password after first login
  - [ ] Strong password policy in place

---

## 🗄️ Database

- [ ] PostgreSQL will be added on Railway
- [ ] Database initialization script ready (init_railway_db.py)
- [ ] Migration files present (if using Flask-Migrate)
- [ ] Backup strategy planned

---

## ⚙️ Environment Variables

Prepare these values before deployment:

### Required
- [ ] `SECRET_KEY` - Generate random value
- [ ] `FLASK_ENV` - Set to "production"
- [ ] `AUTO_CREATE_DB` - Set to "true" for first deploy

### Company Details
- [ ] `COMPANY_NAME` - Mohi Industries
- [ ] `COMPANY_GSTIN` - 10GANPS5418H1ZJ
- [ ] `COMPANY_PHONE` - +91 9262650010
- [ ] `COMPANY_EMAIL` - info@mohiindustries.in
- [ ] `FSSAI_LICENSE` - 10423110000282

### Optional (Email)
- [ ] `MAIL_SERVER` - smtp.gmail.com
- [ ] `MAIL_USERNAME` - Your email
- [ ] `MAIL_PASSWORD` - App password (not regular password!)

### Optional (WhatsApp)
- [ ] `WHATSAPP_ENABLED` - false (enable later)
- [ ] `TWILIO_ACCOUNT_SID` - If using Twilio
- [ ] `TWILIO_AUTH_TOKEN` - If using Twilio

---

## 📦 GitHub Repository

- [ ] Create GitHub repository
  - Repository name: `mohi-erp`
  - Visibility: Private (recommended)

- [ ] Initialize git
  ```bash
  cd d:\OtherRepos\mohierp\mohi-erp
  git init
  ```

- [ ] Add all files
  ```bash
  git add .
  ```

- [ ] Commit
  ```bash
  git commit -m "Initial commit - Ready for Railway deployment"
  ```

- [ ] Add remote
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/mohi-erp.git
  ```

- [ ] Push to GitHub
  ```bash
  git branch -M main
  git push -u origin main
  ```

---

## 🚂 Railway Setup

- [ ] Railway account created
  - Already done! ✅ (Trial Plan active)

- [ ] GitHub connected to Railway
  - Connect in Railway dashboard

- [ ] Credit card added (optional)
  - Not required for trial
  - Add later if needed

---

## 🧪 Testing Plan

After deployment, test these features:

### Authentication
- [ ] Login with admin credentials
- [ ] Change admin password
- [ ] Create new user
- [ ] Test role-based access

### Core Features
- [ ] Create product
- [ ] Generate barcode
- [ ] Print label
- [ ] Create batch
- [ ] Add QC check
- [ ] Create order
- [ ] Track payment

### Reports
- [ ] View dashboard
- [ ] Export Excel reports
- [ ] Generate invoices
- [ ] View analytics

---

## 📊 Monitoring Setup

- [ ] Railway dashboard bookmarked
- [ ] Understand how to view logs
- [ ] Know how to check resource usage
- [ ] Understand credit consumption

---

## 📞 Support Resources

- [ ] Railway docs bookmarked: https://docs.railway.app
- [ ] Railway Discord joined: https://discord.gg/railway
- [ ] Deployment guides saved locally

---

## 🎯 Post-Deployment Tasks

After successful deployment:

1. [ ] Initialize database
   ```bash
   railway run python init_railway_db.py
   ```

2. [ ] Login and change admin password

3. [ ] Create company profile
   - Update company details
   - Add logo
   - Configure settings

4. [ ] Add initial data
   - [ ] Product categories
   - [ ] Warehouses
   - [ ] Products
   - [ ] Distributors

5. [ ] Configure integrations
   - [ ] Email settings
   - [ ] WhatsApp (if needed)
   - [ ] AI chat (if needed)

6. [ ] Create user accounts
   - [ ] Admin users
   - [ ] Manager users
   - [ ] Staff users

7. [ ] Test all features
   - [ ] Create test orders
   - [ ] Generate test reports
   - [ ] Print test labels

8. [ ] Train users
   - [ ] Create user guide
   - [ ] Conduct training session
   - [ ] Share login credentials

---

## ⚠️ Important Notes

### Before Going Live
- ✅ Test thoroughly in staging
- ✅ Backup existing data (if migrating)
- ✅ Inform users of new system
- ✅ Have rollback plan ready

### Security Best Practices
- ✅ Use strong passwords
- ✅ Enable 2FA on Railway account
- ✅ Regular security audits
- ✅ Keep dependencies updated

### Performance
- ✅ Monitor resource usage
- ✅ Optimize slow queries
- ✅ Add indexes if needed
- ✅ Scale up if traffic increases

---

## 🚀 Ready to Deploy?

If all items are checked, you're ready to deploy!

**Next Steps:**
1. Read [DEPLOY_NOW.md](DEPLOY_NOW.md)
2. Follow step-by-step instructions
3. Deploy to Railway
4. Test everything
5. Go live! 🎉

---

## 📝 Deployment Log

Keep track of your deployment:

```
Date: _______________
Time: _______________
Deployed by: _______________
Railway URL: _______________
Database: _______________
Status: _______________
Notes: _______________
```

---

**Good luck with your deployment!** 🚀

If you encounter any issues, check:
1. Railway logs
2. RAILWAY_DEPLOYMENT.md troubleshooting section
3. Railway Discord for help

**You got this!** 💪
