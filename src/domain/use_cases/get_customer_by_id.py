# src/domain/use_cases/get_customer_by_id.py
import uuid
from typing import Optional
from src.domain.entities.customer import Customer
from src.domain.repositories.customer_repository import CustomerRepository

class GetCustomerByIdUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def execute(self, customer_id: uuid.UUID) -> Optional[Customer]:
        return await self.customer_repository.find_by_id(customer_id)
