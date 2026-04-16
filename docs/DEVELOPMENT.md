# SEO Analyzer Pro - Development Guide for Contributors

## Setting Up Development Environment

### Prerequisites
- Python 3.9+
- Git
- Docker (optional)
- PostgreSQL (optional, SQLite is default)

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/seo-analyzer-pro.git
cd seo-analyzer-pro

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run tests
pytest backend/test_api.py -v

# Start development server
uvicorn backend.main:app --reload --port 8000

# In another terminal, test CLI
python cli/cli.py analyze -k "test keyword"
```

---

## Project Structure

```
backend/
├── main.py              # FastAPI application
├── test_api.py          # Unit tests
└── requirements.txt     # Dependencies

cli/
└── cli.py               # Command-line interface

frontend/
└── index.html           # Web dashboard

docs/
└── *.md                 # Documentation

scripts/
├── api_client_example.py      # API usage examples
├── pricing_calculator.py      # ROI calculator
├── growth_projections.py      # Revenue projections
├── deploy_digitalocean.sh     # DigitalOcean deployment
├── deploy_aws.sh              # AWS deployment
└── setup_local.sh             # Local setup

data/
├── sample_data.json           # Sample data
└── sample_keywords.csv        # Sample keywords
```

---

## Code Conventions

### Python Code Style
- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters
- Use docstrings for functions

```python
def analyze_keyword(keyword: str, language: str = "en") -> Dict[str, Any]:
    """
    Analyze keyword metrics for SEO.
    
    Args:
        keyword: The keyword to analyze
        language: Language code (en, fr, es, de)
        
    Returns:
        Dictionary containing:
        - search_volume: Monthly search volume
        - difficulty: Keyword difficulty (0-100)
        - cpc: Cost per click in USD
        - trend: Current trend (growing, stable, declining)
        
    Raises:
        ValueError: If keyword is empty or too long
    """
    pass
```

### Naming Conventions
- Functions: `snake_case` (analyze_keyword)
- Classes: `PascalCase` (SEOAnalyzer)
- Constants: `UPPER_SNAKE_CASE` (API_BASE_URL)
- Private: `_leading_underscore` (_internal_method)

### Comments
```python
# Good: Explains WHY, not WHAT
# We use 1000 as max keywords to prevent database overload
max_keywords = 1000

# Bad: Obvious from code
# Set max keywords
max_keywords = 1000
```

---

## Adding Features

### Feature Request Process

1. **Create issue on GitHub** with:
   - Clear description
   - Use case / why it's needed
   - Proposed implementation (optional)

2. **Get feedback** from maintainers before implementing

3. **Implement on feature branch**:
   ```bash
   git checkout -b feature/my-feature
   ```

4. **Write tests** for new functionality:
   ```python
   def test_new_feature():
       result = new_feature()
       assert result is not None
   ```

5. **Update documentation** if needed

6. **Submit pull request** with:
   - Clear description
   - Reference to issue
   - Screenshots if UI changes

### Common Feature Areas

#### Backend API
- Add endpoint in `backend/main.py`
- Add test in `backend/test_api.py`
- Update documentation

#### CLI Tool
- Add command in `cli/cli.py`
- Add help text
- Test with: `python cli/cli.py --help`

#### Frontend
- Add UI component to `frontend/index.html`
- Ensure responsive design
- Test in multiple browsers

---

## Running Tests

### Run all tests
```bash
pytest backend/test_api.py -v
```

### Run specific test
```bash
pytest backend/test_api.py::test_analyze_keyword -v
```

### Run with coverage
```bash
pytest backend/test_api.py --cov=backend --cov-report=html
open htmlcov/index.html
```

### Coverage targets
- Minimum: 70%
- Target: 85%+

---

## Debugging

### Enable debug mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Pdb debugging
```python
import pdb; pdb.set_trace()
# Or (Python 3.7+):
breakpoint()
```

### Check API responses
```bash
# Test endpoint
curl -X POST http://localhost:8000/api/analyze/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "test"}'

# With pretty print
curl -X POST http://localhost:8000/api/analyze/keyword \
  -H "Content-Type: application/json" \
  -d '{"keyword": "test"}' | python -m json.tool
```

---

## Performance Optimization

### Database Queries
```python
# Bad: N+1 queries
for user in users:
    print(user.analyses)  # Query for each user

# Good: Use joins
users = session.query(User).options(
    joinedload(User.analyses)
).all()
```

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_operation(keyword):
    # Results are cached for 1000 unique inputs
    pass
```

### Async Operations
```python
@app.post("/api/analyze/batch")
async def batch_analyze(keywords: List[str]):
    # Use asyncio for parallel processing
    tasks = [analyze_keyword_async(kw) for kw in keywords]
    results = await asyncio.gather(*tasks)
    return results
```

---

## Deployment

### Local Deployment
```bash
bash scripts/setup_local.sh
```

### Production Deployment
```bash
# DigitalOcean
bash scripts/deploy_digitalocean.sh

# AWS
bash scripts/deploy_aws.sh
```

### Docker Deployment
```bash
# Build image
docker build -t seo-analyzer-pro .

# Run container
docker run -p 8000:8000 seo-analyzer-pro

# Using docker-compose
docker-compose up
```

---

## Continuous Integration

### Before pushing code:
1. ✅ Run tests: `pytest backend/test_api.py -v`
2. ✅ Check linting: `flake8 backend/ cli/`
3. ✅ Type checking: `mypy backend/ cli/`
4. ✅ Code formatting: `black backend/ cli/`

### Git hooks (optional)
```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# This will run checks before each commit
```

---

## Reporting Bugs

### Bug Report Template

**Title:** [BUG] Short description

**Description:**
Clear description of the issue

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Step 3

**Expected behavior:**
What should happen

**Actual behavior:**
What actually happened

**Environment:**
- OS: macOS / Linux / Windows
- Python: 3.9 / 3.10 / 3.11
- Browser: Chrome / Firefox / Safari

**Error message:**
```
Paste full error message here
```

---

## Documentation

### Adding Documentation
1. Create markdown file in `docs/`
2. Follow existing format
3. Include code examples
4. Update `README.md` with link

### Documentation Standards
- Clear and concise
- Code examples for features
- Screenshots for UI changes
- Links to related docs

---

## Release Process

### Version numbering: MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes

### Release checklist
- [ ] Update version in setup.py
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Create git tag: `git tag v1.0.0`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Create GitHub release
- [ ] Deploy to production

---

## Getting Help

- **Documentation:** See `docs/` folder
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Email:** developers@seoanalyzerpro.com

---

## Code of Conduct

- Be respectful to all contributors
- Provide constructive feedback
- Follow project guidelines
- Report issues privately if security-related

---

## License

This project is licensed under MIT License. See LICENSE file for details.

---

**Questions?** Open an issue or email developers@seoanalyzerpro.com
