from json import dumps
from traceback import format_tb

from typing import Any



class RichException(Exception):
    def __init__(
            self,
            message: str,
            meta: dict[str, Any] = None,
            name: str = "Exception"
        ) -> None:
        super().__init__(message)
        self.name = name
        self.message = message
        self.meta = meta or {}
    
    def __str__(
            self,
            newline: str = "\n"
        ) -> str:
        meta_stringified = [
            f" - {k}: {dumps(v, default=str)}"
            for (k,v) in self.meta.items()
        ]
        return newline.join([
            f"{self.name}: {self.message}",
            "",
            "Metadata:",
            *meta_stringified,
            "",
            "Traceback:",
            "".join(format_tb(self.__traceback__))
        ])