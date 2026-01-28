from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class FatSecretCredentials:
    client_id: str
    client_secret: str

class FatSecretService:
    """Placeholder for FatSecret API integration.

    TODO: implement OAuth flow and nutrition diary import.
    """

    def __init__(self, credentials: FatSecretCredentials) -> None:
        self._credentials = credentials

    async def fetch_daily_diary(self, user_id: int) -> dict:
        raise NotImplementedError("FatSecret integration not implemented yet.")
