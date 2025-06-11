# src/interfaces/graphql_resolvers/resolvers.py
import uuid
import strawberry
from typing import List, Optional

from src.interfaces.graphql_resolvers.types import Customer, CreateCustomerInput, UpdateCustomerInput
from src.application.services.customer_service import CustomerService
# No longer need direct import of MongoCustomerRepository here for instantiation

@strawberry.type
class Query:
    @strawberry.field
    async def customers(self, info: strawberry.Info) -> List[Customer]:
        service: CustomerService = info.context["customer_service"]
        domain_customers = await service.get_all_customers()
        # Simple mapping for now
        return [Customer(id=dc.id, name=dc.name, email=dc.email) for dc in domain_customers]

    @strawberry.field
    async def customer(self, info: strawberry.Info, id: uuid.UUID) -> Optional[Customer]:
        service: CustomerService = info.context["customer_service"]
        domain_customer = await service.get_customer_by_id(id)
        if domain_customer:
            return Customer(id=domain_customer.id, name=domain_customer.name, email=domain_customer.email)
        return None

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_customer(self, info: strawberry.Info, input: CreateCustomerInput) -> Customer:
        service: CustomerService = info.context["customer_service"]
        try:
            domain_customer = await service.create_customer(name=input.name, email=input.email)
            return Customer(id=domain_customer.id, name=domain_customer.name, email=domain_customer.email)
        except ValueError as e:
            # Consider using Strawberry's error handling extensions for more structured errors
            raise Exception(str(e)) # Or map to a specific GraphQL error type

    @strawberry.mutation
    async def update_customer(self, info: strawberry.Info, id: uuid.UUID, input: UpdateCustomerInput) -> Optional[Customer]:
        service: CustomerService = info.context["customer_service"]
        try:
            domain_customer = await service.update_customer(customer_id=id, name=input.name, email=input.email)
            if domain_customer:
                return Customer(id=domain_customer.id, name=domain_customer.name, email=domain_customer.email)
            return None # Or raise a NotFound error if preferred for GraphQL
        except ValueError as e:
            raise Exception(str(e))
        except Exception as e:
            # Log error e before raising a generic one
            # import logging
            # logging.error(f"Unexpected error during update_customer: {e}", exc_info=True)
            raise Exception("An unexpected error occurred during customer update.")

    @strawberry.mutation
    async def delete_customer(self, info: strawberry.Info, id: uuid.UUID) -> bool:
        service: CustomerService = info.context["customer_service"]
        try:
            # The service layer's delete_customer returns a boolean.
            # True if deleted, False if not found or failed.
            # This directly maps to the GraphQL boolean return type.
            return await service.delete_customer(id)
        except Exception as e:
            # import logging
            # logging.error(f"Unexpected error during delete_customer: {e}", exc_info=True)
            raise Exception("An unexpected error occurred during customer deletion.")
