"""
Multi-Language Support Demo
Demonstrates the internationalization features of the WebAPI Starter application.
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class I18nDemo:
    """Demo class for testing multi-language support."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_locale_detection(self):
        """Test automatic locale detection from Accept-Language header."""
        print("🌍 Testing locale detection...")
        
        test_cases = [
            ("en-US,en;q=0.9", "English"),
            ("es-ES,es;q=0.9", "Spanish"),  
            ("fr-FR,fr;q=0.9", "French"),
            ("de-DE,de;q=0.9", "German"),
            ("ja-JP,ja;q=0.9", "Default (English fallback)")
        ]
        
        for accept_lang, description in test_cases:
            headers = {"Accept-Language": accept_lang}
            
            async with self.session.get(
                f"{self.base_url}/api/v1/i18n/translate/messages.welcome",
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"  {description}: {data['translation']} (locale: {data['locale']})")
                else:
                    print(f"  {description}: Error {response.status}")
    
    async def test_url_parameter_locale(self):
        """Test locale selection via URL parameter."""
        print("\n🔗 Testing URL parameter locale override...")
        
        locales = ["en", "es", "fr", "de"]
        
        for locale in locales:
            async with self.session.get(
                f"{self.base_url}/api/v1/i18n/translate/messages.welcome?lang={locale}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"  {locale.upper()}: {data['translation']}")
                else:
                    print(f"  {locale.upper()}: Error {response.status}")
    
    async def test_error_messages(self):
        """Test localized error messages."""
        print("\n❌ Testing localized error messages...")
        
        # Test user not found errors in different languages
        locales = ["en", "es", "fr", "de"]
        
        for locale in locales:
            headers = {"Accept-Language": f"{locale}-{locale.upper()}"}
            
            # Try to access a non-existent user (assuming no auth for demo)
            async with self.session.get(
                f"{self.base_url}/api/v1/i18n/translate/users.user_not_found",
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"  {locale.upper()}: {data['translation']}")
    
    async def test_form_labels(self):
        """Test form field labels in different languages."""
        print("\n📝 Testing form labels...")
        
        form_fields = ["forms.name", "forms.email", "forms.password", "forms.submit"]
        locales = ["en", "es", "fr", "de"]
        
        for locale in locales:
            print(f"\n  {locale.upper()} Form Labels:")
            for field in form_fields:
                async with self.session.get(
                    f"{self.base_url}/api/v1/i18n/translate/{field}?lang={locale}"
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        field_name = field.split('.')[1]
                        print(f"    {field_name.capitalize()}: {data['translation']}")
    
    async def test_supported_locales(self):
        """Test getting supported locales."""
        print("\n🌐 Supported locales:")
        
        async with self.session.get(f"{self.base_url}/api/v1/i18n/locales") as response:
            if response.status == 200:
                data = await response.json()
                print(f"  Default: {data['default_locale']}")
                print(f"  Supported: {', '.join(data['supported_locales'])}")
            else:
                print(f"  Error: {response.status}")
    
    async def test_full_translations(self):
        """Test getting full translation sets."""
        print("\n📚 Testing full translation sets...")
        
        locales = ["en", "es"]
        
        for locale in locales:
            async with self.session.get(
                f"{self.base_url}/api/v1/i18n/translations/{locale}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    translations = data['translations']
                    app_title = translations.get('app', {}).get('title', 'N/A')
                    auth_section = len(translations.get('auth', {}))
                    print(f"  {locale.upper()}: App title = '{app_title}', Auth keys = {auth_section}")
                else:
                    print(f"  {locale.upper()}: Error {response.status}")
    
    async def run_all_tests(self):
        """Run all demo tests."""
        print("🚀 WebAPI Starter - Multi-Language Support Demo")
        print("=" * 60)
        
        try:
            await self.test_supported_locales()
            await self.test_locale_detection()
            await self.test_url_parameter_locale()
            await self.test_error_messages()
            await self.test_form_labels()
            await self.test_full_translations()
            
            print("\n✅ Demo completed successfully!")
            print("\n💡 Usage Examples:")
            print("  - Add ?lang=es to any URL for Spanish")
            print("  - Set Accept-Language header for automatic detection")
            print("  - Use /api/v1/i18n/translations/{locale} for frontend i18n")
            
        except aiohttp.ClientConnectorError:
            print("❌ Error: Could not connect to the server.")
            print("   Make sure the WebAPI Starter is running on http://localhost:8000")
            print("   Run: python main.py")
        except Exception as e:
            print(f"❌ Error: {e}")

async def main():
    """Main demo function."""
    async with I18nDemo() as demo:
        await demo.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
