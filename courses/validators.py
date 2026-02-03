import re
from urllib.parse import urlparse

from rest_framework import viewsets
from rest_framework.serializers import ValidationError

YOUTUBE_HOST = 'https://www.youtube.com'


def validate_only_youtube_url(value: str):
    """Разрешаем только Ютуб"""

    if not value:
        return value

    host = urlparse(value).netloc.lower()
    if host not in YOUTUBE_HOST:
        raise ValidationError("You can use only YouTube URLs")
    return value


URL_RE = re.compile(r"https?://[^\s]+")


def validate_no_external_links_except_youtube_url(text: str):
    """Если есть ссылки - разрешаем только YouTube URL"""

    if not text:
        return text
    urls = URL_RE.findall(text)
    for u in urls:
        host = urlparse(u).netloc.lower()
        if host not in YOUTUBE_HOST:
            raise ValidationError("You can use only YouTube URLs")
    return text