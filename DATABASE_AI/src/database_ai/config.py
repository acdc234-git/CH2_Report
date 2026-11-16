from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """.env 파일의 값을 읽어 담는다."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    supabase_url: str
    supabase_key: str

settings = Settings()

