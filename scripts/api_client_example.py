#!/usr/bin/env python3
"""
SEO Analyzer Pro - Sample API Client
Example of how to use the API programmatically
"""

import requests
import json
from typing import Dict, List, Optional

class SEOAnalyzerProClient:
    """Client library for SEO Analyzer Pro API"""
    
    def __init__(self, api_key: str = None, base_url: str = "http://localhost:8000"):
        """
        Initialize client
        
        Args:
            api_key: Your API key (required for Pro/Enterprise)
            base_url: Base URL of the API (default: localhost)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def analyze_keyword(self, keyword: str, language: str = "en") -> Dict:
        """
        Analyze a single keyword
        
        Args:
            keyword: Keyword to analyze
            language: Language code (en, fr, es, de)
            
        Returns:
            Dictionary with analysis results
            
        Example:
            >>> client = SEOAnalyzerProClient()
            >>> result = client.analyze_keyword("web hosting")
            >>> print(result['search_volume'])
            22100
        """
        url = f"{self.base_url}/api/analyze/keyword"
        payload = {
            "keyword": keyword,
            "language": language
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def analyze_keywords_batch(self, keywords: List[str], language: str = "en") -> List[Dict]:
        """
        Analyze multiple keywords at once (faster than individual calls)
        
        Args:
            keywords: List of keywords (up to 100)
            language: Language code
            
        Returns:
            List of analysis results
            
        Example:
            >>> keywords = ["web hosting", "email marketing", "crm software"]
            >>> results = client.analyze_keywords_batch(keywords)
            >>> for result in results:
            ...     print(f"{result['keyword']}: {result['search_volume']} volume")
        """
        url = f"{self.base_url}/api/analyze/batch"
        payload = {
            "keywords": keywords,
            "language": language
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def generate_content(self, keyword: str, content_type: str = "article", 
                        tone: str = "professional", language: str = "en") -> Dict:
        """
        Generate SEO content for a keyword
        
        Args:
            keyword: Target keyword
            content_type: Type of content (article, meta, title, description)
            tone: Writing tone (professional, casual, technical, sales)
            language: Language code
            
        Returns:
            Generated content
            
        Example:
            >>> content = client.generate_content(
            ...     keyword="web hosting",
            ...     content_type="meta",
            ...     tone="professional"
            ... )
            >>> print(content['meta_title'])
            'Best Web Hosting 2026 | Affordable & Reliable'
        """
        url = f"{self.base_url}/api/generate/content"
        payload = {
            "keyword": keyword,
            "content_type": content_type,
            "tone": tone,
            "language": language
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_trending_keywords(self, category: str = "general", 
                            limit: int = 10) -> List[Dict]:
        """
        Get currently trending keywords
        
        Args:
            category: Keyword category (general, tech, business, health, etc)
            limit: Number of keywords to return
            
        Returns:
            List of trending keywords
            
        Example:
            >>> trending = client.get_trending_keywords(category="tech")
            >>> for kw in trending:
            ...     print(f"{kw['keyword']}: {kw['trend']}")
        """
        url = f"{self.base_url}/api/trending/keywords"
        params = {
            "category": category,
            "limit": limit
        }
        
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def analyze_competitor(self, competitor_domain: str, 
                          keywords: List[str] = None) -> Dict:
        """
        Analyze a competitor's keywords and backlinks
        
        Args:
            competitor_domain: Competitor's domain (e.g., example.com)
            keywords: Keywords to check against (optional)
            
        Returns:
            Competitor analysis
            
        Example:
            >>> analysis = client.analyze_competitor(
            ...     "competitor.com",
            ...     keywords=["web hosting", "email marketing"]
            ... )
            >>> print(analysis['top_keywords'])
        """
        url = f"{self.base_url}/api/competitor/analyze"
        payload = {
            "competitor_domain": competitor_domain,
            "keywords": keywords or []
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_user_stats(self) -> Dict:
        """
        Get current user's statistics
        
        Returns:
            User stats (analyses count, API usage, etc)
            
        Example:
            >>> stats = client.get_user_stats()
            >>> print(f"Total analyses: {stats['total_analyses']}")
            >>> print(f"API calls used this month: {stats['api_calls_month']}")
        """
        url = f"{self.base_url}/api/user/stats"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def export_results(self, analysis_ids: List[int], 
                      format: str = "json") -> bytes:
        """
        Export analysis results
        
        Args:
            analysis_ids: IDs of analyses to export
            format: Export format (json, csv)
            
        Returns:
            File content as bytes
            
        Example:
            >>> # Export analyses 1, 2, 3 as CSV
            >>> data = client.export_results([1, 2, 3], format="csv")
            >>> with open("results.csv", "wb") as f:
            ...     f.write(data)
        """
        url = f"{self.base_url}/api/export/results"
        payload = {
            "analysis_ids": analysis_ids,
            "format": format
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.content
    
    def health_check(self) -> bool:
        """Check if API is healthy"""
        try:
            url = f"{self.base_url}/api/health"
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200
        except:
            return False


# EXAMPLE USAGE
if __name__ == "__main__":
    # Initialize client (no API key needed for local dev)
    client = SEOAnalyzerProClient(base_url="http://localhost:8000")
    
    # Example 1: Check API health
    print("Checking API health...")
    if client.health_check():
        print("✅ API is healthy\n")
    else:
        print("❌ API is down\n")
        exit(1)
    
    # Example 2: Analyze single keyword
    print("Analyzing single keyword...")
    result = client.analyze_keyword("web hosting")
    print(f"  Keyword: {result['keyword']}")
    print(f"  Search Volume: {result['search_volume']:,}")
    print(f"  Difficulty: {result['difficulty']}/100")
    print(f"  CPC: ${result['cpc']}\n")
    
    # Example 3: Batch analyze keywords
    print("Batch analyzing keywords...")
    keywords = ["web hosting", "email marketing", "crm software"]
    results = client.analyze_keywords_batch(keywords)
    for result in results:
        print(f"  {result['keyword']}: {result['search_volume']:,} volume")
    print()
    
    # Example 4: Generate content
    print("Generating meta tags...")
    content = client.generate_content(
        keyword="web hosting",
        content_type="meta",
        tone="professional"
    )
    print(f"  Title: {content.get('title', 'N/A')}")
    print(f"  Description: {content.get('description', 'N/A')}\n")
    
    # Example 5: Get trending keywords
    print("Getting trending keywords...")
    trending = client.get_trending_keywords(limit=5)
    for kw in trending:
        print(f"  {kw['keyword']}: {kw['trend']}")
    print()
    
    # Example 6: User stats
    print("Getting user statistics...")
    stats = client.get_user_stats()
    print(f"  Total analyses: {stats.get('total_analyses', 0)}")
    print(f"  API calls this month: {stats.get('api_calls_month', 0)}")
    print()
    
    print("✅ All examples completed successfully!")
