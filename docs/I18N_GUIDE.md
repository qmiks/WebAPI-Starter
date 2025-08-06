# Multi-Language Support (i18n) Guide

The WebAPI Starter now includes comprehensive internationalization (i18n) support, allowing your application to serve content in multiple languages.

## 🌍 Supported Languages

- **English (en)** - Default language
- **Spanish (es)** - Español
- **French (fr)** - Français
- **German (de)** - Deutsch

## 🚀 Quick Start

### 1. Automatic Language Detection

The application automatically detects the user's preferred language from:

1. **URL Parameter**: `?lang=es`
2. **Accept-Language Header**: Browser automatically sends this
3. **Default Fallback**: English (en)

### 2. API Endpoints

#### Get Supported Locales
```bash
GET /api/v1/i18n/locales
```

Response:
```json
{
  "supported_locales": ["en", "es", "fr", "de"],
  "default_locale": "en"
}
```

#### Get All Translations for a Locale
```bash
GET /api/v1/i18n/translations/es
```

#### Translate a Specific Key
```bash
GET /api/v1/i18n/translate/users.user_not_found?lang=es
```

Response:
```json
{
  "key": "users.user_not_found",
  "locale": "es", 
  "translation": "Usuario no encontrado"
}
```

### 3. Using in Frontend

#### JavaScript Example
```javascript
// Set language preference
const setLanguage = async (locale) => {
  const response = await fetch(`/api/v1/i18n/translations/${locale}`);
  const data = await response.json();
  return data.translations;
};

// Use with URL parameter
window.location.href = "/?lang=es";

// Use with Accept-Language header
fetch('/api/v1/users', {
  headers: {
    'Accept-Language': 'es-ES,es;q=0.9'
  }
});
```

#### HTML Examples
```html
<!-- Language selector -->
<select onchange="changeLanguage(this.value)">
  <option value="en">English</option>
  <option value="es">Español</option>
  <option value="fr">Français</option>
  <option value="de">Deutsch</option>
</select>

<!-- Using URL parameters -->
<a href="?lang=es">Español</a>
<a href="?lang=fr">Français</a>
```

## 🛠️ Development Guide

### Adding New Languages

1. **Create translation file**:
   ```bash
   mkdir locales/it
   cp locales/en/messages.json locales/it/messages.json
   ```

2. **Translate the content**:
   ```json
   {
     "app": {
       "title": "WebAPI Starter",
       "description": "Un'applicazione WebAPI Starter completa..."
     },
     "users": {
       "user_not_found": "Utente non trovato"
     }
   }
   ```

3. **Restart the application** - new locales are auto-detected

### Adding New Translation Keys

1. **Add to all language files**:
   ```json
   {
     "new_section": {
       "new_key": "English text",
       "another_key": "More English text"
     }
   }
   ```

2. **Use in code**:
   ```python
   from utils.i18n import t
   
   message = t("new_section.new_key", locale, param1="value")
   ```

### Using in API Endpoints

```python
from fastapi import APIRouter, Request
from utils.localized_errors import get_request_locale, LocalizedNotFound
from utils.i18n import t

@router.get("/example")
async def example_endpoint(request: Request):
    locale = get_request_locale(request)
    
    # Translate message
    message = t("messages.welcome", locale)
    
    # Raise localized error
    if not_found:
        raise LocalizedNotFound("users.user_not_found", locale)
    
    return {"message": message, "locale": locale}
```

### Using in Templates

```python
# In route handler
@app.get("/")
async def root(request: Request):
    locale = getattr(request.state, 'locale', 'en')
    return templates.TemplateResponse("page.html", {
        "request": request,
        "locale": locale,
        "t": lambda key, **kwargs: t(key, locale, **kwargs)
    })
```

```html
<!-- In template -->
<h1>{{ t("messages.welcome") }}</h1>
<p>{{ t("app.description") }}</p>
```

## 📝 Translation File Structure

```json
{
  "app": {
    "title": "Application title",
    "description": "Application description"
  },
  "auth": {
    "invalid_credentials": "Invalid credentials",
    "access_denied": "Access denied"
  },
  "users": {
    "user_created": "User created successfully",
    "user_not_found": "User not found"
  },
  "forms": {
    "name": "Name",
    "email": "Email",
    "submit": "Submit"
  },
  "general": {
    "success": "Success",
    "error": "Error"
  }
}
```

## 🎯 Error Handling

### Localized Exceptions

```python
from utils.localized_errors import (
    LocalizedBadRequest,
    LocalizedNotFound,
    LocalizedUnauthorized
)

# Raise localized errors
raise LocalizedBadRequest("users.email_already_exists", locale)
raise LocalizedNotFound("users.user_not_found", locale)
raise LocalizedUnauthorized("auth.invalid_credentials", locale)
```

### Response Helpers

```python
from utils.localized_errors import create_success_response, create_error_response

# Success response
return create_success_response("users.user_created", user_data, locale)

# Error response  
return create_error_response("general.validation_error", "VALIDATION_001", locale)
```

## 🧪 Testing

Run the i18n demo to test all features:

```bash
python demos/i18n_demo.py
```

This will test:
- Automatic locale detection
- URL parameter overrides
- Error message localization
- Form label translations
- Full translation sets

## 🔧 Configuration

### Environment Variables

```bash
# Default locale (optional, defaults to "en")
DEFAULT_LOCALE=en

# Locales directory (optional, defaults to "locales")
LOCALES_DIR=locales
```

### Customizing I18n Instance

```python
from utils.i18n import I18n

# Custom configuration
custom_i18n = I18n(
    locales_dir="custom_locales",
    default_locale="es"
)
```

## 🌟 Best Practices

1. **Always provide fallbacks**: Include English translations for all keys
2. **Use descriptive keys**: `users.validation.email_invalid` vs `error1`
3. **Group related translations**: Organize by feature/section
4. **Test all languages**: Ensure UI doesn't break with longer translations
5. **Consider RTL languages**: Plan for right-to-left text if needed
6. **Use parameters for dynamic content**: `"welcome": "Hello {name}!"`

## 🚨 Common Issues

### Translation Not Found
- Check the key exists in the translation file
- Verify the JSON syntax is valid
- Ensure the locale is supported

### Wrong Locale Detected
- Check Accept-Language header format
- Use URL parameter to override: `?lang=es`
- Verify locale files exist in the locales directory

### Template Errors
- Ensure `t` function is passed to template context
- Check template syntax: `{{ t("key") }}`
- Verify locale variable is available

## 📚 Example Integration

See `demos/i18n_demo.py` for a complete example of how to integrate multi-language support into your application.
