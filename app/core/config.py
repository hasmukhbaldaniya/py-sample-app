from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

# Get the project root directory (3 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def db_url(self) -> URL:
        """
        Returns the database url from settings.
        :return:
        """
        return URL.create(
            drivername="postgresql+psycopg2",
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
        )

settings = Settings()
