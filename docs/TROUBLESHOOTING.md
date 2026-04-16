# SEO Analyzer Pro - Troubleshooting Guide

## Common Issues & Solutions

### Backend Issues

#### Port Already in Use

**Problem:** `Address already in use` when starting the server

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use a different port
uvicorn backend.main:app --port 8001
```

---

#### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r backend/requirements.txt

# Verify installation
pip list | grep fastapi
```

---

#### Database Connection Error

**Problem:** `conn = sqlite3.connect(database_url)` fails

**Solution:**
```bash
# Check if database file exists
ls -la seo_analyzer.db

# Create database if missing
python -c "import sqlite3; conn = sqlite3.connect('seo_analyzer.db'); conn.close()"

# Check database permissions
chmod 644 seo_analyzer.db
```

---

#### API Returns 500 Error

**Problem:** `Internal Server Error` when calling API

**Solution:**
1. Check backend console for error message
2. Verify request format:
```python
# Correct format
curl -X POST http://localhost:8000/api/analyze/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "test"}'

# Check response
curl -X POST http://localhost:8000/api/analyze/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "test"}' -v
```
3. Check input validation (keyword must not be empty)

---

### Frontend Issues

#### Dashboard Not Loading

**Problem:** Blank page or 404 error

**Solution:**
1. Check backend is running: `http://localhost:8000`
2. Open browser console (F12) for JavaScript errors
3. Check if port is correct in index.html
4. Clear browser cache: `Ctrl+Shift+Delete`
5. Try incognito/private mode

---

#### Form Not Submitting

**Problem:** Click "Analyze" but nothing happens

**Solution:**
```javascript
// Open browser console (F12)
// Check for JavaScript errors

// Test API manually
fetch('http://localhost:8000/api/analyze/keyword', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({keyword: 'test'})
})
.then(r => r.json())
.then(data => console.log(data))
```

---

#### CORS Error

**Problem:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
- Backend already has CORS enabled
- If still occurs, check CORS middleware in `backend/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### CLI Issues

#### CLI Command Not Found

**Problem:** `command not found: python cli/cli.py`

**Solution:**
```bash
# Make sure you're in the right directory
cd /path/to/seo-analyzer-pro

# Use explicit python path
python3 cli/cli.py analyze -k "keyword"

# Or make executable
chmod +x cli/cli.py
./cli/cli.py analyze -k "keyword"
```

---

#### CLI No Output

**Problem:** Command runs but no output

**Solution:**
```bash
# Add -v flag for verbose output
python cli/cli.py analyze -k "keyword" -v

# Check output file
ls -la results.json
cat results.json

# Test with simple command
python cli/cli.py --help
```

---

### Testing Issues

#### Tests Fail

**Problem:** `pytest: command not found` or tests fail

**Solution:**
```bash
# Install pytest
pip install pytest

# Run tests with verbose output
pytest backend/test_api.py -v

# Run specific test
pytest backend/test_api.py::test_analyze_keyword -v

# Run with print output
pytest backend/test_api.py -v -s
```

---

#### Test Hangs

**Problem:** Test runs forever

**Solution:**
```bash
# Add timeout
pytest backend/test_api.py --timeout=10

# Run with debugging
pytest backend/test_api.py -v --pdb

# Check for infinite loops in code
```

---

### Deployment Issues

#### Docker Build Fails

**Problem:** `docker build` fails

**Solution:**
```bash
# Check Dockerfile syntax
docker build -t seo-analyzer-pro . --verbose

# Common issues:
# 1. Missing requirements.txt
# 2. Wrong path in Dockerfile
# 3. Python version mismatch

# Clean and rebuild
docker system prune
docker build --no-cache -t seo-analyzer-pro .
```

---

#### Docker Container Exits Immediately

**Problem:** Container starts and stops

**Solution:**
```bash
# Check logs
docker logs <container_id>

# Run interactively to see error
docker run -it seo-analyzer-pro bash

# Common issues:
# 1. Port already in use
# 2. Database connection error
# 3. Missing environment variables

# Test with debugging
docker run -it -p 8000:8000 seo-analyzer-pro bash
python -c "import backend.main"
```

---

#### Deployment Script Fails

**Problem:** `bash deploy_digitalocean.sh` fails

**Solution:**
```bash
# Check prerequisites
which doctl  # Check if doctl is installed
doctl auth init  # Authenticate with DigitalOcean

# Check API token
echo $DIGITALOCEAN_ACCESS_TOKEN

