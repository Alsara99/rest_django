from rest_framework.serializers import ValidationError
from urllib.parse import urlparse


class YouTubeOnlyValidator:
    def __init__(self, field: str):
        self.field = field

    def __call__(self, attrs):
        url = attrs.get(self.field)

        if not url:
            return

        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()

        allowed_domains = (
            'youtube.com',
            'www.youtube.com',
        )

        if domain not in allowed_domains:
            raise ValidationError(
                {self.field: 'Допустимы только ссылки на YouTube'}
            )
