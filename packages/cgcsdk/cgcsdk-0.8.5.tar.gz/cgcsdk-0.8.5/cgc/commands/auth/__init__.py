from cgc.commands.exceptions import ResponseException


class AuthCommandException(ResponseException):
    pass


class NoNamespaceInConfig(AuthCommandException):
    def __init__(self) -> None:
        super().__init__(f"Namespace not readable from config file.")
