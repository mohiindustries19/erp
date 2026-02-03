# Mohi Industries ERP - Deployment Guide

## Prerequisites

- Docker & Docker Compose installed
- Git installed
- 2GB RAM minimum
- 10GB disk space

## Quick Start (Development)

```bash
# 1. Navigate to project
cd mohi-erp

# 2. Start services
docker-compose up -d

# 3. Wait for database to be ready (30 seconds)
sleep 30

# 4. Initialize database
docker-compose exec web python scripts/db/init_db.py

# 5. Access application
# Open browser: http://localhost:5000
# Login: admin / admin123
```

## Production Deployment

### Option 1: VPS (DigitalOcean, Linode, Hetzner)

**Step 1: Create VPS**
- OS: Ubuntu 22.04 LTS
- RAM: 2GB minimum
- Storage: 20GB SSD

**Step 2: Install Docker**
```bash
# SSH into your server
ssh root@your-server-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y
```

**Step 3: Deploy Application**
```bash
# Clone repository
git clone <your-repo-url>
cd mohi-erp

# Create production environment file
cp .env.example .env
nano .env  # Edit with your details

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Initialize database
docker-compose exec web python scripts/db/init_db.py
```

**Step 4: Setup Domain & SSL (Optional)**
```bash
# Install Nginx
apt install nginx certbot python3-certbot-nginx -y

# Configure Nginx reverse proxy
nano /etc/nginx/sites-available/mohi-erp

# Add this configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
ln -s /etc/nginx/sites-available/mohi-erp /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# Get SSL certificate
certbot --nginx -d your-domain.com
```

### Option 2: Render.com (Zero DevOps)

1. Push code to GitHub
2. Go to render.com → New Web Service
3. Connect GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run.py`
   - Add PostgreSQL database
5. Deploy!

### Option 3: Railway.app

1. Push code to GitHub
2. Go to railway.app → New Project
3. Deploy from GitHub
4. Add PostgreSQL plugin
5. Done!

#### CI/CD with GitHub Actions (Optional)

This repo includes GitHub Actions workflows:

- CI: builds dependencies, runs a Python syntax compile step, and builds the Docker image.
- CD: deploys to Railway using Railway CLI.

To enable CD:

1. Create a Railway project and a service that builds from this repository's `Dockerfile`.
2. In GitHub repo settings → **Secrets and variables** → **Actions**, add:
    - `RAILWAY_TOKEN` (required)
    - `RAILWAY_PROJECT_ID` (required)
    - `RAILWAY_SERVICE_ID` (recommended if your project has multiple services)
    - `RAILWAY_ENVIRONMENT_NAME` (optional; default is `production`)
3. Push to `main`/`master` (or run the workflow manually via `workflow_dispatch`).

## Environment Variables

Create `.env` file with these values:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Flask
SECRET_KEY=your-random-secret-key-here
FLASK_ENV=production

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
```

## Backup Strategy

### Automated Daily Backup
```bash
# Create backup script
nano /root/backup-mohi-erp.sh

#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T db pg_dump -U mohi_admin mohi_erp > /backups/mohi_erp_$DATE.sql
# Keep only last 30 days
find /backups -name "mohi_erp_*.sql" -mtime +30 -delete

# Make executable
chmod +x /root/backup-mohi-erp.sh

# Add to crontab (daily at 2 AM)
crontab -e
0 2 * * * /root/backup-mohi-erp.sh
```

### Restore from Backup
```bash
docker-compose exec -T db psql -U mohi_admin mohi_erp < backup_file.sql
```

## Monitoring

### Check Application Status
```bash
docker-compose ps
docker-compose logs -f web
```

### Check Database
```bash
docker-compose exec db psql -U mohi_admin mohi_erp
```

## Troubleshooting

### Application won't start
```bash
# Check logs
docker-compose logs web

# Restart services
docker-compose restart
```

### Database connection error
```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db
```

### Reset everything
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec web python scripts/db/init_db.py
```

## Security Checklist

- [ ] Change default admin password
- [ ] Update SECRET_KEY in .env
- [ ] Update database password
- [ ] Enable firewall (ufw)
- [ ] Setup SSL certificate
- [ ] Regular backups configured
- [ ] Update GSTIN, PAN, FSSAI details

## Cost Estimates

### Self-Hosted VPS
- DigitalOcean: $12/month (2GB RAM)
- Linode: $12/month (2GB RAM)
- Hetzner: €4.5/month (~$5/month)

### PaaS
- Render.com: $7/month (web) + $7/month (db) = $14/month
- Railway.app: ~$10-15/month

### Local Server
- Old PC/Laptop: Free (electricity cost only)
- Recommended for factory deployment

## Support

For issues or questions:
- Email: info@mohiindustries.in
- Phone: +91 9262650010

---
**ॐ श्री गणेशाय नमः**
