import asyncio
from typing import Any

from ariadne import convert_kwargs_to_snake_case, SubscriptionType
from graphql import GraphQLResolveInfo

from ariadne_example.app.core.struсtures import TASK_QUEUES
from ariadne_example.app.models import Task

subscription = SubscriptionType()


@subscription.source("taskStatusChanged")
@convert_kwargs_to_snake_case
async def task_source(obj: Any, info: GraphQLResolveInfo):
    queue = asyncio.Queue()
    TASK_QUEUES.append(queue)
    try:
        while True:
            change_task = await queue.get()
            queue.task_done()
            yield change_task
    except asyncio.CancelledError:
        TASK_QUEUES.remove(queue)
        raise


@subscription.field("taskStatusChanged")
@convert_kwargs_to_snake_case
def task_resolver(task: Task, info: Any):
    return task
