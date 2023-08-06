from typing import Protocol


class Logger(Protocol):
    """
    Logger protocol
    """

    def debug(self, msg: str):
        ...

    def info(self, msg: str):
        ...

    def warning(self, msg: str):
        ...

    def error(self, msg: str):
        ...

    def exception(self, msg: str):
        ...
