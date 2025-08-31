import yaml
from pathlib import Path

from pydantic import BaseModel


class BookstackConfig(BaseModel):
    """
    Configuration for the Bookstack API.
    """

    url: str
    token_id: str
    token_secret: str
    page_id: int


class CaldavConfig(BaseModel):
    """
    Configuration for the Caldav server.
    """

    url: str
    username: str
    password: str
    calendar: str


class Config(BaseModel):
    """
    The main configuration for the application.
    """

    bookstack: BookstackConfig
    caldav: CaldavConfig

    @staticmethod
    def from_yaml(file_path: Path) -> "Config":
        """
        Loads the configuration from a YAML file.
        """
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
        return Config.model_validate(data)
