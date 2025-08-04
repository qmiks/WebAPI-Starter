#!/usr/bin/env python3
"""
Demo Runner
Convenient script to run various demo scripts and utilities.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_demo(demo_file):
    """Run a single demo file"""
    project_root = Path(__file__).parent.parent
    demo_path = project_root / "demos" / demo_file
    if not demo_path.exists():
        print(f"❌ Demo file not found: {demo_path}")
        return False
    
    print(f"🎯 Running Demo: {demo_file}")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, str(demo_path)], 
                              cwd=project_root, 
                              capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        return False

def list_demos():
    """List all available demos"""
    project_root = Path(__file__).parent.parent
    demos_dir = project_root / "demos"
    if not demos_dir.exists():
        print("❌ Demos directory not found")
        return
    
    demo_files = sorted([f.name for f in demos_dir.glob("*.py")])
    
    print("📋 Available Demos and Utilities:")
    print("=" * 50)
    
    categories = {
        "🎯 Demo Scripts": {
            "Authentication": [
                "api_token_demo.py",
                "swagger_demo.py"
            ],
            "Token Management": [
                "demo_token_creator.py",
                "get_bearer_token.py"
            ]
        },
        "🔧 Utility Scripts": {
            "Database Tools": [
                "sqlite_migration_demo.py",
                "starter_users_demo.py"
            ],
            "User Management": [
                "user_registration_demo.py"
            ]
        }
    }
    
    for main_category, subcategories in categories.items():
        print(f"\n{main_category}:")
        
        for subcategory, demos in subcategories.items():
            print(f"\n  📂 {subcategory}:")
            for demo in demos:
                if demo in demo_files:
                    print(f"    ✅ {demo}")
                else:
                    print(f"    ❓ {demo} (not found)")
    
    # Show any demos not categorized
    all_categorized = set()
    for subcategories in categories.values():
        for demos in subcategories.values():
            all_categorized.update(demos)
    
    uncategorized = set(demo_files) - all_categorized
    if uncategorized:
        print(f"\n❓ Other Files:")
        for demo in sorted(uncategorized):
            print(f"  • {demo}")
    
    # Show non-Python files
    other_files = [f.name for f in demos_dir.iterdir() 
                   if f.is_file() and not f.name.endswith('.py') and f.name != '__init__.py']
    if other_files:
        print(f"\n📄 Sample Files:")
        for file in sorted(other_files):
            print(f"  📄 {file}")

def run_category(category):
    """Run all demos in a category"""
    categories = {
        "admin": [
            "admin_structure_demo.py",
            "user_portal_access_demo.py"
        ],
        "auth": [
            "api_token_demo.py",
            "get_test_token_demo.py",
            "swagger_demo.py",
            "login_context_demo.py",
            "login_error_context_demo.py"
        ],
        "tokens": [
            "demo_token_creator.py",
            "demo_credentials_fix.py",
            "token_generator.py",
            "get_bearer_token.py",
            "simple_token_guide.py"
        ],
        "debug": [
            "debug_auth.py",
            "debug_client_apps.py",
            "check_db_users.py",
            "auth_fix_summary.py"
        ],
        "utils": [
            "run.py"
        ]
    }
    
    if category not in categories:
        print(f"❌ Unknown category: {category}")
        print(f"Available categories: {', '.join(categories.keys())}")
        return False
    
    demos = categories[category]
    success_count = 0
    
    print(f"🎯 Running {category.upper()} demos...")
    print("=" * 60)
    
    for demo in demos:
        if run_demo(demo):
            success_count += 1
        print()  # Add spacing between demos
    
    print(f"📊 Results: {success_count}/{len(demos)} demos completed successfully")
    return success_count == len(demos)

def open_sample_file(filename):
    """Open a sample file in the default application"""
    file_path = Path("demos") / filename
    if not file_path.exists():
        print(f"❌ Sample file not found: {file_path}")
        return False
    
    try:
        if sys.platform.startswith('win'):
            os.startfile(file_path)
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', file_path])
        else:
            subprocess.run(['xdg-open', file_path])
        print(f"✅ Opened {filename}")
        return True
    except Exception as e:
        print(f"❌ Error opening file: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Demo Runner for Web API Application")
    parser.add_argument("--list", "-l", action="store_true", help="List all available demos")
    parser.add_argument("--demo", "-d", help="Run a specific demo file")
    parser.add_argument("--category", "-c", help="Run all demos in a category (admin, auth, tokens, debug, utils)")
    parser.add_argument("--all", "-a", action="store_true", help="Run all demos")
    parser.add_argument("--open", "-o", help="Open a sample file (error_page_sample.html, test_login.html)")
    
    args = parser.parse_args()
    
    if args.list:
        list_demos()
    elif args.demo:
        run_demo(args.demo)
    elif args.category:
        run_category(args.category)
    elif args.open:
        open_sample_file(args.open)
    elif args.all:
        # Run all categories
        categories = ["admin", "auth", "tokens", "debug", "utils"]
        for category in categories:
            print(f"\n{'='*60}")
            print(f"🎯 RUNNING {category.upper()} DEMOS")
            print(f"{'='*60}")
            run_category(category)
    else:
        print("🎯 Web API Demo Runner")
        print("=" * 30)
        print()
        print("Usage:")
        print("  python run_demos.py --list               # List all demos")
        print("  python run_demos.py --demo <file>        # Run specific demo")
        print("  python run_demos.py --category auth      # Run auth demos")
        print("  python run_demos.py --all                # Run all demos")
        print("  python run_demos.py --open sample.html   # Open sample file")
        print()
        print("Categories: admin, auth, tokens, debug, utils")
        print()
        print("Sample files: error_page_sample.html, test_login.html")

if __name__ == "__main__":
    main()
