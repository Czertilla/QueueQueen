import i18n
import asyncio
import aiocache
from pathlib import Path
from typing import Any

from utils.settings import getSettings

class Localization:
    cache = aiocache.Cache(aiocache.SimpleMemoryCache)
    TTL = getSettings().TTL_SECONDS

    def __init__(self, default_lang: str = "en", ttl: int = TTL):
        self.default_lang = default_lang
        self.translations_path = Path(__file__).parent / "locales"
        self.ttl = ttl
        
        assert isinstance(i18n.load_path, list)
        i18n.load_path.append(str(self.translations_path))
        i18n.set("fallback", self.default_lang)
        i18n.set('filename_format', '{locale}.{format}')

    async def get(self, key: str, lang: str = None, **kwargs) -> str:
        """Asynchronously retrieves the localization string with the cache."""
        lang = lang or self.default_lang
        cache_key = f"i18n:{lang}:{key}"

        # Checking the cache
        cached_translation = await self.cache.get(cache_key)
        if cached_translation:
            return cached_translation

        # Uploading the translation
        i18n.set("locale", lang)
        text = i18n.t(key, **kwargs)

        # We put it in the cache with TTL = 5 minutes
        await self.cache.set(cache_key, text, ttl=self.ttl)
        return text

# Global localization object
i18n_manager = Localization()