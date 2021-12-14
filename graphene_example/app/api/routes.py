import graphene
from fastapi import FastAPI

from starlette.graphql import GraphQLApp

from graphene_example.app.api.queries.task import Query
from graphene_example.app.api.mutations import Mutation

def init_gql_route(app: FastAPI) -> None:
    app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))