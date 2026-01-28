from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    fatsecret_client_id: str | None
    fatsecret_client_secret: str | None
    database_url: str
    environment: str

REQUIRED_ENV_VARS = ("TELEGRAM_BOT_TOKEN",)
OPTIONAL_ENV_VARS = ("FATSECRET_CLIENT_ID", "FATSECRET_CLIENT_SECRET")

def load_settings() -> Settings:
    missing = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
    if missing:
        raise RuntimeError(
            "Missing required environment variables: " + ", ".join(missing)
        )

    return Settings(
        telegram_bot_token=os.environ["TELEGRAM_BOT_TOKEN"],
        fatsecret_client_id=os.getenv("FATSECRET_CLIENT_ID"),
        fatsecret_client_secret=os.getenv("FATSECRET_CLIENT_SECRET"),
        database_url=os.getenv(
            "DATABASE_URL", "postgresql://nofat:nofat@localhost:5432/nofat"
        ),
        environment=os.getenv("ENVIRONMENT", "development"),
    )

def summarize_optional_env() -> dict[str, bool]:
    return {name: bool(os.getenv(name)) for name in OPTIONAL_ENV_VARS}
