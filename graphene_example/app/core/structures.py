import enum

import graphene


class TaskStatusEnum(enum.Enum):
    draft = "draft"
    in_process = "in_process"
    delete = "delete"
    done = "done"


class TaskType(graphene.ObjectType):
    id = graphene.ID()
    created_at = graphene.DateTime(required=False)
    title = graphene.String
    status = graphene.Enum.from_enum(TaskStatusEnum)


class User(graphene.ObjectType):
    pass
