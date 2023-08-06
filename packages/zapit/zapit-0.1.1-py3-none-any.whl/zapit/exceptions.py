class ZapitException(Exception):
    """Base exception for Zapit"""


class RequestException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NoOrganizationError(ZapitException):
    ...
