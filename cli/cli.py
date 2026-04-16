#!/usr/bin/env python3
"""CLI pour analyser et générer du contenu SEO en batch"""

import argparse
import sys
import json
import csv
from typing import List
import requests
from datetime import datetime
import time

API_BASE = "http://localhost:8000/api"

class SEOAnalyzerCLI:
    def __init__(self, api_url: str = API_BASE):
        self.api_url = api_url
        self.session = requests.Session()
    
    def analyze_keywords(self, keywords: List[str], output: str = None):
        """Analyse une liste de keywords"""
        print(f"[*] Analysing {len(keywords)} keywords...")
        
        try:
            response = self.session.post(
                f"{self.api_url}/batch/analyze",
                params={"keywords": keywords},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            
            # Affichage dans le terminal
            print("\n" + "="*80)
            print(f"{'Keyword':<25} {'Volume':<12} {'Difficulty':<15} {'CPC':<10} {'Trend':<12}")
            print("="*80)
            
            for result in results:
                print(f"{result['keyword']:<25} {result['search_volume']:<12} {result['difficulty']:<15.1f} ${result['cpc']:<9.2f} {result['trend']:<12}")
            
            print("="*80)
            print(f"✓ Analysed {len(results)} keywords in {data.get('processing_time_ms', 0)}ms")
            
            # Export si demandé
            if output:
                self._export_results(results, output)
                print(f"✓ Results exported to {output}")
            
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            return []
    
    def generate_content_batch(self, keywords: List[str], content_type: str = "article", language: str = "fr", output: str = None):
        """Génère du contenu pour plusieurs keywords"""
        print(f"[*] Generating {content_type} content for {len(keywords)} keywords...")
        
        results = []
        for i, keyword in enumerate(keywords, 1):
            try:
                response = self.session.post(
                    f"{self.api_url}/generate/content",
                    json={
                        "keyword": keyword,
                        "content_type": content_type,
                        "language": language,
                        "tone": "professional"
                    },
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()
                results.append(data)
                print(f"  [{i}/{len(keywords)}] Generated {content_type} for '{keyword}' ({data['word_count']} words)")
                time.sleep(0.1)
                
            except requests.exceptions.RequestException as e:
                print(f"  ✗ Failed for '{keyword}': {e}", file=sys.stderr)
        
        if output:
            self._export_results(results, output)
            print(f"✓ Generated content exported to {output}")
        
        return results
    
    def _export_results(self, results: List[dict], filename: str):
        """Exporte les résultats en JSON ou CSV"""
        if filename.endswith('.json'):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        elif filename.endswith('.csv'):
            if results and isinstance(results[0], dict):
                keys = results[0].keys()
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    for row in results:
                        writer.writerow({k: str(v) if not isinstance(v, (int, float)) else v for k, v in row.items()})

def main():
    parser = argparse.ArgumentParser(
        description="SEO Analyzer CLI - Batch keyword analysis and content generation",
        epilog="Examples:\n"
               "  python cli.py analyze -k 'python tutorial' 'web development'\n"
               "  python cli.py generate -k 'seo tips' -t article -l fr -o output.json\n"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze keywords')
    analyze_parser.add_argument('-k', '--keywords', nargs='+', required=True, help='Keywords to analyze')
    analyze_parser.add_argument('-o', '--output', help='Output file (JSON or CSV)')
    analyze_parser.add_argument('--api', default=API_BASE, help='API base URL')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate SEO content')
    generate_parser.add_argument('-k', '--keywords', nargs='+', required=True, help='Keywords for content generation')
    generate_parser.add_argument('-t', '--type', default='article', choices=['article', 'meta', 'title', 'description'], help='Content type')
    generate_parser.add_argument('-l', '--language', default='fr', choices=['fr', 'en', 'es', 'de'], help='Language')
    generate_parser.add_argument('-o', '--output', help='Output file (JSON)')
    generate_parser.add_argument('--api', default=API_BASE, help='API base URL')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    cli = SEOAnalyzerCLI(args.api)
    
    if args.command == 'analyze':
        cli.analyze_keywords(args.keywords, args.output)
    elif args.command == 'generate':
        cli.generate_content_batch(args.keywords, args.type, args.language, args.output)

if __name__ == '__main__':
    main()
