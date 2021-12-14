from ariadne import ObjectType

from ariadne_example.app.api.queries import task

queries = ObjectType("Query")

queries.set_field("getTasks", task.resolve_get_user_tasks)
queries.set_field("getTask", task.resolve_get_user_task_by_id)
