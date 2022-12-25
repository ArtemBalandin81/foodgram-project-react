import re

from django.core.exceptions import ValidationError

PATTERN = r'^#(?:[0-9a-fA-F]{1,2}){3}$'

def validate_color(value):
    """Проверяем, что тег соответствует HEX-формату"""
    if not re.fullmatch(PATTERN, value, flags=0):
        raise ValidationError(
            f"""color не соответствует HEX-формату."""
        )
    return value
