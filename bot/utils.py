"""
Utility functions for AlphaDroid Telegram Bot
"""
import re
from typing import Optional
from telegram import Update
from telegram.ext import CallbackContext
import logging

logger = logging.getLogger(__name__)


def sanitize_url(url: Optional[str]) -> Optional[str]:
    """
    Sanitize URL by removing duplicate protocol prefixes.
    
    Fixes URLs like 'https://https://example.com' -> 'https://example.com'
    
    Args:
        url: The URL to sanitize
        
    Returns:
        Sanitized URL or None if input is None
    """
    if not url:
        return None
    
    # Remove duplicate https:// or http://
    url = re.sub(r'^(https?://)+', r'\1', url)
    
    # Ensure URL starts with a protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url.strip()


async def safe_reply(
    update: Update,
    text: str,
    **kwargs
) -> bool:
    """
    Safely send a reply message with proper error handling.
    
    Args:
        update: Telegram update object
        text: Message text to send
        **kwargs: Additional arguments for reply_text
        
    Returns:
        True if message was sent successfully, False otherwise
    """
    try:
        if update.message:
            await update.message.reply_text(text, **kwargs)
            return True
        elif update.callback_query:
            await update.callback_query.message.reply_text(text, **kwargs)
            return True
        else:
            logger.warning("No message or callback_query in update")
            return False
    except Exception as e:
        logger.error(f"Error sending reply: {e}")
        return False


def format_error_message(error_type: str, details: str = "") -> str:
    """
    Format user-friendly error messages.
    
    Args:
        error_type: Type of error (e.g., 'device_not_found', 'network_error')
        details: Additional error details
        
    Returns:
        Formatted error message
    """
    error_messages = {
        'device_not_found': "❌ Device not found. Please check the device codename and try again.",
        'network_error': "⚠️ Network error occurred. Please try again later.",
        'timeout': "⏱️ Request timed out. The server is taking too long to respond.",
        'invalid_url': "❌ Invalid URL detected. Please contact the bot administrator.",
        'api_error': "❌ API error occurred. Please try again later.",
        'unknown': "❌ An unexpected error occurred. Please try again later."
    }
    
    base_message = error_messages.get(error_type, error_messages['unknown'])
    
    if details:
        return f"{base_message}\n\n_Details: {details}_"
    
    return base_message


def validate_device_code(device_code: str) -> bool:
    """
    Validate device codename format.
    
    Args:
        device_code: Device codename to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not device_code:
        return False
    
    # Device codes are typically lowercase alphanumeric with optional underscores/hyphens
    pattern = r'^[a-z0-9_-]+$'
    return bool(re.match(pattern, device_code.lower()))


def get_status_info(version: str) -> tuple[str, str]:
    """
    Get status icon and text based on version number.
    
    Args:
        version: Version string (e.g., "2.1", "1.5")
        
    Returns:
        Tuple of (status_icon, status_text)
    """
    try:
        major_version = float(version.split(".")[0])
        if major_version >= 2.0:
            return "🟢", "Active"
        else:
            return "🔴", "Inactive"
    except (ValueError, IndexError):
        return "⚪", "Unknown"
