"""Сервис геокодирования (каркас).

На следующем этапе будет реализован вызов Nominatim и кэширование ответов.
"""

from dataclasses import dataclass


@dataclass
class Coordinates:
    lat: float
    lon: float


def geocode_address(_address: str) -> Coordinates | None:
    # TODO: подключить httpx + Nominatim API.
    return None
