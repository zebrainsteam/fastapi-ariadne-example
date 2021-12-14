from ariadne.contrib.tracing.utils import is_introspection_field

from ariadne_example.app.core.exceptions import BaseGraphQLError


async def handle_error_middleware(resolver, obj, info, **args):
    """
    Если на этапе выполнения мутации или запроса будет выброшено исключение, перехватить
    и вывести в качестве ошибки.
    """
    errors = []
    value = {}

    if is_introspection_field(info):
        return resolver(obj, info, **args)

    try:
        value = await resolver(obj, info, **args)
    except BaseGraphQLError as exc:
        errors.append(exc.parse())
        value = {**value, **{'errors': errors}}
    except TypeError:
        value = resolver(obj, info, **args)
    return value