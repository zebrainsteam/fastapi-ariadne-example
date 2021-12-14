import graphene
from graphql_relay.node.node import from_global_id

from graphene_example.app.core.structures import TaskType, TaskStatusEnum
from graphene_example.app.db.session import Session, engine
from graphene_example.app.models import Task

class TaskInputType(graphene.InputObjectType):
    created_at = graphene.DateTime(required=False)
    title = graphene.String(required=True)
    status = graphene.String()



class CreateTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        user_id = graphene.ID()
        input_data = TaskInputType(required=True)

    def mutate(self, parent, info, user_id: str, input_data: dict):
        local_user_id, _ = from_global_id(user_id)
        with Session(engine) as session:
            task = Task(title=input_data.get("title"), user_id=local_user_id)
            session.add(task)
            session.commit()
            session.refresh()
            return CreateTask(task=task)


class ChangeTaskStatus(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        task_id = graphene.ID()
        new_status = graphene.String()

    def mutate(self, parent, info, task_id: str, new_status: TaskStatusEnum):
        local_task_id, _ = from_global_id(task_id)
        with Session(engine) as session:
            statement = select(Task).where(Task.id == local_task_id)
            task = session.execute(statement)
            task.status = new_status
            session.add(task)
            session.refresh(task)
            return ChangeTaskStatus(task=task)
