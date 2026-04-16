# SEO Analyzer Pro - Quick Start Commands Reference

**Copy-paste ready commands to get everything running**

---

## Installation & Setup

### 1. Clone or Extract Project
```bash
cd ~/projects
git clone https://github.com/yourusername/seo-analyzer-pro.git
cd seo-analyzer-pro
```

### 2. Verify Project
```bash
python VERIFY_PROJECT.py
```

### 3. Setup Local Environment
```bash
bash scripts/setup_local.sh
```

### 4. Activate Virtual Environment
```bash
source venv/bin/activate
# Windows: venv\Scripts\activate
```

---

## Development Commands

### Start Backend (Development)
```bash
uvicorn backend.main:app --reload --port 8000
# Open: http://localhost:8000
```

### Run Tests
```bash
pytest backend/test_api.py -v
```

### Run CLI Tool
```bash
python cli/cli.py analyze -k "keyword1" "keyword2"
python cli/cli.py generate -k "keyword" -t article
python cli/cli.py export -o results.json
```

### Run API Examples
```bash
python INTEGRATION_EXAMPLES.py
```

---

## Deployment Commands

### Deploy to DigitalOcean
```bash
bash scripts/deploy_digitalocean.sh
```

### Deploy to AWS
```bash
bash scripts/deploy_aws.sh
```

### Local Docker Deployment
```bash
docker-compose up -d
```

---

## Database Commands

### Connect to Database
```bash
sqlite3 backend/database.db
# Or for PostgreSQL:
psql -U seo_user -d seo_analyzer_pro
```

### Backup Database
```bash
cp backend/database.db backend/database.db.backup
# Or for PostgreSQL:
pg_dump -U seo_user seo_analyzer_pro > backup.sql
```

### Restore Database
```bash
cp backend/database.db.backup backend/database.db
# Or for PostgreSQL:
psql -U seo_user seo_analyzer_pro < backup.sql
```

---

## Git Commands

### Check Status
```bash
git status
```

### Commit Changes
```bash
git add .
git commit -m "Your message here"
```

### View Commit History
```bash
git log --oneline
```

### Push to Remote
```bash
git push origin main
```

---

## Monitoring & Health Checks

### Check API Health
```bash
curl http://localhost:8000/api/health
```

### Monitor Logs (Development)
```bash
tail -f app.log
```

### Check Server Status
```bash
curl -I http://your-domain.com
```

---

## Troubleshooting Commands

### Check Python Version
```bash
python --version
```

### Check Virtual Environment
```bash
which python
# Or on Windows: where python
```

### Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### Update Dependencies
```bash
pip install --upgrade pip
pip install -r backend/requirements.txt --upgrade
```

### Clear Python Cache
```bash
find . -type d -name __pycache__ -exec rm -r {} +
```

---

## Port & Process Management

### Check What's Using Port 8000
```bash
lsof -i :8000
# Or on Windows: netstat -ano | findstr :8000
```

### Kill Process on Port 8000
```bash
kill -9 $(lsof -t -i :8000)
# Or on Windows: taskkill /PID [PID] /F
```

### Run on Different Port
```bash
uvicorn backend.main:app --port 8001
```

---

## Production Commands

### Create System Service (Linux)
```bash
sudo systemctl enable seo-analyzer-pro
sudo systemctl start seo-analyzer-pro
sudo systemctl status seo-analyzer-pro
```

### View Service Logs
```bash
sudo journalctl -u seo-analyzer-pro -f
```

### Restart Application (Production)
```bash
sudo systemctl restart seo-analyzer-pro
```

---

## Documentation Access

### View README
```bash
cat README.md
# or open in editor
```

### View Specific Guide
```bash
cat MONETIZATION.md
cat DEPLOYMENT.md
cat SECURITY.md
```

### Search Documentation
```bash
grep -r "keyword" docs/
```

---

## Email & Configuration

### Edit Environment Variables
```bash
nano .env
# or
code .env
```

### Test Email Configuration
```bash
python scripts/test_email.py
```

### Generate New Secret Key
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Backup & Recovery

### Full Project Backup
```bash
tar -czf seo-analyzer-pro-backup.tar.gz .
```

### Restore from Backup
```bash
tar -xzf seo-analyzer-pro-backup.tar.gz
```

### Database Backup (DigitalOcean)
```bash
doctl databases backup create seo-analyzer-pro
```

---

## Performance Optimization

### Check Application Performance
```bash
python -m cProfile -s cumtime cli/cli.py analyze -k "test"
```

### Monitor Memory Usage
```bash
python -m memory_profiler scripts/growth_projections.py
```

### Load Test
```bash
ab -n 1000 -c 10 http://localhost:8000/api/health
```

---

## Security Commands

### Check for Vulnerabilities
```bash
pip install safety
safety check
```

### Scan for Secrets
```bash
pip install detect-secrets
detect-secrets scan
```

### Generate SSL Certificate (Local)
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

---

## Quick Stats

### Count Lines of Code
```bash
wc -l backend/*.py cli/*.py scripts/*.py
find . -name "*.py" -type f | xargs wc -l
```

### Count Documentation
```bash
wc -l *.md docs/*.md
find . -name "*.md" -type f | xargs wc -l
```

### List All Files
```bash
find . -type f -name "*.py" -o -name "*.md" | sort
```

---

## Useful One-Liners

### Start everything
```bash
source venv/bin/activate && uvicorn backend.main:app --reload &
```

### Run tests and check coverage
```bash
pytest backend/test_api.py --cov=backend --cov-report=html
```

### Format Python code
```bash
black backend/ cli/ scripts/
```

### Check code quality
```bash
flake8 backend/ cli/ scripts/
```

---

## Emergency Commands

### Stop all services
```bash
pkill -f uvicorn
pkill -f python
```

### Emergency rollback
```bash
git revert HEAD
git push
```

### Reset database to default
```bash
rm backend/database.db
python backend/main.py  # Recreate fresh
```

### Clear all caches
```bash
redis-cli FLUSHALL  # if using Redis
python -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True)"
```

---

## Daily Routine Commands

### Morning Check
```bash
python VERIFY_PROJECT.py
curl http://localhost:8000/api/health
git status
```

### Before Deployment
```bash
pytest backend/test_api.py -v
git add .
git commit -m "Release version X.X.X"
git push
```

### After Deployment
```bash
curl http://your-production-url/api/health
tail -f production.log
```

---

## Helpful Aliases (Add to ~/.bashrc)

```bash
alias seo_dev="cd ~/projects/seo-analyzer-pro && source venv/bin/activate && uvicorn backend.main:app --reload"
alias seo_test="cd ~/projects/seo-analyzer-pro && pytest backend/test_api.py -v"
alias seo_cli="cd ~/projects/seo-analyzer-pro && python cli/cli.py"
alias seo_check="cd ~/projects/seo-analyzer-pro && python VERIFY_PROJECT.py"
```

---

## Need Help?

| Command | Purpose |
|---------|---------|
| `python VERIFY_PROJECT.py` | Check everything works |
| `cat TROUBLESHOOTING.md` | Find solutions to common problems |
| `cat GETTING_STARTED_CHECKLIST.md` | Step-by-step guide |
| `cat LAUNCH_PLAYBOOK_7DAYS.md` | Your first week plan |

---

**Print this page or save to reference during development!**

*Last Updated: 2026-04-15*
