import pytest
from src.bot.localization import localization

# Создаём отдельный объект локализации для тестов
@pytest.fixture(scope="function")
async def i18n_test():
    localizer = localization.Localization(default_lang="en")
    yield localizer
    await localizer.cache.clear()  # Очищаем кэш после каждого теста

@pytest.mark.asyncio
async def test_translation_loading(i18n_test):
    """Тестирует корректность загрузки перевода."""
    text = await i18n_test.get("start_message", lang="ru", username="Тест")
    assert text == "Привет, Тест! Добро пожаловать в нашего бота."

@pytest.mark.asyncio
async def test_fallback_language(i18n_test):
    """Тестирует fallback на английский, если языка нет."""
    text = await i18n_test.get("start_message", lang="fr", username="Test")
    assert text == "Hello, Test! Welcome to our bot."

@pytest.mark.asyncio
async def test_cache_functionality(i18n_test):
    """Тестирует, что значение кешируется."""
    key = "help_message"
    lang = "ru"

    # Загружаем первый раз
    text1 = await i18n_test.get(key, lang=lang)
    
    # Проверяем, что оно есть в кеше
    cached_text = await i18n_test.cache.get(f"i18n:{lang}:{key}")
    
    assert cached_text == text1, "Значение не сохранилось в кэш"

@pytest.mark.asyncio
async def test_missing_key(i18n_test):
    """Тестирует, что если ключа нет, возвращается сам ключ."""
    text = await i18n_test.get("unknown_key", lang="ru")
    assert text == "unknown_key", "Ожидался возврат самого ключа"
