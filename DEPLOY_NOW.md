# 🚀 Deploy to Railway - Quick Start

## ✅ Your ERP is Ready for Deployment!

All configuration files have been created. Follow these simple steps:

---

## 📋 Step 1: Push to GitHub

```bash
cd d:\OtherRepos\mohierp\mohi-erp

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Railway deployment"

# Create GitHub repo and push
# Go to github.com → New Repository → Create "mohi-erp"
# Then:
git remote add origin https://github.com/YOUR_USERNAME/mohi-erp.git
git branch -M main
git push -u origin main
```

---

## 🚂 Step 2: Deploy on Railway

### A. Create New Project
1. Go to https://railway.app (you're already logged in!)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose **"mohi-erp"** repository
5. Railway will start building automatically

### B. Add PostgreSQL Database
1. In your project, click **"New"** → **"Database"**
2. Select **"Add PostgreSQL"**
3. Done! Railway auto-connects it to your app

---

## ⚙️ Step 3: Set Environment Variables

Click on your app service → **"Variables"** tab → Add these:

### Required Variables:
```
SECRET_KEY=change-this-to-random-secret-key-xyz123
FLASK_ENV=production
AUTO_CREATE_DB=true
```

### Company Details:
```
COMPANY_NAME=Mohi Industries
COMPANY_GSTIN=10GANPS5418H1ZJ
COMPANY_PHONE=+91 9262650010
COMPANY_EMAIL=info@mohiindustries.in
FSSAI_LICENSE=10423110000282
BARCODE_COMPANY_PREFIX=890123456
```

**Note**: Railway automatically sets `DATABASE_URL` and `PORT` - don't add these!

---

## 🎯 Step 4: Initialize Database

After deployment completes, run this command:

### Option A: Via Railway Dashboard
1. Go to your service → **"Settings"** → **"Deploy"**
2. Wait for deployment to finish
3. Go to **"Settings"** → **"Service"** → Click **"New Deployment"**

### Option B: Via Railway CLI (Recommended)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run initialization
railway run python init_railway_db.py
```

This creates:
- ✅ Database tables
- ✅ Admin user (username: `admin`, password: `admin123`)
- ✅ Company profile

---

## 🌐 Step 5: Access Your ERP

Railway will provide a URL like:
```
https://mohi-erp-production.up.railway.app
```

**Login:**
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANT**: Change the admin password immediately after first login!

---

## 📊 Monitor Your Deployment

### View Logs
Railway Dashboard → Your Service → **"Deployments"** → Click latest

### Check Usage
Railway Dashboard → **"Usage"** tab
- You have **$5 credit** (26 days remaining)
- Monitor CPU, RAM, bandwidth

---

## ✅ What's Deployed

Your ERP includes:
- ✅ User authentication & roles
- ✅ Product & inventory management
- ✅ Batch tracking with QC
- ✅ EAN-13 barcode generation
- ✅ Professional retail labels
- ✅ Order management
- ✅ Distributor management
- ✅ GST compliance
- ✅ Payment tracking
- ✅ Analytics dashboard
- ✅ AI chat assistant
- ✅ Email notifications
- ✅ WhatsApp integration
- ✅ Document generation

---

## 🆘 Troubleshooting

### Build Failed?
- Check Railway logs for errors
- Verify GitHub repo has all files
- Ensure `requirements.txt` is correct

### Can't Connect to Database?
- Verify PostgreSQL service is running in Railway
- Check that `DATABASE_URL` is automatically set
- Wait 1-2 minutes after adding database

### App Shows Error?
- Check deployment logs in Railway
- Verify all environment variables are set
- Run `railway run python init_railway_db.py`

### Need Help?
- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

---

## 🎉 You're All Set!

Your Mohi Industries ERP is production-ready and configured for Railway deployment.

**Next Steps:**
1. Push to GitHub ✅
2. Deploy on Railway ✅
3. Add PostgreSQL ✅
4. Set environment variables ✅
5. Initialize database ✅
6. Login and start using! 🚀

---

**Questions? Just ask!** 💬
