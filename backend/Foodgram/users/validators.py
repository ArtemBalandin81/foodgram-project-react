import re

from django.core.exceptions import ValidationError

ANTI_PATTERN = r'(?!^[\w.@+-]+\Z).*'
REGEX_USERNAME = re.compile(r'^[\w.@+-]+\Z')


def check_username(value):
    """Проверяем, что пользователь не использует имя 'me'."""
    if value == 'me':
        raise ValidationError(
            f'Имя {value} пользователя использовать запрещено!'
        )
    if not REGEX_USERNAME.fullmatch(value):
        result = re.search(ANTI_PATTERN, value)
        raise ValidationError(
            f"""
            Используйте только цифры, буквы и символы ".@+-".
            Символы {set(result.group(0))} запрещены.
            """
        )
    return value
