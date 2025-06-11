# src/interfaces/graphql_resolvers/types.py
import uuid
import strawberry
from typing import Optional

@strawberry.type
class Customer:
    id: uuid.UUID
    name: str
    email: str

@strawberry.input
class CreateCustomerInput:
    name: str
    email: str

@strawberry.input
class UpdateCustomerInput:
    name: Optional[str] = None
    email: Optional[str] = None
