from aiohttp import ClientSession
from pydantic import HttpUrl


class HTTPClient:
    def __init__(self, base_url: HttpUrl, session: ClientSession) -> None:
        self.base_url = base_url
        self.session = session
