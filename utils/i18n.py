"""
Internationalization (i18n) Support Module
Provides multi-language support for the WebAPI Starter application.
"""

import json
import os
from typing import Dict, Optional, Any
from pathlib import Path
from fastapi import Request, Header
from functools import lru_cache

class I18n:
    """Internationalization manager for multi-language support."""
    
    def __init__(self, locales_dir: str = "locales", default_locale: str = "en"):
        self.locales_dir = Path(locales_dir)
        self.default_locale = default_locale
        self.supported_locales = self._load_supported_locales()
        self._translations: Dict[str, Dict[str, Any]] = {}
        self._load_all_translations()
    
    def _load_supported_locales(self) -> list:
        """Load list of supported locales from the locales directory."""
        if not self.locales_dir.exists():
            return [self.default_locale]
        
        locales = []
        for item in self.locales_dir.iterdir():
            if item.is_dir() and (item / "messages.json").exists():
                locales.append(item.name)
        
        return locales if locales else [self.default_locale]
    
    def _load_all_translations(self):
        """Load all translation files into memory."""
        for locale in self.supported_locales:
            self._load_translations(locale)
    
    @lru_cache(maxsize=128)
    def _load_translations(self, locale: str) -> Dict[str, Any]:
        """Load translations for a specific locale."""
        if locale in self._translations:
            return self._translations[locale]
        
        translations_file = self.locales_dir / locale / "messages.json"
        
        try:
            if translations_file.exists():
                with open(translations_file, 'r', encoding='utf-8') as f:
                    translations = json.load(f)
                    self._translations[locale] = translations
                    return translations
            else:
                # Fall back to default locale
                if locale != self.default_locale:
                    return self._load_translations(self.default_locale)
                else:
                    return {}
        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Error loading translations for locale '{locale}': {e}")
            if locale != self.default_locale:
                return self._load_translations(self.default_locale)
            return {}
    
    def get_locale_from_request(self, request: Request, accept_language: Optional[str] = None) -> str:
        """
        Determine the best locale for a request based on:
        1. URL parameter (?lang=es)
        2. Accept-Language header
        3. Default locale
        """
        # Check URL parameter first
        if hasattr(request, 'query_params'):
            lang_param = request.query_params.get('lang')
            if lang_param and lang_param in self.supported_locales:
                return lang_param
        
        # Check Accept-Language header
        if accept_language:
            # Parse Accept-Language header (simplified)
            for lang_range in accept_language.split(','):
                lang = lang_range.split(';')[0].strip().lower()
                # Check exact match
                if lang in self.supported_locales:
                    return lang
                # Check language part only (e.g., 'en' from 'en-US')
                lang_part = lang.split('-')[0]
                if lang_part in self.supported_locales:
                    return lang_part
        
        return self.default_locale
    
    def translate(self, key: str, locale: str = None, **kwargs) -> str:
        """
        Translate a key to the specified locale.
        
        Args:
            key: Translation key in dot notation (e.g., 'auth.invalid_credentials')
            locale: Target locale, defaults to default_locale
            **kwargs: Variables for string formatting
        
        Returns:
            Translated string or the key if translation not found
        """
        if locale is None:
            locale = self.default_locale
        
        if locale not in self.supported_locales:
            locale = self.default_locale
        
        translations = self._load_translations(locale)
        
        # Navigate through nested dictionary using dot notation
        keys = key.split('.')
        value = translations
        
        try:
            for k in keys:
                value = value[k]
            
            # If kwargs provided, format the string
            if kwargs and isinstance(value, str):
                try:
                    return value.format(**kwargs)
                except (KeyError, ValueError):
                    # If formatting fails, return the unformatted string
                    return value
            
            return str(value)
        
        except (KeyError, TypeError):
            # If translation not found, try default locale
            if locale != self.default_locale:
                return self.translate(key, self.default_locale, **kwargs)
            # If still not found, return the key itself
            return key
    
    def get_translations(self, locale: str = None) -> Dict[str, Any]:
        """Get all translations for a locale."""
        if locale is None:
            locale = self.default_locale
        return self._load_translations(locale)
    
    def reload_translations(self):
        """Reload all translation files (useful for development)."""
        self._translations.clear()
        self._load_all_translations()

# Global i18n instance
i18n = I18n()

def get_locale_from_request(request: Request, accept_language: Optional[str] = Header(None)) -> str:
    """
    Dependency to get locale from request with robust fallback mechanism.
    Priority: 
    1. URL parameter (?lang=es) 
    2. Session cookie (lang_preference)
    3. Accept-Language header
    4. Default locale
    """
    # Check URL parameter first (highest priority)
    if hasattr(request, 'query_params'):
        lang_param = request.query_params.get('lang')
        if lang_param and lang_param in i18n.supported_locales:
            return lang_param
    
    # Check session cookie (second priority)
    if hasattr(request, 'cookies'):
        cookie_lang = request.cookies.get('lang_preference')
        if cookie_lang and cookie_lang in i18n.supported_locales:
            return cookie_lang
    
    # Check Accept-Language header (third priority)
    return i18n.get_locale_from_request(request, accept_language)

def t(key: str, locale: str = None, **kwargs) -> str:
    """Shorthand function for translation."""
    return i18n.translate(key, locale, **kwargs)

def get_translations_for_locale(locale: str = None) -> Dict[str, Any]:
    """Get all translations for a locale (useful for frontend)."""
    return i18n.get_translations(locale)

class LocalizedResponse:
    """Helper class for creating localized API responses."""
    
    def __init__(self, locale: str = None):
        self.locale = locale or i18n.default_locale
    
    def success(self, message_key: str = "general.success", data: Any = None, **kwargs) -> Dict[str, Any]:
        """Create a localized success response."""
        return {
            "success": True,
            "message": t(message_key, self.locale, **kwargs),
            "data": data,
            "locale": self.locale
        }
    
    def error(self, message_key: str = "general.error", error_code: str = None, **kwargs) -> Dict[str, Any]:
        """Create a localized error response."""
        response = {
            "success": False,
            "message": t(message_key, self.locale, **kwargs),
            "locale": self.locale
        }
        if error_code:
            response["error_code"] = error_code
        return response

def create_localized_response(locale: str = None) -> LocalizedResponse:
    """Factory function to create a LocalizedResponse instance."""
    return LocalizedResponse(locale)

# Middleware to add locale to request state
class LocaleMiddleware:
    """Middleware to automatically detect and set locale for each request."""
    
    def __init__(self, app, i18n_instance: I18n = None):
        self.app = app
        self.i18n = i18n_instance or i18n
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Create a request object to get headers
            from fastapi import Request
            request = Request(scope, receive)
            
            # Get Accept-Language header
            accept_language = request.headers.get("accept-language")
            
            # Determine locale
            locale = self.i18n.get_locale_from_request(request, accept_language)
            
            # Add locale to request state
            if "state" not in scope:
                scope["state"] = {}
            scope["state"]["locale"] = locale
        
        await self.app(scope, receive, send)