# Run with debugging
bash -x deploy_digitalocean.sh

# Common issues:
# 1. doctl not installed
# 2. Invalid API token
# 3. Insufficient permissions
```

---

### Performance Issues

#### Slow API Response

**Problem:** API takes >1 second to respond

**Solution:**
```python
# Enable FastAPI logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check database query time
# Profile code:
import cProfile
cProfile.run('analyze_keyword("test")')

# Check network latency
# Optimize database queries
# Add caching
```

---

#### High Memory Usage

**Problem:** Process uses lots of RAM

**Solution:**
```python
# Check for memory leaks
import tracemalloc
tracemalloc.start()

# Check for large data structures
# Limit batch size

# Monitor memory
import psutil
process = psutil.Process()
print(process.memory_info())
```

---

### Database Issues

#### Cannot Connect to Database

**Problem:** `connection refused` or `database locked`

**Solution:**
```python
# For SQLite:
# 1. Check file permissions
chmod 644 seo_analyzer.db

# 2. Remove lock file if exists
rm seo_analyzer.db-journal

# 3. Verify database:
sqlite3 seo_analyzer.db "SELECT 1;"

# For PostgreSQL:
# 1. Check if server is running
psql -U postgres

# 2. Check connection string
echo $DATABASE_URL

# 3. Verify credentials
psql -U username -h localhost -d database_name
```

---

#### Database Migration Failed

**Problem:** Schema migration errors

**Solution:**
```bash
# Backup database first!
cp seo_analyzer.db seo_analyzer.db.backup

# Recreate database
rm seo_analyzer.db
python -c "import sqlite3; conn = sqlite3.connect('seo_analyzer.db'); conn.close()"

# Or for PostgreSQL:
dropdb database_name
createdb database_name
```

---

### Git Issues

#### Merge Conflicts

**Problem:** `CONFLICT: merge failed`

**Solution:**
```bash
# View conflicts
git status

# Edit conflicted files (look for <<<, ===, >>>)
# Mark as resolved
git add <file>

# Complete merge
git commit -m "Resolve merge conflicts"
```

---

#### Cannot Push to Repository

**Problem:** `permission denied` or `authentication failed`

**Solution:**
```bash
# Check SSH key
ssh -T git@github.com

# Add SSH key if needed
ssh-keygen -t ed25519 -C "your_email@example.com"

# Or use HTTPS with token
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

---

### Email/Notification Issues

#### Emails Not Sending

**Problem:** Email verification fails or emails don't arrive

**Solution:**
```python
# Check SendGrid API key
echo $SENDGRID_API_KEY

# Test email sending
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
message = Mail(
    from_email='noreply@seoanalyzerpro.com',
    to_emails='test@example.com',
    subject='Test',
    plain_text_content='Test email'
)
response = sg.send(message)

# Common issues:
# 1. Invalid API key
# 2. Sender email not verified
# 3. Recipient in spam list
```

---

## Debugging Techniques

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.post("/api/analyze/keyword")
def analyze(keyword: str):
    logger.debug(f"Analyzing keyword: {keyword}")
    result = do_analysis(keyword)
    logger.debug(f"Result: {result}")
    return result
```

### Use Breakpoints
```python
# Python debugger
import pdb; pdb.set_trace()

# Or (Python 3.7+)
breakpoint()

# Step through code:
# n = next line
# s = step into function
# c = continue
# p variable = print variable
```

### Network Debugging
```bash
# Check network requests
curl -v http://localhost:8000/api/analyze/keyword

# Monitor network in browser (F12 → Network tab)
# Check request/response headers and body
```

---

## Getting Help

If you can't find your issue here:

1. **Check the FAQ:** docs/FAQ.md
2. **Review documentation:** docs/
3. **Search GitHub issues:** github.com/yourname/seo-analyzer-pro/issues
4. **Open a new issue** with:
   - Error message (full text)
   - Steps to reproduce
   - Environment (OS, Python version, etc)
   - What you've already tried

---

## Known Limitations

### Current Version
- Mock data generation (real APIs coming Q2 2026)
- SQLite only (PostgreSQL support coming)
- Single-server deployment (scaling coming Q2 2026)
- Limited to 100 keywords per batch (by design)

### Workarounds
- Use PostgreSQL locally (update requirements.txt)
- Process larger batches sequentially
- Run multiple instances behind load balancer

---

**Still stuck?** Email support@seoanalyzerpro.com
