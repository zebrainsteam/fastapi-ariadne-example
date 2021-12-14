
from typing import List, Union
from ariadne.asgi import GraphQL
from starlette.routing import WebSocketRoute, Route
from ariadne import make_executable_schema, load_schema_from_path, snake_case_fallback_resolvers

from ariadne_example.app.api.mutations import mutations
from ariadne_example.app.api.queries import queries
from ariadne_example.app.api.subscriptions import subscription
from ariadne_example.app.core.config import settings
from ariadne_example.app.core.struсtures import task_type_enum, datetime_scalar
from ariadne_example.app.core.middlewares import handle_error_middleware

type_defs = load_schema_from_path(settings.GQL_FILE)

schema = make_executable_schema(
    type_defs,
    queries,
    mutations,
    subscription,
    snake_case_fallback_resolvers,
    task_type_enum,
    datetime_scalar,
)


def init_gql_route() -> List[Union[Route, WebSocketRoute]]:
    return [
        Route("/graphql", GraphQL(schema, middleware=[handle_error_middleware], debug=settings.DEBUG)),  # noqa
        WebSocketRoute("/graphql", GraphQL(schema, debug=settings.DEBUG)),
    ]
