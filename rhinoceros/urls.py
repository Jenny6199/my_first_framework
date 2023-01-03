from dataclasses import dataclass
from rhinoceros.view import View
from typing import Type


@dataclass
class Url:
    url: str
    view: Type[View]
