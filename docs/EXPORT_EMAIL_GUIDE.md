# Invoice Export & Email Feature Guide

**Date:** January 29, 2026  
**Feature:** Export invoices to PDF/Excel and send via email

---

## 🎯 Features Added

### 1. Export to PDF
- Download invoice as professional PDF file
- Same design as print version (black theme)
- Filename: `Invoice_ORD20260129001.pdf`
- Ready to share or archive

### 2. Export to Excel
- Download invoice data as Excel spreadsheet
- Professional formatting with colors
- Includes all invoice details:
  - Company header
  - Invoice details
  - Customer information
  - Line items with calculations
  - GST breakdown
  - Payment status
- Filename: `Invoice_ORD20260129001.xlsx`
- Ready for accounting/analysis

### 3. Send via Email
- Email invoice directly to distributor
- PDF attachment included
- Professional email template
- Options:
  - **To:** Distributor's email (from profile)
  - **CC:** Your email (info@mohiindustries.in)
  - **Custom:** Enter any email address

---

## 📍 Where to Find

**Location:** Orders → View Order → Top buttons

**New Buttons:**
1. 🖨️ **Print Invoice** - Opens print preview
2. 📄 **Export PDF** - Downloads PDF file
3. 📊 **Export Excel** - Downloads Excel file
4. 📧 **Send Email** - Opens email modal

---

## 🚀 How to Use

### Export PDF
1. Go to Orders → View any order
2. Click **"📄 Export PDF"** button
3. PDF downloads automatically
4. Open with any PDF reader
5. Share via WhatsApp/email

### Export Excel
1. Go to Orders → View any order
2. Click **"📊 Export Excel"** button
3. Excel file downloads automatically
4. Open with Microsoft Excel/Google Sheets
5. Use for accounting/analysis

### Send Email
1. Go to Orders → View any order
2. Click **"📧 Send Email"** button
3. Email modal opens with:
   - **To Email:** Pre-filled with distributor's email
   - **CC Email:** Pre-filled with your email (optional)
4. Verify/edit email addresses
5. Click **"Send Email"**
6. Invoice sent with PDF attachment!

---

## 📧 Email Template

**Subject:** Invoice {order_number} - Mohi Industries

**Body:**
```
Dear {Distributor Name},

Please find attached invoice for your order.

Invoice Details:
- Invoice No: ORD20260129001
- Date: 29-01-2026
- Total Amount: ₹10,000.00
- Amount Paid: ₹5,000.00
- Balance Due: ₹5,000.00

Payment Terms: Credit

Bank Details:
Bank Name: State Bank of India
Account No: 1234567890
IFSC Code: SBIN0001234
Branch: Hajipur

Thank you for your business!

Best regards,
Mohi Industries
Phone: +91 9262650010
Email: info@mohiindustries.in
```

**Attachment:** Invoice_ORD20260129001.pdf

---

## 📊 Excel Format

### Sheet Structure:

**Header Section:**
- Company name (MOHI INDUSTRIES)
- Address
- Contact details
- GSTIN

**Invoice Details:**
- Invoice number
- Date
- Status
- Payment status

**Customer Details:**
- Business name
- Address
- GSTIN
- Contact

**Items Table:**
| # | Product | HSN | Qty | Rate | Disc% | Taxable | GST% | Amount |
|---|---------|-----|-----|------|-------|---------|------|--------|
| 1 | Bread   | 1905| 100 | ₹32  | 0%    | ₹3,200  | 5%   | ₹3,360 |

**Totals:**
- Subtotal
- Discount
- Taxable Amount
- CGST/SGST or IGST
- **TOTAL AMOUNT** (highlighted in red)

**Payment Status:**
- Amount Paid
- Balance Due (highlighted in red)

