# 🚀 Guide Complet de Déploiement Cloud

Déployer SEO Analyzer Pro en production sur différentes plateformes.

## 1. Heroku (Plus Simple - Gratuit pour tester)

### Setup (10 minutes)

```bash
# 1. Installer Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Créer une app
heroku create seo-analyzer-pro

# 4. Ajouter PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 5. Push le code
git push heroku main

# 6. Vérifier le status
heroku logs --tail
heroku open
```

### Configuration pour Heroku

**Procfile** (root directory):
```
web: uvicorn backend.main:app --host=0.0.0.0 --port=$PORT
```

**runtime.txt**:
```
python-3.11.8
```

**requirements.txt**: Déjà préparé ✅

### Environnement Variables sur Heroku

```bash
heroku config:set DATABASE_URL=postgresql://...
heroku config:set STRIPE_SECRET_KEY=sk_...
heroku config:set SENDGRID_API_KEY=SG...
```

**Coût**: 
- App gratuite (+ $7/mois si DB)
- Parfait pour MVP

---

## 2. AWS (Meilleur pour Scale)

### Option A: Elastic Beanstalk (Simple)

```bash
# 1. Install EB CLI
pip install awsebcli

# 2. Initialiser
eb init -p python-3.11 seo-analyzer-pro

# 3. Créer environnement
eb create production

# 4. Deploy
git push aws main

# 5. Check logs
eb logs
```

**Coût**:
- EC2 t3.micro: ~$10-15/mois
- RDS PostgreSQL: ~$20-30/mois
- Total: ~$30-50/mois

### Option B: ECS + Fargate (Docker)

```bash
# 1. Build Docker image
docker build -t seo-analyzer .

# 2. Push to ECR
aws ecr create-repository --repository-name seo-analyzer
aws ecr get-login-password | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker tag seo-analyzer:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/seo-analyzer:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/seo-analyzer:latest

# 3. Create Fargate service (via AWS Console)
# - Use ECR image
# - Set environment variables
# - Configure ALB
```

**Coût**:
- Fargate: ~$0.05/hour (~$36/mois baseline)
- RDS: ~$30/mois
- ALB: ~$16/mois
- Total: ~$80-100/mois

---

## 3. DigitalOcean (Simple + Cheap)

### App Platform (Recommandé)

```bash
# 1. Connect GitHub
# - New App → Select repository

# 2. Configure
# - Select branch: main
# - Runtime: Python
# - Run command: uvicorn backend.main:app

# 3. Environment
# Add these in UI:
DATABASE_URL=postgresql://...
STRIPE_SECRET_KEY=sk_...

# 4. Deploy
# Automatically deploys on push!
```

**Setup via CLI**:
```bash
# Installer doctl
doctl auth init

# Create app
doctl apps create --spec app.yaml
```

**app.yaml**:
```yaml
name: seo-analyzer-pro
region: nyc

services:
- name: api
  github:
    branch: main
    repo: YOUR_USERNAME/seo-analyzer
  build_command: pip install -r backend/requirements.txt
  run_command: uvicorn backend.main:app --host 0.0.0.0
  http_port: 8000

databases:
- name: db
  engine: PG
  version: "15"
```

**Coût**:
- App Platform: $12/month (starter)
- Database: $15/month
- Total: ~$27/month ✅ **BEST VALUE**

---

## 4. Vercel (Pour Frontend + Serverless API)

### Déployer Frontend

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Deploy
cd frontend
vercel

# 3. Confirm configuration
# Accès automatiquement sur https://seo-analyzer-pro.vercel.app
```

### Serverless API avec Vercel Functions

**Créer api/analyze.py**:
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/api/analyze")
async def analyze(keyword: str):
    # Logic here
    return {"keyword": keyword}
```

**Coût**: Gratuit (dans les limites raisonnables)

---

## 5. Railway (Très Simple)

```bash
# 1. Connect GitHub
# - New Project → Select repo

# 2. Auto-detects Python
# - Reads requirements.txt
# - Detects procfile

# 3. Configure Environment
# DATABASE_URL, API_keys, etc.

# 4. Deploy
# Auto-deploys on push!
```

**Coût**: $5-20/month pour hobby projects

---

## 6. Self-Hosted (VPS)

Si vous préférez total control:

### DigitalOcean Droplet

```bash
# 1. Create droplet
# - Ubuntu 22.04
# - Basic ($4/month) or Standard ($6/month)

# 2. SSH in
ssh root@your_ip

# 3. Setup
sudo apt update && sudo apt upgrade
sudo apt install python3-pip python3-venv postgresql nginx

# 4. Clone repo
git clone https://github.com/yourname/seo-analyzer
cd seo-analyzer/backend

# 5. Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Run with gunicorn
pip install gunicorn
gunicorn main:app --workers 4 --bind 0.0.0.0:8000

# 7. Setup Nginx as reverse proxy
sudo nano /etc/nginx/sites-available/default
```

