# src/interfaces/graphql_resolvers/schema.py
import strawberry
from src.interfaces.graphql_resolvers.resolvers import Query, Mutation

schema = strawberry.Schema(query=Query, mutation=Mutation)
