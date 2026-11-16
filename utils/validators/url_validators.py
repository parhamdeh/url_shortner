from django.core.exceptions import ValidationError
from django.core.validators import URLValidator



def validate_url(url: str) -> None:
    """
    Validate a URL using Django's built-in URL validator.

    Args:
        url: URL that should be validated.

    Raises:
        ValidationError: If the URL is invalid.
    """
    validator = URLValidator()

    try:
        validator(url)
    except ValidationError:
        raise ValidationError("Invalid Url")