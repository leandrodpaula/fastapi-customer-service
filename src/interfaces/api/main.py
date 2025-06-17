# src/interfaces/api/main.py
from fastapi import FastAPI, Depends, HTTPException, status # Added HTTPException, status
from strawberry.fastapi import GraphQLRouter
from typing import List # Import List for potential future list responses

from src.interfaces.graphql_resolvers.schema import schema
from src.application.services.customer_service import CustomerService
from src.infrastructure.database.mongo_customer_repository import MongoCustomerRepository
from src.domain.repositories import CustomerRepository
from src.domain.entities import Customer as DomainCustomer # For type hinting
from .schemas import CustomerCreateRequest, CustomerResponse # Import Pydantic models

# Dependency Injection for FastAPI
def get_customer_repository() -> CustomerRepository:
    return MongoCustomerRepository()

def get_customer_service(
    repo: CustomerRepository = Depends(get_customer_repository)
) -> CustomerService:
    return CustomerService(customer_repository=repo)

async def get_context(
    customer_service: CustomerService = Depends(get_customer_service),
):
    return {
        "customer_service": customer_service
    }

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI(
    title="Customer API",
    description="A Clean Architecture Customer API with FastAPI, GraphQL, and RESTful elements.",
    version="0.1.0"
)

# Mount GraphQL router
app.include_router(graphql_app, prefix="/graphql")

# New REST endpoint for creating a customer
@app.post("/customers/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED, tags=["Customers"])
async def create_customer_rest(
    customer_data: CustomerCreateRequest,
    service: CustomerService = Depends(get_customer_service)
):
    """
    Create a new customer via REST.
    """
    try:
        # The service's create_customer method expects name and email directly
        created_domain_customer = await service.create_customer(
            name=customer_data.name,
            email=customer_data.email
        )
        # Convert domain model to Pydantic response model
        return CustomerResponse(
            id=created_domain_customer.id,
            name=created_domain_customer.name,
            email=created_domain_customer.email
        )
    except ValueError as e:
        # Handle domain validation errors, e.g., customer already exists
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Catch-all for other unexpected errors
        # Log the error e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Customer API. Visit /graphql for GraphQL or /docs for REST API documentation."}

# Update __init__.py in src/interfaces/api if schemas.py needs to be easily importable (optional)
# For now, direct import from .schemas in main.py is fine.
