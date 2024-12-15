from dataclasses import dataclass
from os import getenv
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class DatabaseConfig:
    db_uri: str

    @staticmethod
    def from_env() -> "DatabaseConfig":
        uri = getenv("DATABASE_URI")

        return DatabaseConfig(str(uri))
