#!/usr/bin/env python3
"""
Quick script to fix Unicode emoji issues in demos for Windows compatibility
"""

import os
import re

def fix_emojis_in_file(filepath):
    """Replace common emojis with ASCII equivalents"""
    
    emoji_replacements = {
        '🗄️': '[DB]',
        '📁': '[FILE]',
        '📍': '[LOC]',
        '📏': '[SIZE]',
        '🕒': '[TIME]',
        '✅': '[OK]',
        '❌': '[ERR]',
        '🏗️': '[STRUCT]',
        '📋': '[LIST]',
        '📊': '[DATA]',
        '📈': '[COUNT]',
        '🔍': '[INDEX]',
        '👥': '[USERS]',
        '👑': '[ADMIN]',
        '🛡️': '[MOD]',
        '👤': '[USER]',
        '🟢': '[ACTIVE]',
        '🔴': '[INACTIVE]',
        '📦': '[ITEMS]',
        '📝': '[DESC]',
        '💰': '[PRICE]',
        '❓': '[UNKNOWN]',
        '🔑': '[CLIENT]',
        '🚀': '[MIGRATE]',
        '📖': '[USAGE]',
        '🐍': '[PYTHON]',
        '🧪': '[TEST]',
        '🌐': '[WEB]',
        '📚': '[API]',
        '🛠️': '[ADMIN]',
        '🎉': '[SUMMARY]',
        '🔐': '[AUTH]',
        '🎯': '[DEMO]',
        '🔧': '[UTIL]',
        '📄': '[FILE]',
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for emoji, replacement in emoji_replacements.items():
            content = content.replace(emoji, replacement)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed emojis in: {filepath}")
            return True
        else:
            print(f"No emojis found in: {filepath}")
            return False
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    demo_dir = "demos"
    
    if not os.path.exists(demo_dir):
        print("Demos directory not found!")
        return
    
    demo_files = [
        "sqlite_migration_demo.py",
        "starter_users_demo.py",
        "swagger_demo.py",
        "user_registration_demo.py",
        "api_token_demo.py",
        "get_bearer_token.py",
        "demo_token_creator.py"
    ]
    
    print("Fixing emoji encoding issues in demo files...")
    
    fixed_count = 0
    for demo_file in demo_files:
        filepath = os.path.join(demo_dir, demo_file)
        if os.path.exists(filepath):
            if fix_emojis_in_file(filepath):
                fixed_count += 1
        else:
            print(f"File not found: {filepath}")
    
    print(f"\nFixed {fixed_count} demo files")
    print("Demos should now work properly in Windows PowerShell")

if __name__ == "__main__":
    main()
