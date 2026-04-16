#!/bin/bash
# SEO Analyzer Pro - Local Development Setup
# Quick setup for local development

set -e

echo "=========================================="
echo "SEO Analyzer Pro - Local Setup"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# Setup database
echo ""
echo "=========================================="
echo "Setting up database..."
echo "=========================================="
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from template"
    echo "⚠️  Edit .env with your configuration"
fi

# Initialize database
echo "Initializing SQLite database..."
python3 -c "
import sqlite3
conn = sqlite3.connect('seo_analyzer.db')
conn.execute('''CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY,
    keyword TEXT,
    volume INTEGER,
    difficulty INTEGER,
    cpc REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()
print('✅ Database initialized')
"

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To start development:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Start backend: uvicorn backend.main:app --reload"
echo "  3. Open frontend: http://localhost:8000"
echo ""
echo "CLI commands:"
echo "  python cli/cli.py analyze -k 'keyword1' 'keyword2'"
echo "  python cli/cli.py generate -k 'keyword' -t article"
echo ""
echo "Run tests:"
echo "  pytest backend/test_api.py -v"
echo ""