**nginx config**:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Restart
sudo systemctl restart nginx
```

**SSL avec Let's Encrypt**:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

**Coût**: $4-12/month

---

## Comparison Chart

| Platform | Cost | Ease | Scale | Best For |
|----------|------|------|-------|----------|
| Heroku | $7-50 | ⭐⭐⭐⭐⭐ | Up to 10K users | MVP |
| DigitalOcean App | $27 | ⭐⭐⭐⭐ | Up to 100K users | **RECOMMENDED** |
| Railway | $5-20 | ⭐⭐⭐⭐⭐ | Up to 50K users | Hobby to scale |
| AWS Beanstalk | $30-50 | ⭐⭐⭐ | Up to 1M users | Enterprise |
| DigitalOcean VPS | $4-12 | ⭐⭐ | Unlimited | Control freaks |
| Vercel | Free-$20 | ⭐⭐⭐⭐⭐ | Frontend only | Static + API |

---

## Database Setup

### PostgreSQL on DigitalOcean Managed Database

```bash
# 1. Create managed DB
# - Via console: Databases → New Database Cluster
# - Choose: PostgreSQL 15, Basic plan ($15/month)

# 2. Get connection string
# Format: postgresql://user:password@host:port/database

# 3. Connect from app
# Set DATABASE_URL env variable

# 4. Run migrations (when using SQLAlchemy ORM)
alembic upgrade head
```

### Backup Strategy

```bash
# Daily backups (automated)
# - DigitalOcean does this automatically

# Manual backup
pg_dump -U user -h host database > backup.sql

# Restore
psql -U user -h host database < backup.sql
```

---

## Domain & SSL Setup

### Buy Domain

**Options:**
- Namecheap ($3-5/year)
- Google Domains ($12/year)
- DigitalOcean ($3/year)

### Point Domain

**Step 1: Get nameservers**
```
ns1.digitalocean.com
ns2.digitalocean.com
ns3.digitalocean.com
```

**Step 2: Update in registrar**
- Login to domain registrar
- Set nameservers to DigitalOcean

**Step 3: Setup SSL**
```bash
# If using DigitalOcean App Platform
# Auto-generates SSL certificate!

# If using VPS
sudo certbot --nginx -d yourdomain.com
```

---

## Monitoring & Alerts

### Setup Monitoring

**Sentry (Error tracking)**:
```python
import sentry_sdk

sentry_sdk.init(
    "https://your-token@sentry.io/project-id",
    traces_sample_rate=1.0
)
```

**Uptime monitoring**:
- Use UptimeRobot.com (free)
- Monitor http://yourdomain.com/api/health

**Performance monitoring**:
- Datadog ($15-50/month)
- New Relic (free tier available)

---

## CI/CD Pipeline

### GitHub Actions (Free)

**.github/workflows/deploy.yml**:
```yaml
name: Deploy to DigitalOcean

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to DigitalOcean
        run: |
          doctl apps update ${{ secrets.APP_ID }} --main-branch main
        env:
          DIGITALOCEAN_ACCESS_TOKEN: ${{ secrets.DO_TOKEN }}
```

**Setup secrets**:
- Go to repo Settings → Secrets
- Add: `DO_TOKEN`, `APP_ID`

---

## Recommended Setup (Month 1-6)

```
┌─────────────────────────────────────┐
│  DigitalOcean App Platform          │
│  - Backend: $12/month               │
│  - PostgreSQL: $15/month            │
│  Total: $27/month ✅                 │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│  Vercel (Frontend)                  │
│  - Static deployment: FREE           │
│  - Custom domain: FREE               │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│  Stripe (Payments)                  │
│  - Only pay per transaction (2.9%)   │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│  SendGrid (Emails)                  │
│  - Free: 100/day                    │
│  - Pro: $20-30/month                 │
└─────────────────────────────────────┘

Total: $47-57/month to go live ✅
```

---

## Deployment Checklist

- [ ] Choose hosting (DigitalOcean App)
- [ ] Setup database
- [ ] Setup domain + SSL
- [ ] Set environment variables
- [ ] Test API endpoints
- [ ] Deploy frontend
- [ ] Setup monitoring
- [ ] Test payment flow
- [ ] Setup email notifications
- [ ] Document deployment process
- [ ] Create CI/CD pipeline
- [ ] Backup strategy ready

---

## Troubleshooting

**API returning 502 Bad Gateway?**
- Check logs: `heroku logs --tail`
- Verify requirements.txt installed
- Check environment variables

**Database connection refused?**
- Verify DATABASE_URL format
- Check network/firewall rules
- Test locally first

**High latency?**
- Check database query performance
- Enable caching
- Scale up compute
- Use CDN for frontend

---

**Next Step**: Choose DigitalOcean App Platform and deploy this week!
