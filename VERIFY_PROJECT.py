#!/usr/bin/env python3
"""
SEO Analyzer Pro - Verification & Health Check Script
Run this to verify everything is working correctly
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_files():
    """Check that all Python files compile"""
    print("=" * 80)
    print("VERIFYING PYTHON FILES")
    print("=" * 80)
    
    python_files = [
        "backend/main.py",
        "backend/test_api.py",
        "cli/cli.py",
        "setup.py"
    ]
    
    all_good = True
    for file in python_files:
        try:
            with open(file, 'r') as f:
                compile(f.read(), file, 'exec')
            print(f"✅ {file}")
        except SyntaxError as e:
            print(f"❌ {file}: {e}")
            all_good = False
        except FileNotFoundError:
            print(f"❌ {file}: NOT FOUND")
            all_good = False
    
    return all_good

def check_documentation():
    """Check that all documentation files exist"""
    print("\n" + "=" * 80)
    print("VERIFYING DOCUMENTATION FILES")
    print("=" * 80)
    
    doc_files = [
        "README.md",
        "QUICKSTART.md",
        "MONETIZATION.md",
        "BUSINESS_PLAN.md",
        "DEPLOYMENT.md",
        "ARCHITECTURE.md",
        "docs/INTEGRATIONS.md",
        "docs/DEVELOPMENT.md",
        "docs/SECURITY.md",
        "docs/FAQ.md",
    ]
    
    all_good = True
    for file in doc_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print(f"✅ {file} ({size:,} bytes)")
        else:
            print(f"❌ {file}: NOT FOUND")
            all_good = False
    
    return all_good

def check_configuration():
    """Check configuration files"""
    print("\n" + "=" * 80)
    print("VERIFYING CONFIGURATION FILES")
    print("=" * 80)
    
    config_files = [
        "Dockerfile",
        "docker-compose.yml",
        ".env.example",
        "backend/requirements.txt",
        ".gitignore",
        "LICENSE"
    ]
    
    all_good = True
    for file in config_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}: NOT FOUND")
            all_good = False
    
    return all_good

def check_scripts():
    """Check deployment scripts"""
    print("\n" + "=" * 80)
    print("VERIFYING SCRIPTS")
    print("=" * 80)
    
    scripts = [
        "scripts/setup_local.sh",
        "scripts/deploy_digitalocean.sh",
        "scripts/deploy_aws.sh",
        "scripts/api_client_example.py",
        "scripts/pricing_calculator.py",
        "scripts/growth_projections.py"
    ]
    
    all_good = True
    for script in scripts:
        if Path(script).exists():
            print(f"✅ {script}")
        else:
            print(f"❌ {script}: NOT FOUND")
            all_good = False
    
    return all_good

def check_git():
    """Check git repository"""
    print("\n" + "=" * 80)
    print("VERIFYING GIT REPOSITORY")
    print("=" * 80)
    
    try:
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            if "nothing to commit, working tree clean" in result.stdout:
                print("✅ Git repository is clean")
                
                # Get commit count
                result = subprocess.run(
                    ["git", "rev-list", "--count", "HEAD"],
                    capture_output=True,
                    text=True
                )
                commit_count = result.stdout.strip()
                print(f"✅ Total commits: {commit_count}")
                
                return True
            else:
                print("❌ Git repository has uncommitted changes")
                print(result.stdout)
                return False
        else:
            print("❌ Not a git repository")
            return False
    except Exception as e:
        print(f"⚠️  Could not verify git: {e}")
        return False

def check_file_count():
    """Check total file count"""
    print("\n" + "=" * 80)
    print("VERIFYING FILE COUNT")
    print("=" * 80)
    
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True
        )
        file_count = len(result.stdout.strip().split('\n'))
        print(f"✅ Total tracked files: {file_count}")
        return file_count >= 40  # Should have 40+ files
    except:
        print("⚠️  Could not count files")
        return False

def main():
    """Run all checks"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  SEO ANALYZER PRO - VERIFICATION & HEALTH CHECK".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    results = {
        "Python files": check_python_files(),
        "Documentation": check_documentation(),
        "Configuration": check_configuration(),
        "Scripts": check_scripts(),
        "Git repository": check_git(),
        "File count": check_file_count(),
    }
    
    # Summary
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    
    all_good = True
    for check, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check:.<40} {status}")
        if not result:
            all_good = False
    
    print("=" * 80)
    
    if all_good:
        print("\n✅ ALL CHECKS PASSED!")
        print("\nYour SEO Analyzer Pro project is ready!")
        print("\nNext steps:")
        print("  1. bash scripts/setup_local.sh")
        print("  2. source venv/bin/activate")
        print("  3. uvicorn backend.main:app --reload")
        print("  4. Open http://localhost:8000")
        return 0
    else:
        print("\n❌ SOME CHECKS FAILED!")
        print("Please fix the issues above before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
