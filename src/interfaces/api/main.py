# src/interfaces/api/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from strawberry.fastapi import GraphQLRouter
from typing import List, Dict, Any # Import Dict, Any

from src.interfaces.graphql_resolvers.schema import schema
from src.application.services.customer_service import CustomerService
from src.infrastructure.database.mongo_customer_repository import MongoCustomerRepository
from src.domain.repositories import CustomerRepository
from src.domain.entities import Customer as DomainCustomer
from .schemas import CustomerCreateRequest, CustomerResponse

# --- GraphQL Request Body Examples ---
graphql_examples = {
    "GetAllCustomers": {
        "summary": "Get All Customers Query",
        "description": "Example query to fetch all customers.",
        "value": {
            "query": """
                query GetAllCustomers {
                  customers {
                    id
                    name
                    email
                  }
                }
            """
        }
    },
    "GetCustomerById": {
        "summary": "Get Customer by ID Query",
        "description": "Example query to fetch a single customer by their ID. Replace `your-customer-uuid` with an actual ID.",
        "value": {
            "query": """
                query GetCustomerById($customerId: UUID!) {
                  customer(id: $customerId) {
                    id
                    name
                    email
                  }
                }
            """,
            "variables": {"customerId": "a1b2c3d4-e5f6-7890-1234-567890abcdef"}
        }
    },
    "CreateCustomerMutation": {
        "summary": "Create Customer Mutation",
        "description": "Example mutation to create a new customer.",
        "value": {
            "query": """
                mutation CreateNewCustomer($name: String!, $email: String!) {
                  createCustomer(input: {name: $name, email: $email}) {
                    id
                    name
                    email
                  }
                }
            """,
            "variables": {"name": "GraphQL User", "email": "graphql.user@example.com"}
        }
    },
    "UpdateCustomerMutation": {
        "summary": "Update Customer Mutation",
        "description": "Example mutation to update an existing customer. Replace `your-customer-uuid`.",
        "value": {
            "query": """
                mutation UpdateExistingCustomer($customerId: UUID!, $name: String, $email: String) {
                  updateCustomer(id: $customerId, input: {name: $name, email: $email}) {
                    id
                    name
                    email
                  }
                }
            """,
            "variables": {
                "customerId": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "name": "Updated GraphQL User"
                # email can also be provided
            }
        }
    },
    "DeleteCustomerMutation": {
        "summary": "Delete Customer Mutation",
        "description": "Example mutation to delete a customer by ID. Replace `your-customer-uuid`.",
        "value": {
            "query": """
                mutation DeleteExistingCustomer($customerId: UUID!) {
                  deleteCustomer(id: $customerId)
                }
            """,
            "variables": {"customerId": "a1b2c3d4-e5f6-7890-1234-567890abcdef"}
        }
    }
}

# Dependency Injection for FastAPI (remains the same)
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

# Initialize FastAPI app
app = FastAPI(
    title="Customer API",
    description="A Clean Architecture Customer API with FastAPI, GraphQL, and RESTful elements.",
    version="0.1.0"
)

# Setup GraphQL app
# Note: The GraphQLRouter instance must be the same for include_router and for schema customization if any.
# graphiql=True is default, but explicit for clarity.
graphql_app_router = GraphQLRouter(schema, context_getter=get_context, graphiql=True)
app.include_router(
    graphql_app_router, # Use the same instance
    prefix="/graphql",
    tags=["GraphQL"],
)

# Customizing the OpenAPI schema for GraphQL examples
def custom_openapi():
    if app.openapi_schema: # Check if schema is already cached
        return app.openapi_schema

    # Generate the default schema once
    openapi_schema = app.openapi() # This will call the original app.openapi()

    # Find the path for /graphql and its POST operation
    # Ensure paths and operations exist before modification
    if "/graphql" in openapi_schema.get("paths", {}) and \
       "post" in openapi_schema["paths"]["/graphql"]:

        graphql_post_op = openapi_schema["paths"]["/graphql"]["post"]

        # Ensure requestBody and its content structure exist
        if "requestBody" not in graphql_post_op or not isinstance(graphql_post_op.get("requestBody"), dict):
             graphql_post_op["requestBody"] = {"content": {}}
        if "application/json" not in graphql_post_op["requestBody"].get("content", {}):
            graphql_post_op["requestBody"]["content"]["application/json"] = {}

        # Add the examples
        graphql_post_op["requestBody"]["content"]["application/json"]["examples"] = graphql_examples

    app.openapi_schema = openapi_schema # Cache the modified schema
    return app.openapi_schema

app.openapi = custom_openapi


# REST endpoint for creating a customer (remains the same)
@app.post("/customers/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED, tags=["Customers"])
async def create_customer_rest(
    customer_data: CustomerCreateRequest,
    service: CustomerService = Depends(get_customer_service)
):
    """
    Create a new customer via REST.
    """
    try:
        created_domain_customer = await service.create_customer(
            name=customer_data.name,
            email=customer_data.email
        )
        return CustomerResponse(
            id=created_domain_customer.id,
            name=created_domain_customer.name,
            email=created_domain_customer.email
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Log the error e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Customer API. Visit /graphql for GraphQL or /docs for REST API documentation."}
