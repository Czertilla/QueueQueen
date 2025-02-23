import i18n
import asyncio
import aiocache
from pathlib import Path
from typing import Any, Optional

from utils.settings import getSettings

class Localization:
    cache: aiocache.Cache = aiocache.Cache(aiocache.SimpleMemoryCache)
    TTL: int = getSettings().TTL_SECONDS

    def __init__(self, default_lang: str = "en", ttl: int = TTL) -> None:
        """
        Initializes the Localization object.
        
        :param default_lang: The default language for localization (default is 'en')
        :param ttl: Time-to-live for cache entries (default is TTL from settings)
        """
        self.default_lang: str = default_lang
        self.translations_path: Path = Path(__file__).parent / "locales"
        self.ttl: int = ttl
        
        assert isinstance(i18n.load_path, list)
        i18n.load_path.append(str(self.translations_path))
        i18n.set("fallback", self.default_lang)

    async def get(
            self, key: str, lang: Optional[str] = None, 
            markup: str = "HTML", **kwargs: Any
    ) -> str:
        """
        Asynchronously retrieves the localization string from cache or loads 
        it if not cached.
        
        :param key: The translation key
        :param lang: The language to retrieve the translation in 
            (default is None, falls back to default_lang)
        :param markup: The format for the translation key (default is "HTML")
        :param kwargs: Additional arguments for translation formatting
        :return: Translated string
        """
        lang = lang or self.default_lang
        cache_key = f"i18n:{lang}:{key}"

        # Checking the cache
        cached_translation: Optional[str] = await self.cache.get(cache_key)
        if cached_translation:
            return cached_translation

        # Uploading the translation
        i18n.set("locale", lang)
        text: str = i18n.t(f"{markup}.{key}", **kwargs)

        # We put it in the cache with TTL = 5 minutes
        await self.cache.set(cache_key, text, ttl=self.ttl)
        return text

# Global localization object
i18n_manager: Localization = Localization()
