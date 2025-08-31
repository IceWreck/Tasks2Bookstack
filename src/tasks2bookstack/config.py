from tasks2bookstack.log import get_logger
import yaml
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Type

logger = get_logger(name=__name__)


@dataclass
class Config:
    ...

    @staticmethod
    def from_yaml(file_path: Path) -> "Config": ...

    def to_json(self) -> str:
        """
        Returns a pretty printed JSON string of the configuration.
        """
        return json.dumps(asdict(self), indent=4)
