import pydantic
import pydantic_settings
import os
import functools

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development").lower()


class DatabaseSettings(pydantic.BaseModel):
    protocol: str = "mongodb"
    user: str
    password: str
    host: str
    name: str


class LoggingSettings(pydantic.BaseModel):
    level: str = "INFO"


class Settings(pydantic_settings.BaseSettings):
    application_name: str = "engin33ring-thesis"
    database: DatabaseSettings
    logging: LoggingSettings = LoggingSettings()

    model_config = {"env_nested_delimiter": "__"}

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        source = pydantic_settings.YamlConfigSettingsSource(
            settings_cls, yaml_file=f"backend/resources/config_{ENVIRONMENT}.yaml"
        )
        return (
            source,
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,  # as in base method
        )


settings = Settings()


@functools.lru_cache(maxsize=1)
def get_settings() -> Settings:
    return settings
