from ariadne import ObjectType

from .task import resolve_create_task

mutations = ObjectType('Mutations')

mutations.set_field('createTask', resolve_create_task)
