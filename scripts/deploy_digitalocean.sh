#!/bin/bash
# SEO Analyzer Pro - One-Click DigitalOcean Deployment
# Deploy entire stack to DigitalOcean in 5 minutes

set -e

echo "=========================================="
echo "SEO Analyzer Pro - DigitalOcean Deployment"
echo "=========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v doctl &> /dev/null; then
    echo "❌ doctl CLI not found. Install from: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

echo "✅ Prerequisites OK"
echo ""

# Get inputs
echo "Please provide the following information:"
read -p "Enter DigitalOcean API token: " DO_TOKEN
read -p "Enter app name (e.g., seo-analyzer-pro): " APP_NAME
read -p "Enter region (nyc3, sfo3, lon1, etc): " REGION

# Set token
export DIGITALOCEAN_ACCESS_TOKEN=$DO_TOKEN

echo ""
echo "=========================================="
echo "Creating DigitalOcean App..."
echo "=========================================="
echo ""

# Create app spec
cat > app-spec.yaml <<EOF
name: $APP_NAME
services:
  - name: backend
    github:
      repo: YOUR_GITHUB_REPO/seo-analyzer-pro
      branch: main
    build_command: pip install -r backend/requirements.txt
    run_command: uvicorn backend.main:app --host 0.0.0.0 --port 8080
    envs:
      - key: DATABASE_URL
        value: postgresql://user:password@db:5432/seoanalyzer
    http_port: 8080
    source_dir: /

  - name: frontend
    github:
      repo: YOUR_GITHUB_REPO/seo-analyzer-pro
      branch: main
    build_command: "# Static files"
    run_command: "# Served by backend"
    source_dir: frontend

databases:
  - name: db
    engine: PG
    version: "14"

static_sites:
  - name: docs
    source_dir: docs
    routes:
      - path: /docs

regions:
  - $REGION
EOF

echo "Creating app with spec..."
doctl apps create --spec app-spec.yaml

echo ""
echo "=========================================="
echo "✅ Deployment Initiated!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Check deployment status: doctl apps list"
echo "2. View logs: doctl apps logs [APP_ID]"
echo "3. Configure domain in DigitalOcean dashboard"
echo "4. Set environment variables for production"
echo ""
echo "Estimated cost: $5-12/month"