**Formatting:**
- Red headers (#D00000)
- Professional borders
- Bold totals
- Color-coded status

---

## ⚙️ Setup Required

### 1. Install Dependencies

```cmd
cd D:\OtherRepos\mohierp\mohi-erp
.venv\Scripts\activate
pip install weasyprint openpyxl
```

### 2. Email Configuration

Already configured in `.env`:
```
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=apikey
MAIL_PASSWORD=SG.oHHc_AaqQfeiWcl5jN2N5g...
MAIL_DEFAULT_SENDER=info@mohiindustries.in
```

### 3. Distributor Email

Make sure distributors have email addresses:
1. Go to Distributors → Edit
2. Add email address
3. Save

---

## 🎯 Use Cases

### Daily Operations:
1. **Create Order** → **Export PDF** → Share on WhatsApp
2. **Create Order** → **Send Email** → Automatic delivery
3. **Create Order** → **Export Excel** → Import to Tally

### Month-End:
1. Export all invoices to Excel
2. Consolidate for accounting
3. GST filing preparation

### Customer Service:
1. Customer asks for invoice
2. Click "Send Email"
3. Instant delivery!

### Record Keeping:
1. Export PDF for each order
2. Save to folder
3. Backup/archive

---

## 📱 Email Modal Features

**Smart Pre-fill:**
- Automatically fills distributor's email
- Adds your email to CC
- Shows invoice summary

**Validation:**
- Checks email format
- Requires valid email
- Shows error if missing

**User-Friendly:**
- Black theme matching ERP
- Red accents
- Clear instructions
- Easy to use

---

## 🔧 Technical Details

### PDF Generation:
- Uses WeasyPrint library
- Converts HTML to PDF
- Same styling as print version
- High quality output

### Excel Generation:
- Uses openpyxl library
- Professional formatting
- Color-coded headers
- Auto-sized columns

### Email Sending:
- Uses Flask-Mail
- SendGrid SMTP
- PDF attachment
- HTML email body

---

## 🎨 Theme Consistency

All exports match your black theme:

**PDF:**
- Black background
- White text
- Red accents (#d00000)
- Professional appearance

**Excel:**
- Red headers (#D00000)
- White background (Excel standard)
- Bold totals
- Clean layout

**Email Modal:**
- Black background
- White text
- Red borders
- Matches ERP theme

---

## 📋 Workflow Examples

### Example 1: Daily Order Processing
```
1. Distributor calls with order
2. Create order in ERP
3. Click "Send Email"
4. Distributor receives invoice instantly
5. Payment tracking begins
```

### Example 2: Month-End Accounting
```
1. Go to Orders list
2. For each order:
   - Click "Export Excel"
   - Save to folder
3. Consolidate all Excel files
4. Import to accounting software
5. GST filing ready!
```

### Example 3: Customer Follow-up
```
1. Customer hasn't paid
2. Open order
3. Click "Send Email"
4. Add reminder in email
5. Track payment
```

---

## ⚠️ Important Notes

### Email Requirements:
- Distributor must have email in profile
- Email configuration must be correct
- Internet connection required
- SendGrid account active

### File Sizes:
- PDF: ~100-200 KB per invoice
- Excel: ~50-100 KB per invoice
- Email attachment limit: 10 MB (plenty!)

### Browser Compatibility:
- Works in all modern browsers
- Chrome, Firefox, Edge
- Download location: Browser's download folder

---

## 🐛 Troubleshooting

### PDF Not Downloading?
1. Check browser pop-up blocker
2. Allow downloads from localhost
3. Check browser download settings

### Excel Not Opening?
1. Install Microsoft Excel or LibreOffice
2. Check file association
3. Try opening manually from downloads

### Email Not Sending?
1. Check distributor has email
2. Verify email configuration in `.env`
3. Check internet connection
4. Check SendGrid account status
5. Look for error message

### Email Not Received?
1. Check spam folder
2. Verify email address is correct
3. Check SendGrid logs
4. Try different email address

---

## 📊 Statistics Tracking

Track your usage:
- **PDFs exported:** Count downloads
- **Emails sent:** Check SendGrid dashboard
- **Excel exports:** Monitor accounting workflow

---

## 🚀 Future Enhancements

Possible additions:
- Bulk email to multiple distributors
- Scheduled email reminders
- WhatsApp PDF sharing
- Cloud storage integration
- Automatic backup

---

## ✅ Testing Checklist

Before going live:
- [ ] Install weasyprint and openpyxl
- [ ] Test PDF export
- [ ] Test Excel export
- [ ] Add email to test distributor
- [ ] Send test email
- [ ] Verify email received
- [ ] Check PDF attachment
- [ ] Verify Excel formatting
- [ ] Test with different orders
- [ ] Test with different browsers

---

## 📞 Support

**Need Help?**
- Check error messages
- Verify configuration
- Test with sample order
- Check logs

**Common Issues:**
- Missing email: Add to distributor profile
- Email not sending: Check `.env` configuration
- PDF not generating: Install weasyprint
- Excel not opening: Install Excel/LibreOffice

---

## 🎉 Benefits

**Time Saved:**
- No manual PDF creation
- No manual email composition
- Instant delivery
- Professional appearance

**Improved Service:**
- Faster invoice delivery
- Professional communication
- Better record keeping
- Happy customers!

**Better Accounting:**
- Easy Excel export
- Ready for Tally import
- GST compliance
- Audit trail

---

**All features are ready to use! Start exporting and emailing invoices today!** 📧📄📊

