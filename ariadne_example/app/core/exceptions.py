from typing import Optional, Dict, Any

from graphql import GraphQLError

from ariadne_example.app.core.struсtures import ErrorTypes, ErrorScalar


class BaseGraphQLError(GraphQLError):
    def __init__(self, msg: str = "Server Error", extensions: Optional[Dict[str, Any]] = None):
        if not hasattr(self, "_extensions"):
            self._extensions = {"code": ErrorTypes.SERVER_ERROR.name}
        if extensions is not None:
            self._extensions = {**self._extensions, **extensions}
        super().__init__(msg, extensions=self._extensions)

    def parse(self) -> ErrorScalar:
        parsed_exception = ErrorScalar(
            message=self.extensions.get("user_message"),
            code=self.extensions.get("code"),
            text=self.message,
        )
        return parsed_exception


class ValidationError(BaseGraphQLError):
    def __init__(self, msg: str, extensions: Optional[Dict[str, Any]] = None):
        self._extensions = {"code": ErrorTypes.VALIDATION_ERROR.name}
        super().__init__(msg, extensions=extensions)


class NotFoundError(BaseGraphQLError):
    def __init__(self, msg: str, extensions: Optional[Dict[str, Any]] = None):
        self._extensions = {"code": ErrorTypes.NOT_FOUND_ERROR.name}
        super().__init__(msg, extensions=extensions)
