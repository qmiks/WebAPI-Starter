#!/usr/bin/env python3
"""
Test translation system
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils.i18n import get_translations_for_locale, t

def test_translations():
    """Test translation function"""
    print("🌍 Testing Translation System")
    print("=" * 40)
    
    # Test Polish translations
    locale = 'pl'
    translations = get_translations_for_locale(locale)
    
    print(f"Locale: {locale}")
    print(f"Translations loaded: {bool(translations)}")
    
    # Test specific keys that should exist
    test_keys = [
        "dashboard.table.id",
        "dashboard.table.username", 
        "dashboard.table.email",
        "dashboard.table.name",
        "dashboard.table.status",
        "dashboard.table.actions"
    ]
    
    for key in test_keys:
        translation = t(key, locale)
        print(f"  {key} -> '{translation}'")
        
        if translation == key:
            print(f"    ❌ Translation missing for: {key}")
        else:
            print(f"    ✅ Translation found")

    # Test direct access to dashboard.table section
    print("\nDirect access test:")
    if 'dashboard' in translations:
        print("  ✅ dashboard section exists")
        if 'table' in translations['dashboard']:
            print("  ✅ table section exists")
            table_keys = translations['dashboard']['table']
            print(f"  Available table keys: {list(table_keys.keys())}")
        else:
            print("  ❌ table section missing")
    else:
        print("  ❌ dashboard section missing")

if __name__ == "__main__":
    test_translations()
