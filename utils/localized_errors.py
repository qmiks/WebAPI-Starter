"""
Localized Error Handling Module
Provides localized error messages and exceptions.
"""

from fastapi import HTTPException, Request
from typing import Optional, Dict, Any
from utils.i18n import t, i18n

class LocalizedException(HTTPException):
    """HTTPException with localized error messages."""
    
    def __init__(
        self,
        status_code: int,
        message_key: str,
        locale: str = None,
        detail: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        **translation_kwargs
    ):
        # Get localized message
        localized_detail = t(message_key, locale, **translation_kwargs)
        
        # Use provided detail as fallback if translation fails
        if localized_detail == message_key and detail:
            localized_detail = detail
        
        super().__init__(
            status_code=status_code,
            detail=localized_detail,
            headers=headers
        )
        
        self.message_key = message_key
        self.locale = locale or i18n.default_locale
        self.translation_kwargs = translation_kwargs

def get_request_locale(request: Request) -> str:
    """Extract locale from request state."""
    return getattr(request.state, 'locale', i18n.default_locale)

# Common localized exceptions
class LocalizedBadRequest(LocalizedException):
    """400 Bad Request with localized message."""
    def __init__(self, message_key: str = "general.bad_request", locale: str = None, **kwargs):
        super().__init__(400, message_key, locale, **kwargs)

class LocalizedUnauthorized(LocalizedException):
    """401 Unauthorized with localized message."""
    def __init__(self, message_key: str = "general.unauthorized", locale: str = None, **kwargs):
        super().__init__(401, message_key, locale, **kwargs)

class LocalizedForbidden(LocalizedException):
    """403 Forbidden with localized message."""
    def __init__(self, message_key: str = "general.forbidden", locale: str = None, **kwargs):
        super().__init__(403, message_key, locale, **kwargs)

class LocalizedNotFound(LocalizedException):
    """404 Not Found with localized message."""
    def __init__(self, message_key: str = "general.not_found", locale: str = None, **kwargs):
        super().__init__(404, message_key, locale, **kwargs)

class LocalizedValidationError(LocalizedException):
    """422 Validation Error with localized message."""
    def __init__(self, message_key: str = "general.validation_error", locale: str = None, **kwargs):
        super().__init__(422, message_key, locale, **kwargs)

class LocalizedInternalServerError(LocalizedException):
    """500 Internal Server Error with localized message."""
    def __init__(self, message_key: str = "general.internal_error", locale: str = None, **kwargs):
        super().__init__(500, message_key, locale, **kwargs)

# Helper functions for common authentication errors
def raise_invalid_credentials(request: Request = None, locale: str = None):
    """Raise localized invalid credentials error."""
    if not locale and request:
        locale = get_request_locale(request)
    raise LocalizedUnauthorized("auth.invalid_credentials", locale)

def raise_token_expired(request: Request = None, locale: str = None):
    """Raise localized token expired error."""
    if not locale and request:
        locale = get_request_locale(request)
    raise LocalizedUnauthorized("auth.token_expired", locale)

def raise_access_denied(request: Request = None, locale: str = None):
    """Raise localized access denied error."""
    if not locale and request:
        locale = get_request_locale(request)
    raise LocalizedForbidden("auth.access_denied", locale)

def raise_user_not_found(request: Request = None, locale: str = None):
    """Raise localized user not found error."""
    if not locale and request:
        locale = get_request_locale(request)
    raise LocalizedNotFound("users.user_not_found", locale)

def raise_item_not_found(request: Request = None, locale: str = None):
    """Raise localized item not found error."""
    if not locale and request:
        locale = get_request_locale(request)
    raise LocalizedNotFound("items.item_not_found", locale)

# Response helpers
def create_success_response(
    message_key: str = "general.success",
    data: Any = None,
    locale: str = None,
    **translation_kwargs
) -> Dict[str, Any]:
    """Create a localized success response."""
    return {
        "success": True,
        "message": t(message_key, locale, **translation_kwargs),
        "data": data,
        "locale": locale or i18n.default_locale
    }

def create_error_response(
    message_key: str = "general.error",
    error_code: str = None,
    locale: str = None,
    **translation_kwargs
) -> Dict[str, Any]:
    """Create a localized error response."""
    response = {
        "success": False,
        "message": t(message_key, locale, **translation_kwargs),
        "locale": locale or i18n.default_locale
    }
    if error_code:
        response["error_code"] = error_code
    return response
