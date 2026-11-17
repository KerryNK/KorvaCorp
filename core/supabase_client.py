from functools import lru_cache

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from supabase import Client, create_client


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """Return a reusable Supabase client configured from Django settings."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_PUBLISHABLE_KEY:
        raise ImproperlyConfigured(
            "Set SUPABASE_URL and SUPABASE_PUBLISHABLE_KEY before using Supabase."
        )

    return create_client(settings.SUPABASE_URL, settings.SUPABASE_PUBLISHABLE_KEY)
