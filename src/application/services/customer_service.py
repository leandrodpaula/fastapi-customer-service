# src/application/services/customer_service.py
import uuid
from typing import List, Optional

from src.domain.entities import Customer as DomainCustomer
from src.domain.use_cases import (
    CreateCustomerUseCase,
    GetCustomerByIdUseCase,
    GetAllCustomersUseCase,
    UpdateCustomerUseCase,
    DeleteCustomerUseCase,
)
from src.domain.repositories import CustomerRepository
# Import GQL types for return type hinting if desired, though service layer should ideally be GQL-agnostic
# from src.interfaces.graphql_resolvers.types import Customer as GQLCustomer

class CustomerService:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def create_customer(self, name: str, email: str) -> DomainCustomer:
        use_case = CreateCustomerUseCase(self.customer_repository)
        # Here we could map input DTOs to domain if they were different
        return await use_case.execute(name=name, email=email)

    async def get_customer_by_id(self, customer_id: uuid.UUID) -> Optional[DomainCustomer]:
        use_case = GetCustomerByIdUseCase(self.customer_repository)
        return await use_case.execute(customer_id)

    async def get_all_customers(self) -> List[DomainCustomer]:
        use_case = GetAllCustomersUseCase(self.customer_repository)
        return await use_case.execute()

    async def update_customer(self, customer_id: uuid.UUID, name: Optional[str] = None, email: Optional[str] = None) -> Optional[DomainCustomer]:
        use_case = UpdateCustomerUseCase(self.customer_repository)
        return await use_case.execute(customer_id=customer_id, name=name, email=email)

    async def delete_customer(self, customer_id: uuid.UUID) -> bool:
        use_case = DeleteCustomerUseCase(self.customer_repository)
        return await use_case.execute(customer_id)
