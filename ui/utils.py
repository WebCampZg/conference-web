import logging
from django.conf import settings
from functools import lru_cache
from os import path

logger = logging.getLogger(__name__)


@lru_cache(maxsize=128)
def get_icon_svg(name):
    icon_path = path.join(settings.BASE_DIR, f"ui/static/icons/{name}.svg")

    if not path.exists(icon_path):
        logger.error(f"Icon not found: {name}")
        return ""

    with open(icon_path, "r") as f:
        return f.read()
