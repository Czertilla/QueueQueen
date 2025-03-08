from aiohttp import ClientSession
from pydantic import HttpUrl


class HTTPClient:
    """
    HTTP client wrapper for making requests to a specific base URL.

    Encapsulates an aiohttp ClientSession and a base URL for convenient request building.

    Attributes:
        base_url (HttpUrl): The base URL for the client.
        session (ClientSession): The aiohttp ClientSession instance.
    """

    def __init__(self, base_url: HttpUrl, session: ClientSession) -> None:
        """
        Initializes the HTTPClient with a base URL and ClientSession.

        Args:
            base_url (HttpUrl): The base URL for the client.
            session (ClientSession): The aiohttp ClientSession instance.
        """
        self.base_url = base_url
        self.session = session
