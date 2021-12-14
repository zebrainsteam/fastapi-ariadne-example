import graphene
from graphql_relay.node.node import from_global_id

from graphene_example.app.core.structures import TaskType
from graphene_example.app.db.session import Session, engine


class Query(graphene.ObjectType):
    get_user_tasks = graphene.List(TaskType, required=True)
    get_user_task_by_id = graphene.Field(TaskType, required=True)

    @staticmethod
    def resolve_get_user_tasks(parent, info, user_id: int):
        local_user_id, _ = from_global_id(user_id)
        with Session(engine) as session:
            statement = select(TaskType).where(TaskType.user_id == user_id)
            tasks = session.execute(statement).scalars().all()
            return [
                TaskType(
                    id=task.id,
                    created_at=task.created_at,
                    title=task.title,
                    status=task.status,
                    user_id=task.user_id,
                ) for task in tasks
            ]

    @staticmethod
    def resolve_get_user_task_by_id(parent, info, user_id, task_id):
        local_user_id, _ = from_global_id(user_id)
        local_task_id, _ = from_global_id(task_id)
        session = get_session()
        statement = select(TaskType).where(TaskType.user_id == local_user_id, TaskType.id == local_task_id)
        task = session.execute(statement).scalar_one()
        return TaskType(
            id=task.id,
            created_at=task.created_at,
            title=task.title,
            status=task.status,
            user_id=task.user_id,
        )
