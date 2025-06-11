# src/domain/use_cases/delete_customer.py
import uuid
from src.domain.repositories.customer_repository import CustomerRepository

class DeleteCustomerUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def execute(self, customer_id: uuid.UUID) -> bool:
        customer = await self.customer_repository.find_by_id(customer_id)
        if not customer:
            return False # Or raise an exception, e.g., CustomerNotFound
        return await self.customer_repository.delete(customer_id)
