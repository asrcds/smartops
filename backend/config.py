from pydantic import Field  # Field 仍然从 pydantic 导入
from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets

class Settings(BaseSettings):
    # MySQL config
    DB_URL: str = Field(default='localhost')
    DB_USER: str = Field(default='root')
    DB_PASSWORD: str = Field(default='password')
    DB_NAME: str = Field(default='test')

    # InfluxDB config
    INFLUX_URL: str = Field(default='http://localhost:8086')
    INFLUX_TOKEN: str = Field(default='your_token')
    INFLUX_ORG: str = Field(default='your_org')
    INFLUX_BUCKET: str = Field(default='your_bucket')

    # JWT secret key
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    HOST: str = Field(default='mock_server01')

    def get_database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_URL}:3306/{self.DB_NAME}?charset=utf8mb4"
        )

    @property
    def DATABASE_URL(self) -> str:
        return self.get_database_url()

settings = Settings()
