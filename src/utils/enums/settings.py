from utils.abstract.enum import AEnum


class DBManagerType(str, AEnum):
    sqlite = "sqlite"
    postgres = "postgres"

    __default__ = sqlite
