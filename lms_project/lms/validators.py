from django.core.exceptions import ValidationError
import re


def validate_no_external_links(value):
    """Проверяет, что в тексте нет ссылок на сторонние ресурсы, кроме youtube.com."""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, value)

    for url in urls:
        if 'youtube.com' not in url:
            raise ValidationError(
                "Ссылки на сторонние ресурсы запрещены. Разрешены только ссылки на youtube.com."
            )
