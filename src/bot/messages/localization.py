import logging
from uuid import UUID
import i18n
import aiocache
from pathlib import Path
from typing import Any
from hashlib import sha256
import json

from utils.settings import getSettings

# Configure logging
logger = logging.getLogger(__name__)


class Localization:
    """
    Handles localization and caching for translated strings.

    Attributes:
        cache (aiocache.Cache): cache instanse
        TTL (int): default Time-to-live for cached translations from settings
            Defaults to `TTL_SECONDS` from settings
    """

    cache: aiocache.Cache = aiocache.Cache(aiocache.SimpleMemoryCache)
    TTL: int = getSettings().TTL_SECONDS

    def __init__(self, default_lang: str = "en", ttl: int = TTL) -> None:
        """
        Initializes the Localization instance.

        Args:
            default_lang (str, optional): Default language for translations.
                Defaults to "en".
            ttl (int, optional): Time-to-live for cached translations.
                Defaults to `TTL` attribute.
        """
        self.default_lang: str = default_lang
        self.translations_path: Path = Path(__file__).parent / "locales"
        self.ttl: int = ttl

        i18n.load_path.append(str(self.translations_path))
        i18n.set("fallback", self.default_lang)

        logger.info(f"Localization initialized: {self}")

    def __repr__(self) -> str:
        """
        Returns a string representation of the Localization instance.

        Returns:
            str: A formatted string containing the class name, default 
                language, and TTL.
        """
        return f"<Localization(default_lang={self.default_lang}, ttl={self.ttl})>"

    @staticmethod
    def hash_kwargs(kwargs: dict) -> str:
        filtered_kwargs = {
            k: (v.__hash__() if isinstance(v, UUID) else v)
            for k, v in kwargs.items()
        }
        return sha256(
            json.dumps(filtered_kwargs, sort_keys=True).encode()
        ).hexdigest()

    async def get(
        self, key: str, lang: str | None = None, markup: str = "HTML", **kwargs: Any
    ) -> str:
        """
        Retrieves a localized string asynchronously. Uses caching to improve
        performance.

        Args:
            key (str): The translation key.
            lang (str, optional): The language for the translation.
                Defaults to `None`, which falls back to `default_lang`.
            markup (str, optional): The format for the translation key.
                Defaults to "HTML".
            **kwargs (Any): Additional parameters for formatting.

        Returns:
            str: The translated string.
        """
        lang = lang or self.default_lang
        cache_key = f"i18n:{lang}:{key}"

        # Check cache
        cached_translation: str | None = await self.cache.get(cache_key)
        if cached_translation:
            logger.debug(f"Cache hit: {cache_key}")
            return cached_translation

        # Load translation if cache miss
        logger.debug(f"Cache miss: {cache_key}. Fetching translation.")

        i18n.set("locale", lang)
        text: str = i18n.t(f"{markup}.{key}", **kwargs)

        # Store in cache
        await self.cache.set(cache_key, text, ttl=self.ttl)
        logger.debug(f"Cached translation: {cache_key} (TTL: {self.ttl}s)")

        return text


# Global localization object
i18n_manager: Localization = Localization()
