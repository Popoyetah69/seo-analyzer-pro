"""
SEO Analyzer Pro - Sample API Usage & Integration Examples
Complete working examples for developers
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

print("=" * 80)
print("SEO ANALYZER PRO - INTEGRATION EXAMPLES")
print("=" * 80)
print()

# Example 1: Basic keyword analysis
print("EXAMPLE 1: Analyze Single Keyword")
print("-" * 80)

keyword_data = {
    "keyword": "best web hosting",
    "language": "en"
}

print(f"Request: POST /api/analyze/keyword")
print(f"Payload: {json.dumps(keyword_data, indent=2)}")
print()

try:
    response = requests.post(
        f"{BASE_URL}/api/analyze/keyword",
        json=keyword_data,
        headers=HEADERS,
        timeout=5
    )
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success! Response:")
        print(json.dumps(result, indent=2))
        print()
    else:
        print(f"❌ Error: {response.status_code}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("(Make sure backend is running on http://localhost:8000)")
print()

# Example 2: Batch keyword analysis
print("EXAMPLE 2: Batch Analyze Keywords")
print("-" * 80)

batch_data = {
    "keywords": [
        "web hosting",
        "email marketing",
        "crm software"
    ],
    "language": "en"
}

print(f"Request: POST /api/analyze/batch")
print(f"Keywords: {batch_data['keywords']}")
print()

try:
    response = requests.post(
        f"{BASE_URL}/api/analyze/batch",
        json=batch_data,
        headers=HEADERS,
        timeout=10
    )
    if response.status_code == 200:
        results = response.json()
        print(f"✅ Success! Analyzed {len(results)} keywords:")
        for result in results:
            print(f"  • {result['keyword']}: {result['search_volume']:,} volume, {result['difficulty']}/100 difficulty")
    else:
        print(f"❌ Error: {response.status_code}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
print()

# Example 3: Generate content
print("EXAMPLE 3: Generate SEO Content")
print("-" * 80)

content_data = {
    "keyword": "best web hosting",
    "content_type": "meta",
    "tone": "professional",
    "language": "en"
}

print(f"Request: POST /api/generate/content")
print(f"Keyword: {content_data['keyword']}")
print(f"Type: {content_data['content_type']}")
print()

try:
    response = requests.post(
        f"{BASE_URL}/api/generate/content",
        json=content_data,
        headers=HEADERS,
        timeout=5
    )
    if response.status_code == 200:
        content = response.json()
        print(f"✅ Success! Generated content:")
        for key, value in content.items():
            if isinstance(value, str):
                print(f"  {key}: {value[:100]}...")
            elif isinstance(value, list):
                print(f"  {key}: {', '.join(value[:3])}")
    else:
        print(f"❌ Error: {response.status_code}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
print()

# Example 4: Get trending keywords
print("EXAMPLE 4: Get Trending Keywords")
print("-" * 80)

print("Request: GET /api/trending/keywords")
print()

try:
    response = requests.get(
        f"{BASE_URL}/api/trending/keywords",
        params={"limit": 5},
        headers=HEADERS,
        timeout=5
    )
    if response.status_code == 200:
        trending = response.json()
        print(f"✅ Success! Top trending keywords:")
        for kw in trending[:5]:
            print(f"  • {kw['keyword']}: {kw.get('trend', 'stable')}")
    else:
        print(f"❌ Error: {response.status_code}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
print()

# Example 5: User statistics
print("EXAMPLE 5: Get User Statistics")
print("-" * 80)

print("Request: GET /api/user/stats")
print()

try:
    response = requests.get(
        f"{BASE_URL}/api/user/stats",
        headers=HEADERS,
        timeout=5
    )
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Success! User statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    else:
        print(f"❌ Error: {response.status_code}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
print()

# Example 6: Health check
print("EXAMPLE 6: Health Check")
print("-" * 80)

print("Request: GET /api/health")
print()

try:
    response = requests.get(
        f"{BASE_URL}/api/health",
        headers=HEADERS,
        timeout=5
    )
    if response.status_code == 200:
        print(f"✅ API is healthy!")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ API returned: {response.status_code}")
except Exception as e:
    print(f"❌ API is not running: {e}")
print()

print("=" * 80)
print("INTEGRATION EXAMPLES COMPLETED")
print("=" * 80)
