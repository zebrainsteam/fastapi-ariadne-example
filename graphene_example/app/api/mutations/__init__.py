import graphene

from graphene_example.app.api.mutations.task import CreateTask, ChangeTaskStatus

class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    change_task = ChangeTaskStatus.Field()