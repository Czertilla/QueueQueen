import logging
import i18n
import aiocache
from pathlib import Path
from typing import Any, Optional

from utils.settings import getSettings

# Configure logging
logger = logging.getLogger(__name__)


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

        logger.info(
            f"Localization initialized  {self=}")
        
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the Localization object.

        :return: A string containing class name, default language, and TTL.
        """
        return f"<Localization(default_lang={self.default_lang}, ttl={self.ttl})>"

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
            logger.debug(f"Cache hit: {cache_key}")
            return cached_translation

        # Cache miss
        logger.debug(f"Cache miss: {cache_key}. Loading translation.")

        # Uploading the translation
        i18n.set("locale", lang)
        text: str = i18n.t(f"{markup}.{key}", **kwargs)

        # We put it in the cache with TTL
        await self.cache.set(cache_key, text, ttl=self.ttl)
        logger.debug(f"Cached new translation: {cache_key} (TTL: {self.ttl}s)")

        return text


# Global localization object
i18n_manager: Localization = Localization()
