import json
from typing import Any, List

from ariadne import convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from graphql_relay.node.node import from_global_id
from sqlmodel import select

from ariadne_example.app.db.session import Session, engine
from ariadne_example.app.models import Task

@convert_kwargs_to_snake_case
def resolve_get_user_tasks(
        obj: Any,
        info: GraphQLResolveInfo,
        user_id: str,
) -> List[dict]:
    """Get user tasks"""
    with Session(engine) as session:
        local_user_id, _ = from_global_id(user_id)
        statement = select(Task).where(Task.user_id == int(local_user_id))
        tasks = session.execute(statement).scalars().all()
        return [
            Task(
                id=task.id,
                created_at=task.created_at,
                title=task.title,
                status=task.status,
                user_id=task.user_id
            ).dict()
            for task in tasks
        ]

@convert_kwargs_to_snake_case
def resolve_get_user_task_by_id(
        obj: Any,
        info: GraphQLResolveInfo,
        task_id: str,
        user_id: str,
) -> dict:
    """Get user task by task ID."""
    with Session(engine) as session:
        local_task_id, _ = from_global_id(task_id)
        local_user_id, _ = from_global_id(user_id)
        statement = select(Task).where(Task.user_id == local_user_id, Task.id == local_task_id)
        task = session.execute(statement).scalar_one()
        return Task(
            id=task.id,
            created_at=task.created_at,
            title=task.title,
            status=task.status,
            user_id=task.user_id,
        ).dict()