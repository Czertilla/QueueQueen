from enum import StrEnum


class DBManagerType(StrEnum):
    sqlite = "sqlite"
    postgres = "postgres"

    __default__ = sqlite



class AppArchitecture(StrEnum):
    MICROSERVICES = "microservices"
    MONOLITH = "monolith"

    __default__ = MICROSERVICES


class TgBotFeedType(StrEnum):
    POLLING = "long-polling"
    WEBHOOK = "web-hook"

    __default__ = WEBHOOK