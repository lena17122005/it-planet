from dataclasses import dataclass

import httpx

from app.core.config import settings


@dataclass
class Coordinates:
    lat: float
    lon: float


async def geocode_address(address: str) -> Coordinates | None:
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": settings.nominatim_user_agent}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(settings.nominatim_url, params=params, headers=headers)
            response.raise_for_status()
            payload = response.json()
    except Exception:
        # Geocoding should not break vacancy creation flow.
        return None

    if not payload:
        return None

    first = payload[0]
    return Coordinates(lat=float(first["lat"]), lon=float(first["lon"]))
