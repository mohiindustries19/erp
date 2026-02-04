# 🌐 Generate Public URL for Your ERP

## Quick Steps (2 minutes):

### 1. Open Railway Dashboard
Go to: https://railway.app/project/123d0ab0-c547-4712-9b94-4fd76c27566d

### 2. Click on "erp" Service
Click on the service with the GitHub icon (not Postgres)

### 3. Go to Settings Tab
Click on "Settings" in the top menu

### 4. Scroll to Networking Section
Look for the "Networking" section

### 5. Generate Domain
Click the **"Generate Domain"** button

### 6. Copy Your URL
Railway will create a URL like:
```
https://erp-production.up.railway.app
```

### 7. Open Your ERP
Click on the URL or copy it to your browser

---

## 🔐 First Login

**URL**: Your generated Railway URL  
**Username**: `admin`  
**Password**: `admin123`

⚠️ **IMPORTANT**: Change password immediately after first login!

---

## ⚙️ Set Environment Variables (If Not Done)

Before accessing, make sure these are set in Railway:

1. Click on "erp" service
2. Go to "Variables" tab
3. Add these:

```
SECRET_KEY=your-random-secret-key-here
FLASK_ENV=production
AUTO_CREATE_DB=true
COMPANY_NAME=Mohi Industries
COMPANY_GSTIN=10GANPS5418H1ZJ
COMPANY_PHONE=+91 9262650010
COMPANY_EMAIL=info@mohiindustries.in
FSSAI_LICENSE=10423110000282
BARCODE_COMPANY_PREFIX=890123456
```

**Note**: Railway automatically sets `DATABASE_URL` and `PORT` - don't add these!

---

## 🎉 Your ERP Features

Once logged in, you'll have access to:

✅ Inventory Management  
✅ Batch Tracking & QC  
✅ Order Processing  
✅ Distributor Management  
✅ Payment Tracking  
✅ GST Compliance  
✅ Barcode Generation  
✅ Professional Labels  
✅ Analytics Dashboard  
✅ Email Notifications  
✅ WhatsApp Integration  
✅ AI Chat Assistant  

---

## 📱 Access from Anywhere

Once you have the URL, you can:
- Bookmark it in your browser
- Access from mobile phone
- Share with your team
- Use from any device with internet

---

## 🔒 Security Tips

1. Change admin password immediately
2. Create separate user accounts for staff
3. Use strong passwords
4. Don't share admin credentials
5. Regular backups (Railway does this automatically)

---

## 🆘 Troubleshooting

### Can't Access URL?
- Check if both "erp" and "Postgres" services show green "Online" status
- Wait 1-2 minutes after generating domain
- Check Railway logs for errors

### Login Not Working?
- Default credentials: admin / admin123
- Check if AUTO_CREATE_DB=true is set in variables
- Check deployment logs

### Need to Regenerate URL?
- Go to Settings → Networking
- Click "Remove Domain"
- Click "Generate Domain" again

---

## 📞 Support

**Railway Dashboard**: https://railway.app/project/123d0ab0-c547-4712-9b94-4fd76c27566d

**Railway Docs**: https://docs.railway.app

**Your GitHub Repo**: https://github.com/mohiindustries19/erp

---

**Ready to access your ERP! Just click "Generate Domain" in Railway Settings!** 🚀
