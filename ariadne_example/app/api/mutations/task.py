from typing import Any

import sqlalchemy.exc
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo
from graphql_relay.node.node import from_global_id
from sqlmodel import select

from ariadne_example.app.db.session import Session, engine
from ariadne_example.app.core.struсtures import TaskStatusEnum, TASK_QUEUES
from ariadne_example.app.models import Task
from ariadne_example.app.core.exceptions import NotFoundError

@convert_kwargs_to_snake_case
def resolve_create_task(
        obj: Any,
        info: GraphQLResolveInfo,
        user_id: str,
        task_input: dict,
) -> int:
    with Session(engine) as session:
        local_user_id, _ = from_global_id(user_id)
        try:
            task = Task(
                title=task_input.get("title"),
                created_at=task_input.get("created_at"),
                status=task_input.get("status"),
                user_id=local_user_id
            )
            session.add(task)
            session.commit()
            session.refresh(task)
        except sqlalchemy.exc.IntegrityError:
            raise NotFoundError(msg='Не найден пользователь с таким user_id')
        return task.id


@convert_kwargs_to_snake_case
async def resolve_change_task_status(
        obj: Any,
        info: GraphQLResolveInfo,
        new_status: TaskStatusEnum,
        task_id: str,
) -> None:
    with Session(engine) as session:
        local_task_id, _ = from_global_id(task_id)
        try:
            statement = select(Task).where(Task.id == local_task_id)
            task = session.execute(statement)
            task.status = new_status
            session.add(task)
            session.commit()
            session.refresh(task)
        except sqlalchemy.exc.IntegrityError:
            raise NotFoundError(msg='Не найдена задача с таким task_id')
        for queue in TASK_QUEUES:
            queue.put(task)
