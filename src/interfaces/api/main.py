# src/interfaces/api/main.py
from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter

from src.interfaces.graphql_resolvers.schema import schema
from src.application.services.customer_service import CustomerService
from src.infrastructure.database.mongo_customer_repository import MongoCustomerRepository
from src.domain.repositories import CustomerRepository

# Dependency Injection for FastAPI
def get_customer_repository() -> CustomerRepository:
    return MongoCustomerRepository()

def get_customer_service(
    repo: CustomerRepository = Depends(get_customer_repository)
) -> CustomerService:
    return CustomerService(customer_repository=repo)

# Adjust GraphQL resolvers to use FastAPI's Depends
# This requires modifying how service is obtained in resolvers.py or by passing context.
# For now, we will create a context for Strawberry to carry dependencies.

async def get_context(
    customer_service: CustomerService = Depends(get_customer_service),
):
    return {
        "customer_service": customer_service
    }

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI(
    title="Customer API",
    description="A Clean Architecture Customer API with FastAPI and GraphQL",
    version="0.1.0"
)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Customer API. Visit /graphql for the GraphQL interface."}

# The following modification is needed in src/interfaces/graphql_resolvers/resolvers.py
# to use the context from FastAPI/Strawberry:
#
# Replace:
# async def get_customer_service() -> CustomerService: ...
# service = await get_customer_service()
#
# With:
# In Query and Mutation methods, access service via info.context:
# service: CustomerService = info.context["customer_service"]
#
# Example for one method in Query:
# @strawberry.field
# async def customers(self, info: strawberry.Info) -> List[Customer]:
#     service: CustomerService = info.context["customer_service"]
#     domain_customers = await service.get_all_customers()
#     return [Customer(id=dc.id, name=dc.name, email=dc.email) for dc in domain_customers]
#
# This change will be applied by a subsequent step if this subtask becomes too large.
# For now, this comment serves as a reminder.
