# 🚂 Railway Deployment Guide - Mohi Industries ERP

## ✅ Files Created for Railway

All necessary configuration files have been created:

- ✅ `Procfile` - Tells Railway how to start the app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `railway.json` - Railway-specific configuration
- ✅ `.railwayignore` - Excludes unnecessary files
- ✅ `nixpacks.toml` - Build configuration
- ✅ `requirements.txt` - Already has gunicorn

## 🚀 Deployment Steps

### 1. Push to GitHub

```bash
cd mohi-erp
git init
git add .
git commit -m "Initial commit - Ready for Railway deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/mohi-erp.git
git push -u origin main
```

### 2. Deploy on Railway

1. Go to [railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `mohi-erp` repository
5. Railway will auto-detect it's a Python app

### 3. Add PostgreSQL Database

1. In your Railway project, click **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway will automatically:
   - Create a PostgreSQL database
   - Set the `DATABASE_URL` environment variable
   - Link it to your app

### 4. Set Environment Variables

Go to your app service → **"Variables"** tab and add:

```env
# Required
SECRET_KEY=your-super-secret-key-here-change-this
FLASK_ENV=production
AUTO_CREATE_DB=true

# Company Details
COMPANY_NAME=Mohi Industries
COMPANY_GSTIN=10GANPS5418H1ZJ
COMPANY_PAN=XXXXX1234X
COMPANY_STATE=Bihar
COMPANY_STATE_CODE=10
COMPANY_PHONE=+91 9262650010
COMPANY_EMAIL=info@mohiindustries.in

# FSSAI
FSSAI_LICENSE=10423110000282

# Barcode
BARCODE_COMPANY_PREFIX=890123456

# Email (Optional - for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@mohiindustries.in

# WhatsApp (Optional)
WHATSAPP_ENABLED=false
```

**Note**: Railway automatically provides `DATABASE_URL` and `PORT` - don't set these manually!

### 5. Deploy!

Railway will automatically:
- ✅ Install dependencies from `requirements.txt`
- ✅ Run database migrations
- ✅ Start the app with gunicorn
- ✅ Provide a public URL (e.g., `mohi-erp-production.up.railway.app`)

### 6. Initialize Database

After first deployment, you need to create tables:

**Option A: Via Railway CLI**
```bash
railway login
railway link
railway run flask db upgrade
railway run python init_db.py
```

**Option B: Set AUTO_CREATE_DB=true**
Already set in environment variables above - tables will be created automatically on first run.

### 7. Create Admin User

SSH into Railway or use Railway CLI:
```bash
railway run python
```

Then in Python shell:
```python
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    admin = User(
        username='admin',
        email='admin@mohiindustries.in',
        password_hash=generate_password_hash('admin123'),
        role='admin',
        is_active=True
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
```

## 🔧 Configuration Details

### Gunicorn Settings
- **Workers**: 2 (good for Railway's free tier)
- **Timeout**: 120 seconds (for long-running operations)
- **Binding**: `0.0.0.0:$PORT` (Railway provides PORT)

### Database
- Railway PostgreSQL automatically sets `DATABASE_URL`
- Config.py already handles this via `os.environ.get('DATABASE_URL')`

### Static Files
- Flask serves static files automatically
- No need for separate CDN on Railway

## 📊 Monitoring

### View Logs
Railway Dashboard → Your Service → **"Deployments"** tab → Click latest deployment

### Check Resource Usage
Railway Dashboard → **"Usage"** tab
- Monitor your $5 credit usage
- Track CPU, RAM, bandwidth

## ⚠️ Important Notes

### Database URL Fix
Railway provides `DATABASE_URL` starting with `postgres://`, but SQLAlchemy needs `postgresql://`.

Add this to `config.py` if not already there:
```python
# Fix Railway DATABASE_URL
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
SQLALCHEMY_DATABASE_URI = database_url or 'postgresql://localhost/mohi_erp'
```

### Free Tier Limits
- ✅ $5 credit/month (usually enough for small usage)
- ✅ No sleep/downtime
- ⚠️ Credit runs out if heavy traffic

### Security
- ✅ Change `SECRET_KEY` to a strong random value
- ✅ Use strong admin password
- ✅ Enable HTTPS (Railway provides this automatically)

## 🎉 Success!

Once deployed, your ERP will be live at:
```
https://your-app-name.up.railway.app
```

Login with:
- Username: `admin`
- Password: `admin123` (change immediately!)

## 🆘 Troubleshooting

### Build Fails
- Check Railway logs for errors
- Verify all dependencies in `requirements.txt`
- Ensure Python version matches `runtime.txt`

### Database Connection Error
- Verify PostgreSQL service is running
- Check `DATABASE_URL` is set automatically
- Ensure database tables are created

### App Won't Start
- Check Procfile syntax
- Verify gunicorn is in requirements.txt
- Check Railway logs for startup errors

### 500 Internal Server Error
- Check application logs in Railway
- Verify all environment variables are set
- Check database migrations ran successfully

## 📞 Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Your Trial: 26 days or $5.00 remaining

---

**Ready to deploy! 🚀**
