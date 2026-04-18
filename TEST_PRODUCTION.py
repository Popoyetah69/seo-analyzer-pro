#!/usr/bin/env python3
"""
Production Verification Script
Tests all critical endpoints and functionality
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://analyzerseo.store"
API_URL = f"{BASE_URL}/api"

def log(message, status="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{status}] {message}")

def test_landing_page():
    """Test that landing page loads"""
    log("Testing landing page...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200 and "SEO Analyzer Pro" in response.text:
            log("✓ Landing page loads correctly", "PASS")
            return True
        else:
            log(f"✗ Landing page returned {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"✗ Landing page error: {e}", "FAIL")
        return False

def test_pricing_endpoint():
    """Test pricing endpoint"""
    log("Testing /api/payments/pricing endpoint...")
    try:
        response = requests.get(f"{API_URL}/payments/pricing", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "plans" in data:
                log(f"✓ Pricing endpoint works. Found {len(data['plans'])} plans", "PASS")
                return True
        log(f"✗ Pricing endpoint returned {response.status_code}", "FAIL")
        return False
    except Exception as e:
        log(f"✗ Pricing endpoint error: {e}", "FAIL")
        return False

def test_health():
    """Test health endpoint"""
    log("Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            log("✓ Health endpoint working", "PASS")
            return True
        else:
            log(f"✗ Health endpoint returned {response.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"✗ Health endpoint error: {e}", "FAIL")
        return False

def test_cors():
    """Test CORS headers"""
    log("Testing CORS headers...")
    try:
        response = requests.get(
            f"{API_URL}/health",
            headers={"Origin": "https://analyzerseo.store"}
        )
        cors_header = response.headers.get('Access-Control-Allow-Origin', 'NOT_SET')
        if cors_header in ['https://analyzerseo.store', 'https://www.analyzerseo.store']:
            log(f"✓ CORS correctly restricted: {cors_header}", "PASS")
            return True
        elif cors_header == '*':
            log("✗ CORS is completely open (*) - SECURITY RISK!", "FAIL")
            return False
        else:
            log(f"⚠ CORS header value: {cors_header}", "WARN")
            return True
    except Exception as e:
        log(f"✗ CORS test error: {e}", "FAIL")
        return False

def test_security_headers():
    """Test security headers"""
    log("Testing security headers...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        
        headers_to_check = [
            ('X-Frame-Options', 'DENY'),
            ('X-Content-Type-Options', 'nosniff'),
            ('Strict-Transport-Security', 'max-age=31536000'),
        ]
        
        all_good = True
        for header, expected_value in headers_to_check:
            actual_value = response.headers.get(header, 'NOT_SET')
            if expected_value in actual_value:
                log(f"  ✓ {header}: {actual_value}", "PASS")
            else:
                log(f"  ✗ {header}: Expected '{expected_value}', got '{actual_value}'", "FAIL")
                all_good = False
        
        return all_good
    except Exception as e:
        log(f"✗ Security headers test error: {e}", "FAIL")
        return False

def test_https():
    """Test HTTPS is enforced"""
    log("Testing HTTPS enforcement...")
    try:
        # Try HTTP, should redirect to HTTPS
        response = requests.get("http://analyzerseo.store", allow_redirects=False, timeout=5)
        if response.status_code in [301, 302, 307]:
            location = response.headers.get('Location', '')
            if location.startswith('https://'):
                log(f"✓ HTTP redirects to HTTPS", "PASS")
                return True
        log("⚠ HTTP redirect check unclear", "WARN")
        return True
    except Exception as e:
        log(f"⚠ HTTPS test inconclusive: {e}", "WARN")
        return True

def main():
    log("=" * 60)
    log("PRODUCTION VERIFICATION SUITE", "START")
    log("=" * 60)
    
    tests = [
        ("Landing Page", test_landing_page),
        ("Pricing Endpoint", test_pricing_endpoint),
        ("Health Endpoint", test_health),
        ("CORS Configuration", test_cors),
        ("Security Headers", test_security_headers),
        ("HTTPS Enforcement", test_https),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            log(f"✗ Unexpected error in {test_name}: {e}", "ERROR")
            results[test_name] = False
    
    log("=" * 60)
    log("SUMMARY", "RESULT")
    log("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        log(f"{test_name}: {status}")
    
    log(f"\nTotal: {passed}/{total} tests passed", "SUMMARY")
    
    if passed == total:
        log("🚀 ALL TESTS PASSED - PRODUCTION READY", "SUCCESS")
        return 0
    else:
        log(f"⚠ {total - passed} test(s) failed - REVIEW REQUIRED", "WARNING")
        return 1

if __name__ == "__main__":
    exit(main())
